import os
import json
import requests
from anthropic import Anthropic
from scorer import compute_breakdown, compute_final_score, get_verdict
from checklists import CHECKLISTS
from dotenv import load_dotenv
from zyndai_agent.agent import AgentConfig, ZyndAIAgent

load_dotenv()

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

def run_checklist(dimension: str, questions: list, agent_desc: str, input_text: str, output_text: str) -> list:
    questions_formatted = "\n".join([f"{i+1}. {q} (Yes/No)" for i, q in enumerate(questions)])
    
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
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

config = AgentConfig(
    name="AgentEval",
    description="Evaluates AI agent output quality using deterministic binary checklists. Scores coherence, completeness, conciseness and format.",
    category="tooling",
    tags=["eval", "quality", "scoring", "agents", "llm"],
    entity_url="https://variably-scared-oaf.ngrok-free.dev",
    server_host="0.0.0.0",
    server_port=5000,
    registry_url="https://zns01.zynd.ai",
    price="0.001",
)

agent = ZyndAIAgent(config)

def handle_message(content: str) -> str:
    try:
        data = json.loads(content)
    except:
        data = {}
    
    agent_id = data.get("agent_id", "")
    input_text = data.get("input", "")
    output_text = data.get("output", "")

    card = fetch_agent_card(agent_id)
    agent_desc = card.get("description", "A general purpose AI agent")

    dimension_answers = {}
    for dimension, questions in CHECKLISTS.items():
        answers = run_checklist(dimension, questions, agent_desc, input_text, output_text)
        dimension_answers[dimension] = answers

    breakdown = compute_breakdown(dimension_answers)
    final_score = compute_final_score(breakdown)
    verdict = get_verdict(final_score)

    return json.dumps({
        "agent_id": agent_id,
        "score": final_score,
        "verdict": verdict,
        "breakdown": breakdown
    })

agent.set_custom_agent(handle_message)

if __name__ == "__main__":
    agent.start()
    import time
    while True:
        time.sleep(1)