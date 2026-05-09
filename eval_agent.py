import os
import json
import requests
from flask import Flask, request, jsonify
from anthropic import Anthropic
from scorer import compute_breakdown, compute_final_score, get_verdict
from checklists import CHECKLISTS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
client = Anthropic()

def fetch_agent_card(agent_id: str) -> dict:
    try:
        url = f"https://zns01.zynd.ai/v1/agents/{agent_id}"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return response.json()
    except Exception:
        pass
    return {}

def run_checklist(dimension: str, questions: list, agent_desc: str, input_text: str, output_text: str) -> list[str]:
    questions_formatted = "\n".join([f"{i+1}. {q} (Yes/No)" for i, q in enumerate(questions)])
    
    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=256,
        system="""You are a strict evaluator. 
Answer each question with ONLY 'Yes' or 'No'. 
One answer per line. No explanations.""",
        messages=[{
            "role": "user",
            "content": f"""Agent purpose: {agent_desc}

User input: {input_text}

Agent output: {output_text}

Answer each question with Yes or No only:
{questions_formatted}"""
        }]
    )
    
    answers = message.content[0].text.strip().split("\n")
    return [a.strip() for a in answers if a.strip()]

@app.route("/eval", methods=["POST"])
def evaluate():
    data = request.json
    
    agent_id = data.get("agent_id", "")
    input_text = data.get("input", "")
    output_text = data.get("output", "")
    start_time = data.get("start_time")
    end_time = data.get("end_time")

    # fetch agent card
    card = fetch_agent_card(agent_id)
    agent_desc = card.get("description", "A general purpose AI agent")

    # run checklists
    dimension_answers = {}
    for dimension, questions in CHECKLISTS.items():
        answers = run_checklist(dimension, questions, agent_desc, input_text, output_text)
        dimension_answers[dimension] = answers

    # compute scores
    breakdown = compute_breakdown(dimension_answers)

    # response time score if provided
    if start_time and end_time:
        elapsed = end_time - start_time
        breakdown["response_time"] = round(max(0, 10 - elapsed), 2)

    final_score = compute_final_score(breakdown)
    verdict = get_verdict(final_score)

    return jsonify({
        "agent_id": agent_id,
        "score": final_score,
        "verdict": verdict,
        "breakdown": breakdown,
        "agent_description": agent_desc
    })

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(port=5000, debug=True)