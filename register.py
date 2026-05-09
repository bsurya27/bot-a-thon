import os
from zyndai_agent.agent import AgentConfig, ZyndAIAgent
from dotenv import load_dotenv

load_dotenv()

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

print(f"✅ Registered! Entity ID: {agent.entity_id}")
print(f"🌐 Card URL: {agent.card_url}")
print(f"📡 Webhook URL: {agent.a2a_url}")
