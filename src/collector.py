from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict, Any
import uuid

from src.database import insert_trace
from src.kafka_producer import publish_trace

app = FastAPI(title="Agent Trace Collector")


class TraceInput(BaseModel):
    question: str
    tool_calls: List[Dict[str, Any]]
    agent_response: str


@app.post("/collect")
async def collect_trace(trace: TraceInput):
    trace_id = str(uuid.uuid4())

    insert_trace(
        trace_id=trace_id,
        question=trace.question,
        tool_calls=trace.tool_calls,
        agent_response=trace.agent_response,
    )

    publish_trace({
        "trace_id": trace_id,
        "question": trace.question,
        "tool_calls": trace.tool_calls,
        "agent_response": trace.agent_response,
    })

    return {"trace_id": trace_id, "status": "collected"}


@app.get("/health")
async def health():
    return {"status": "ok"}