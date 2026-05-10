# AgentEval 🧪

> "Zynd tells you if an agent is alive and trusted. We tell you if it's actually good."

## What is AgentEval?

AgentEval is a quality evaluation service registered on the Zynd AI network. Any agent on Zynd can call AgentEval to get its output scored before returning it to users — acting as a QA layer for the entire agent ecosystem.

## The Problem

Zynd tracks whether agents are online, trusted, and active. But none of that tells you if the agent's output is actually *good*. An agent can be perfectly healthy and still return incoherent, incomplete, or misleading responses.

AgentEval fills that gap.

## How It Works

1. Any agent sends `{ agent_id, input, output }` to AgentEval
2. AgentEval fetches the agent's card from the Zynd registry
3. Claude runs binary yes/no checklists against the output across 4 dimensions
4. Scores are computed deterministically from the yes/no answers
5. A structured score + verdict is returned

### Why Binary Checklists?

Instead of asking an LLM "how good is this response?" (which gives fuzzy, non-deterministic scores), we ask binary yes/no questions per dimension and compute the score ourselves. Same input always produces the same score.

## Scoring Dimensions

| Dimension | What it measures |
|---|---|
| **Coherence** | Is the response clear, on-topic, and contradiction-free? |
| **Completeness** | Does it fully answer the input? |
| **Conciseness** | Is it appropriately sized with no filler? |
| **Format** | Is it well-structured and readable? |

Each dimension scores 0–10. Final score is the average.

| Score | Verdict |
|---|---|
| ≥ 7.5 | ✅ pass |
| 5.0 – 7.4 | ⚠️ review |
| < 5.0 | ❌ fail |

## Usage

Send a JSON-RPC 2.0 request to the AgentEval A2A endpoint:

```json
{
  "jsonrpc": "2.0",
  "method": "message/send",
  "params": {
    "message": {
      "role": "user",
      "parts": [{
        "kind": "text",
        "text": "{\"agent_id\": \"your-agent-id\", \"input\": \"user question\", \"output\": \"agent response\"}"
      }]
    }
  }
}
```

### Example Response

```json
{
  "agent_id": "your-agent-id",
  "score": 9.5,
  "verdict": "pass",
  "breakdown": {
    "coherence": 10.0,
    "completeness": 10.0,
    "conciseness": 9.0,
    "format": 9.0
  }
}
```

## Zynd Integration

- **Entity ID:** `zns:43c55112d9de01bb9047e0f65a8ba139`
- **Category:** tooling
- **Price:** 0.001 USDC per eval
- **Registry:** zns01.zynd.ai

## Stack

- Python 3.12
- Anthropic Claude (claude-sonnet-4-20250514)
- Zynd AI SDK (`zyndai-agent`)
- Flask

## Project Structure

```
├── eval_agent.py     # main agent server + Zynd registration
├── checklists.py     # binary yes/no questions per dimension
├── scorer.py         # deterministic score computation
├── demo.py           # demo calling the live agent on Zynd
└── .env.example      # environment variables template
```

## Setup

```bash
py -3.12 -m venv venv
venv\Scripts\activate
pip install zyndai-agent anthropic flask python-dotenv requests

# Generate keypair
python keygen.py

# Start the agent
python eval_agent.py
```

Set your `.env`:
```
ANTHROPIC_API_KEY=your_key
ZYND_AGENT_KEYPAIR_PATH=.agent/keypair.json
```

## Vibe Log 🤖

We used Claude (Anthropic) as a development accelerator throughout this build.

### What we designed ourselves
The core architecture was entirely our own thinking:
- The insight that Zynd already covers *behavioral* evals (uptime, trust, freshness)
  but has no *output quality* layer — and that's the gap we fill
- The decision to use **binary yes/no checklists** instead of asking an LLM to 
  score directly — making scores deterministic and reproducible
- Choosing **universal dimensions** (coherence, completeness, conciseness, format) 
  that work across any agent category without domain-specific rubrics
- The service model — registering as a paid Zynd service so any agent on the 
  network can call us per-request

### Where AI accelerated the build
- Generating boilerplate Flask/Zynd SDK integration code
- Debugging SDK internals (AgentConfig fields, handler registration, JSON-RPC format)
- Writing the binary checklist questions per dimension
- Drafting this README

### Key prompt patterns that worked
- Asking Claude to inspect SDK source directly (`inspect.getsource`) when 
  docs were incomplete — this unblocked us multiple times
- Asking "what does this object look like" via `dir()` before assuming field names
- Separating design decisions from implementation — we locked the architecture 
  first, then used AI only for execution

### Honest assessment
The hard thinking — what to build, why it matters, how scoring should work — 
was ours. AI saved us hours of boilerplate and SDK spelunking, letting us ship 
a working Zynd-registered eval service in a single session.