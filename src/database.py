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