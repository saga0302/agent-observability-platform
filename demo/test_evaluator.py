from src.evaluator import evaluate_trace

good = {
    "question": "What is the capital of Japan?",
    "tool_calls": [{"name": "search", "input": "capital of Japan", "output": "Tokyo"}],
    "agent_response": "The capital of Japan is Tokyo.",
}

bad = {
    "question": "What is the capital of Japan?",
    "tool_calls": [{"name": "search", "input": "capital of France", "output": "Paris"}],
    "agent_response": "The capital of Japan is Osaka, founded in 1850.",
}

for name, trace in [("GOOD", good), ("BAD", bad)]:
    print(name, evaluate_trace(trace))