import os
import psycopg2
from psycopg2.extras import Json

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432"),
    "dbname": os.getenv("DB_NAME", "agent_observability"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "postgres"),
}


def get_connection():
    return psycopg2.connect(**DB_CONFIG)


def insert_trace(trace_id: str, question: str, tool_calls: list, agent_response: str):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO traces (trace_id, question, tool_calls, agent_response)
                VALUES (%s, %s, %s, %s)
                """,
                (trace_id, question, Json(tool_calls), agent_response),
            )
        conn.commit()
    finally:
        conn.close()

def get_recent_traces(limit: int = 10):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT trace_id, question, agent_response, timestamp
                FROM traces
                ORDER BY timestamp DESC
                LIMIT %s
                """,
                (limit,),
            )
            rows = cur.fetchall()
            columns = [desc[0] for desc in cur.description]
            return [dict(zip(columns, row)) for row in rows]
    finally:
        conn.close()


def get_trace_by_id(trace_id: str):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT t.trace_id, t.question, t.tool_calls, t.agent_response, t.timestamp,
                       e.correctness_score, e.hallucination_detected, e.tool_usage_score, e.claude_feedback
                FROM traces t
                LEFT JOIN evaluations e ON t.trace_id = e.trace_id
                WHERE t.trace_id = %s
                """,
                (trace_id,),
            )
            row = cur.fetchone()
            if row is None:
                return None
            columns = [desc[0] for desc in cur.description]
            return dict(zip(columns, row))
    finally:
        conn.close()


def get_stats():
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM traces")
            total_traces = cur.fetchone()[0]

            cur.execute("SELECT AVG(correctness_score) FROM evaluations")
            avg_score = cur.fetchone()[0]

            cur.execute("SELECT COUNT(*) FROM evaluations WHERE hallucination_detected = TRUE")
            hallucination_count = cur.fetchone()[0]

            return {
                "total_traces": total_traces,
                "avg_correctness_score": float(avg_score) if avg_score is not None else None,
                "hallucination_count": hallucination_count,
            }
    finally:
        conn.close()