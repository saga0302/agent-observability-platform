import json
import anthropic
from dotenv import load_dotenv

load_dotenv()

MODEL = "claude-haiku-4-5-20251001"
client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from the environment

SYSTEM_PROMPT = """You are a strict evaluator of AI agent runs.
You are given a user question, the tool calls the agent made (with inputs and outputs),
and the agent's final answer. Judge the run on three things:

1. correctness_score (0.0 to 1.0): is the final answer correct and does it actually answer the question?
2. hallucination_detected (true/false): does the answer contain claims NOT supported by the tool outputs or common knowledge?
3. tool_usage_score (0.0 to 1.0): were the right tools called, with sensible inputs, and were their outputs used properly?

Respond with ONLY a JSON object, no other text:
{"correctness_score": 0.0, "hallucination_detected": false, "tool_usage_score": 0.0, "feedback": "one or two sentences"}"""


def build_prompt(trace: dict) -> str:
    return (
        f"QUESTION:\n{trace['question']}\n\n"
        f"TOOL CALLS:\n{json.dumps(trace['tool_calls'], indent=2)}\n\n"
        f"AGENT ANSWER:\n{trace['agent_response']}"
    )


def clamp(x: float) -> float:
    return max(0.0, min(1.0, float(x)))


def evaluate_trace(trace: dict) -> dict:
    response = client.messages.create(
        model=MODEL,
        max_tokens=300,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": build_prompt(trace)}],
    )
    text = response.content[0].text.strip()

    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end == -1:
        raise ValueError(f"No JSON in model reply: {text[:200]}")
    result = json.loads(text[start : end + 1])

    return {
        "correctness_score": clamp(result["correctness_score"]),
        "hallucination_detected": bool(result["hallucination_detected"]),
        "tool_usage_score": clamp(result["tool_usage_score"]),
        "claude_feedback": str(result.get("feedback", "")),
    }