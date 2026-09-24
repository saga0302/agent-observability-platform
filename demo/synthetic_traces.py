import random
import time
import requests

COLLECTOR_URL = "http://localhost:8000/collect"

QUESTIONS = [
    "What's the weather in San Francisco?",
    "What are the cheapest flights from LA to NYC?",
    "What are the best-rated restaurants in Seattle?",
    "What's the current price of Bitcoin?",
    "Who won the last Super Bowl?",
]

TOOL_NAMES = ["search", "database_lookup", "calculator", "weather_api", "flights_api"]


def random_tool_calls():
    n = random.randint(1, 3)
    return [
        {
            "name": random.choice(TOOL_NAMES),
            "input": "auto-generated input",
            "output": "auto-generated output",
        }
        for _ in range(n)
    ]


def generate_trace():
    question = random.choice(QUESTIONS)
    return {
        "question": question,
        "tool_calls": random_tool_calls(),
        "agent_response": f"Based on my research, here is the answer to: '{question}'",
    }


def run(count=50):
    sent = 0
    for i in range(count):
        trace = generate_trace()
        resp = requests.post(COLLECTOR_URL, json=trace)
        if resp.status_code == 200:
            sent += 1
            print(f"[{i+1}/{count}] sent -> {resp.json()['trace_id']}")
        else:
            print(f"[{i+1}/{count}] FAILED -> {resp.status_code} {resp.text}")
        time.sleep(0.05)
    print(f"\nDone. {sent}/{count} traces sent successfully.")


if __name__ == "__main__":
    run(50)