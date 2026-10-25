import json
import time
import psycopg2
from kafka import KafkaConsumer

from src.evaluator import evaluate_trace
from src.database import insert_evaluation

BOOTSTRAP_SERVERS = "localhost:9092"
TOPIC = "agent-traces"
GROUP_ID = "evaluator-group"
MAX_RETRIES = 5


def save_with_retry(trace_id, result):
    # The storage consumer may not have saved the trace yet, so wait and retry.
    for _ in range(MAX_RETRIES):
        try:
            insert_evaluation(trace_id=trace_id, **result)
            return True
        except psycopg2.errors.ForeignKeyViolation:
            time.sleep(1)
    return False


def run():
    consumer = KafkaConsumer(
        TOPIC,
        bootstrap_servers=BOOTSTRAP_SERVERS,
        group_id=GROUP_ID,
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        auto_offset_reset="earliest",
    )
    print(f"Evaluator listening on '{TOPIC}' as group '{GROUP_ID}'...")
    for message in consumer:
        trace = message.value
        trace_id = trace["trace_id"]
        try:
            result = evaluate_trace(trace)
            if save_with_retry(trace_id, result):
                print(f"[EVALUATED] {trace_id} correctness={result['correctness_score']}")
            else:
                print(f"[SKIPPED] {trace_id}: trace never appeared in Postgres")
        except Exception as e:
            print(f"[ERROR] {trace_id}: {e}")


if __name__ == "__main__":
    run()