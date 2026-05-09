import requests
import json
import uuid

AGENT_URL = "https://variably-scared-oaf.ngrok-free.dev/a2a/v1"

def call_eval_agent(agent_id: str, input_text: str, output_text: str):
    payload = {
        "jsonrpc": "2.0",
        "id": str(uuid.uuid4()),
        "method": "message/send",
        "params": {
            "message": {
                "role": "user",
                "parts": [
                    {
                        "kind": "text",
                        "text": json.dumps({
                            "agent_id": agent_id,
                            "input": input_text,
                            "output": output_text
                        })
                    }
                ],
                "messageId": str(uuid.uuid4())
            }
        }
    }

    response = requests.post(AGENT_URL, json=payload)
    return response.json()

if __name__ == "__main__":
    print("🧪 Test 1: Good output")
    result = call_eval_agent(
        agent_id="test-agent",
        input_text="What are the symptoms of dehydration?",
        output_text="Common symptoms of dehydration include thirst, dark urine, dizziness, fatigue, and dry mouth. Severe dehydration can cause rapid heartbeat and confusion."
    )
    print(json.dumps(result, indent=2))

    print("\n🧪 Test 2: Bad output")
    result = call_eval_agent(
        agent_id="test-agent",
        input_text="What are the symptoms of dehydration?",
        output_text="I dunno maybe drink water sometimes? Could be lots of things honestly."
    )
    print(json.dumps(result, indent=2))