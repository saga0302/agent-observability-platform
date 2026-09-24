from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import uuid

from src.kafka_producer import publish_trace
from src.database import get_recent_traces, get_trace_by_id, get_stats

app = FastAPI(title="Agent Trace Collector")


class TraceInput(BaseModel):
    question: str
    tool_calls: List[Dict[str, Any]]
    agent_response: str


@app.post("/collect")
async def collect_trace(trace: TraceInput):
    trace_id = str(uuid.uuid4())

    publish_trace({
        "trace_id": trace_id,
        "question": trace.question,
        "tool_calls": trace.tool_calls,
        "agent_response": trace.agent_response,
    })

    return {"trace_id": trace_id, "status": "queued"}


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/traces")
async def list_traces(limit: int = 10):
    return get_recent_traces(limit)


@app.get("/traces/{trace_id}")
async def get_trace(trace_id: str):
    trace = get_trace_by_id(trace_id)
    if trace is None:
        raise HTTPException(status_code=404, detail="Trace not found")
    return trace


@app.get("/stats")
async def stats():
    return get_stats()