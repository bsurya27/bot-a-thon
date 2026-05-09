from zyndai_agent.agent import AgentConfig, ZyndAIAgent
from dotenv import load_dotenv
load_dotenv()

config = AgentConfig(
    name='AgentEval',
    description='Evaluates AI agent output quality using deterministic binary checklists.',
    category='tooling',
    tags=['eval', 'quality', 'scoring', 'agents', 'llm'],
    webhook_host='0.0.0.0',
    webhook_port=5000,
    registry_url='https://zns01.zynd.ai',
    price='0.001',
    use_ngrok=True,
)
agent = ZyndAIAgent(config)
print(dir(agent))