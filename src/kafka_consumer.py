import json
from kafka import KafkaConsumer

from src.database import insert_trace

BOOTSTRAP_SERVERS = "localhost:9092"
TOPIC = "agent-traces"
GROUP_ID = "storage-writer-group"


def run():
    consumer = KafkaConsumer(
        TOPIC,
        bootstrap_servers=BOOTSTRAP_SERVERS,
        group_id=GROUP_ID,
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        auto_offset_reset="earliest",
    )
    print(f"Listening on '{TOPIC}' as group '{GROUP_ID}'...")
    for message in consumer:
        trace = message.value
        try:
            insert_trace(
                trace_id=trace["trace_id"],
                question=trace["question"],
                tool_calls=trace["tool_calls"],
                agent_response=trace["agent_response"],
            )
            print(f"[SAVED] {trace['trace_id']}")
        except Exception as e:
            print(f"[ERROR] Failed to save {trace.get('trace_id')}: {e}")


if __name__ == "__main__":
    run()