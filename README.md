# Agent Observability Platform

Real-time observability platform for LLM agents. Captures agent execution traces, evaluates reasoning quality with Claude (LLM-as-judge), detects anomalies, and alerts on quality drops.

## Status: Day 1 — Trace Collector

- Kafka + Zookeeper + PostgreSQL running locally via Docker Compose
- FastAPI collector receiving traces at `POST /collect`
- Traces persisted to PostgreSQL and published to Kafka topic `agent-traces`

## Setup

1. `docker compose up -d`
2. `python3.11 -m venv venv && source venv/bin/activate`
3. `pip install -r requirements.txt`
4. Load schema: `docker exec -i agent_observability-postgres-1 psql -U postgres -d agent_observability < schema.sql`
5. `uvicorn src.collector:app --reload`

## Test

```bash
curl -X POST http://localhost:8000/collect \
  -H "Content-Type: application/json" \
  -d '{"question": "...", "tool_calls": [...], "agent_response": "..."}'
```

## Status: Day 2 — Kafka Consumer + Event-Sourced Storage

- Collector (`POST /collect`) now only validates and publishes to Kafka — no direct database write
- `src/kafka_consumer.py` independently consumes `agent-traces` and writes to PostgreSQL
- Chose this design over an initial dual-write approach (collector writing to both Postgres and Kafka directly) specifically to avoid the dual-write consistency problem — if one write fails, the two stores can silently disagree. Kafka is now the single source of truth every downstream service reads from.
- Added `anomalies` and `alerts` tables for future anomaly detection and alerting
- Query API: `GET /traces`, `GET /traces/{trace_id}`, `GET /stats`
- Synthetic trace generator (`demo/synthetic_traces.py`) for load testing without a live agent
- Verified: 50 synthetic traces sent → all 50 flowed through Kafka → all 50 landed in PostgreSQL