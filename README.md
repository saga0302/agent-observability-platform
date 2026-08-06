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