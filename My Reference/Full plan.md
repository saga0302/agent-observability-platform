# Real-Time LLM Agent Observability Platform
## Complete Project Specification & Day-by-Day Timeline

**Author:** Sagarika Raju  
**Timeline:** 10 Days (July 15–24, 2026)  
**Target:** Production-ready MVP for portfolio + interviews  
**Total Cost:** $0 development + $0.50–$2 Claude API (one-time demo cost)

---

## PROJECT OVERVIEW

### Problem Statement
AI agents running in production appear to succeed (return response with 200 status) but fail semantically (hallucinate, misuse tools, reason incorrectly). Teams can't detect these failures in real-time, leading to customer dissatisfaction and manual debugging workflows that take hours.

### Solution
A real-time observability platform that:
1. **Captures** every step of an agent's reasoning (trace collection)
2. **Evaluates** whether the reasoning was correct (Claude LLM-as-judge)
3. **Detects** anomalies when quality drops (ML-based baseline detection)
4. **Alerts** teams instantly (Slack notifications)
5. **Debugs** with full context (interactive dashboard)

### Target Audience
- **Hiring:** Anthropic, OpenAI, Databricks, Scale AI, Weights & Biases, Together AI
- **Problem:** Every company with production agents needs this
- **Signal:** Shows you understand production AI infrastructure, not just ML models

---

## TECH STACK & ARCHITECTURE

### Core Technologies
| Layer | Technology | Why | Cost |
|-------|-----------|-----|------|
| Trace Collection | Python + FastAPI | Fast, RESTful, production-grade | Free |
| Real-Time Streaming | Apache Kafka (Docker local) | Event-driven, handles millions/sec | Free (local) |
| Storage | PostgreSQL (Docker local) | Queryable, ACID, standard | Free |
| Evaluation | Claude API (claude-3-5-haiku) | LLM-as-judge, fast + cheap | $0.50–$2 |
| Anomaly Detection | Python + scikit-learn | Baseline + z-score detection | Free |
| Dashboard | Streamlit | Fast iteration, clean UI | Free |
| Demo/Deployment | AWS Lambda + S3 (free tier) | Shows AWS hands-on | Free |

### Architecture Diagram
```
┌─────────────────────────────────────────────────────────────────┐
│                        USER APPLICATION                          │
│                      (LangGraph / Claude)                        │
└──────────────────────────┬──────────────────────────────────────┘
                           │ Agent executes
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│              TRACE COLLECTOR (FastAPI)                           │
│  - Receives trace (question, tool calls, answer)               │
│  - Stores in PostgreSQL                                        │
│  - Pushes to Kafka topic                                       │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    KAFKA STREAM                                  │
│  - Real-time event flow                                        │
│  - Decouples collectors from processors                        │
│  - Enables scaling                                             │
└──────────────────────────┬──────────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        ▼                  ▼                  ▼
┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
│  EVALUATOR       │ │ ANOMALY DETECTOR │ │ AGGREGATOR       │
│  (Claude API)    │ │ (ML baseline)    │ │ (Dashboarding)   │
│                  │ │                  │ │                  │
│ Scores trace:    │ │ Detects when     │ │ Groups similar   │
│ - Correctness    │ │ quality drops    │ │ failures         │
│ - Hallucination  │ │ - z-score > 2    │ │ - Trends         │
│ - Tool usage     │ │ - Baseline drift │ │ - Patterns       │
└──────────────────┘ └──────────────────┘ └──────────────────┘
        │                  │                  │
        └──────────────────┼──────────────────┘
                           ▼
        ┌──────────────────────────────────┐
        │   RESULTS STORE (PostgreSQL)     │
        │  - Traces + scores + flags       │
        └──────────────────────────────────┘
                           │
                           ▼
        ┌──────────────────────────────────┐
        │  ALERT SYSTEM (Slack webhook)    │
        │  "⚠️ Agent quality dropped 30%"  │
        └──────────────────────────────────┘
                           │
                           ▼
        ┌──────────────────────────────────┐
        │  STREAMLIT DASHBOARD             │
        │  - View traces + scores          │
        │  - Drill into failures           │
        │  - See trends over time          │
        └──────────────────────────────────┘
```

### Directory Structure
```
agent-observability/
├── README.md                          # Project overview + setup
├── docker-compose.yml                 # Kafka + PostgreSQL
├── requirements.txt                   # Python dependencies
│
├── src/
│   ├── collector.py                   # FastAPI trace collector
│   ├── kafka_producer.py              # Push traces to Kafka
│   ├── kafka_consumer.py              # Consume from Kafka
│   ├── evaluator.py                   # Claude API scoring
│   ├── anomaly_detector.py            # ML baseline + z-score
│   ├── database.py                    # PostgreSQL schema + queries
│   └── utils.py                       # Helpers (logging, etc)
│
├── dashboard/
│   └── streamlit_app.py               # Streamlit UI
│
├── demo/
│   ├── synthetic_traces.py            # Generate fake agent traces
│   ├── example_agent.py               # Simple LangGraph agent
│   └── demo_data.json                 # Pre-generated traces
│
├── tests/
│   ├── test_collector.py
│   ├── test_evaluator.py
│   └── test_anomaly_detector.py
│
├── docs/
│   ├── ARCHITECTURE.md                # Technical deep dive
│   ├── SETUP.md                       # Installation guide
│   └── API.md                         # Collector API spec
│
└── .github/
    └── workflows/
        └── ci.yml                     # GitHub Actions (pytest)
```

---

## TIMELINE: DAY-BY-DAY BREAKDOWN

### DAY 1: SETUP + TRACE COLLECTOR (4–5 hours)

**Objective:** Local environment working, trace collection API running

**Deliverables:**
- Docker setup (Kafka + PostgreSQL running)
- FastAPI trace collector receiving traces
- PostgreSQL schema for traces
- First trace stored successfully

**Tasks:**

1. **Environment Setup (30 min)**
   - Clone repo template (or create from scratch)
   - `pip install -r requirements.txt` (fastapi, psycopg2, pydantic, kafka-python)
   - Verify Python 3.10+

2. **Docker Compose (45 min)**
   - Create `docker-compose.yml` with:
     - Kafka broker (image: confluentinc/cp-kafka:latest)
     - Zookeeper (dependency for Kafka)
     - PostgreSQL (image: postgres:15)
   - Run: `docker-compose up -d`
   - Verify containers running: `docker ps`

3. **PostgreSQL Schema (45 min)**
   - Connect to Postgres: `psql -U postgres -h localhost`
   - Create schema:
     ```sql
     CREATE TABLE traces (
       id SERIAL PRIMARY KEY,
       trace_id UUID UNIQUE NOT NULL,
       question TEXT NOT NULL,
       tool_calls JSONB NOT NULL,
       agent_response TEXT NOT NULL,
       timestamp TIMESTAMP DEFAULT NOW(),
       created_at TIMESTAMP DEFAULT NOW()
     );
     
     CREATE TABLE evaluations (
       id SERIAL PRIMARY KEY,
       trace_id UUID UNIQUE NOT NULL REFERENCES traces(trace_id),
       correctness_score FLOAT,
       hallucination_detected BOOLEAN,
       tool_usage_score FLOAT,
       claude_feedback TEXT,
       evaluated_at TIMESTAMP DEFAULT NOW(),
       FOREIGN KEY(trace_id) REFERENCES traces(trace_id)
     );
     
     CREATE INDEX idx_trace_timestamp ON traces(timestamp);
     CREATE INDEX idx_eval_score ON evaluations(correctness_score);
     ```

4. **FastAPI Collector (90 min)**
   - Create `src/collector.py`:
     ```python
     from fastapi import FastAPI, HTTPException
     from pydantic import BaseModel
     import psycopg2
     from datetime import datetime
     import uuid
     
     app = FastAPI(title="Agent Trace Collector")
     
     class TraceInput(BaseModel):
         question: str
         tool_calls: list  # [{name: "search", input: "...", output: "..."}]
         agent_response: str
     
     @app.post("/collect")
     async def collect_trace(trace: TraceInput):
         trace_id = str(uuid.uuid4())
         # Store in PostgreSQL
         # Push to Kafka
         return {"trace_id": trace_id, "status": "collected"}
     
     @app.get("/health")
     async def health():
         return {"status": "ok"}
     ```
   - Test locally: `uvicorn src.collector:app --reload`
   - Send test trace via curl or Python requests

5. **Kafka Producer (60 min)**
   - Create `src/kafka_producer.py` to push traces to Kafka topic "agent-traces"
   - Test: trace stored in DB → pushed to Kafka topic

**Validation Checklist:**
- ✅ Docker containers running
- ✅ FastAPI running on `localhost:8000`
- ✅ POST `/collect` receives trace and returns trace_id
- ✅ Trace appears in PostgreSQL `traces` table
- ✅ Trace published to Kafka (verify with `kafka-console-consumer`)
- ✅ README updated with setup steps

**End-of-Day Commit:**
```
git add .
git commit -m "Day 1: Setup, Kafka/PostgreSQL, trace collector API"
git push
```

---

### DAY 2: KAFKA CONSUMER + STORAGE (4–5 hours)

**Objective:** Traces flowing end-to-end, persisted to database with retrieval API

**Deliverables:**
- Kafka consumer consuming traces
- Results store (evaluation + anomaly tables)
- Simple query API to fetch traces + scores
- Test with synthetic traces

**Tasks:**

1. **Kafka Consumer (60 min)**
   - Create `src/kafka_consumer.py`:
     ```python
     from kafka import KafkaConsumer
     import json
     
     consumer = KafkaConsumer(
         'agent-traces',
         bootstrap_servers=['localhost:9092'],
         group_id='evaluator-group',
         value_deserializer=lambda m: json.loads(m.decode('utf-8'))
     )
     
     for message in consumer:
         trace = message.value
         print(f"Consuming trace: {trace['trace_id']}")
         # Pass to evaluator
     ```
   - Run as background process

2. **Results Storage Schema (45 min)**
   - Add more tables:
     ```sql
     CREATE TABLE anomalies (
       id SERIAL PRIMARY KEY,
       trace_id UUID REFERENCES traces(trace_id),
       anomaly_type VARCHAR(50),  -- 'hallucination', 'tool_misuse', 'drift'
       z_score FLOAT,
       flagged_at TIMESTAMP DEFAULT NOW()
     );
     
     CREATE TABLE alerts (
       id SERIAL PRIMARY KEY,
       trace_id UUID REFERENCES traces(trace_id),
       message TEXT,
       severity VARCHAR(20),  -- 'warning', 'critical'
       created_at TIMESTAMP DEFAULT NOW()
     );
     ```

3. **Synthetic Trace Generator (90 min)**
   - Create `demo/synthetic_traces.py`:
     ```python
     import json
     import random
     from datetime import datetime
     
     def generate_traces(count=100):
         traces = []
         for _ in range(count):
             trace = {
                 "question": random.choice([
                     "What's the weather in SF?",
                     "Cheapest flights LA to NYC?",
                     "Best restaurants in SF?"
                 ]),
                 "tool_calls": [
                     {"name": "search", "output": "..."},
                     {"name": "database", "output": "..."}
                 ],
                 "agent_response": "Based on my search, ..."
             }
             traces.append(trace)
         return traces
     ```
   - Generate 100 sample traces
   - POST to collector in a loop

4. **Query API (60 min)**
   - Extend `src/collector.py`:
     ```python
     @app.get("/traces")
     async def list_traces(limit: int = 10):
         # Query PostgreSQL, return recent traces
         pass
     
     @app.get("/traces/{trace_id}")
     async def get_trace(trace_id: str):
         # Return trace + evaluation + anomalies
         pass
     
     @app.get("/stats")
     async def get_stats():
         # Return avg score, hallucination rate, etc
         pass
     ```

5. **Integration Test (45 min)**
   - Generate 50 synthetic traces
   - POST all to collector
   - Verify all land in PostgreSQL
   - Query `/stats` and confirm counts

**Validation Checklist:**
- ✅ Kafka consumer running, consuming traces
- ✅ Synthetic traces generated (50+)
- ✅ All traces in `traces` table
- ✅ `/traces` endpoint returns list
- ✅ `/traces/{trace_id}` returns single trace
- ✅ `/stats` shows correct counts (traces: 50+)
- ✅ Can filter by timestamp

**End-of-Day Commit:**
```
git commit -m "Day 2: Kafka consumer, results storage schema, query API, synthetic traces"
git push
```

---

### DAY 3: CLAUDE EVALUATOR (5–6 hours)

**Objective:** Claude scoring traces, results stored, evaluation working end-to-end

**Deliverables:**
- Claude API integration
- Automated scoring of traces
- Evaluation results stored
- Batch evaluation working

**Tasks:**

1. **Claude Evaluator Setup (90 min)**
   - Create `src/evaluator.py`:
     ```python
     import anthropic
     import json
     
     client = anthropic.Anthropic()
     
     EVALUATOR_PROMPT = """
     You are an expert evaluator of AI agent reasoning. 
     Evaluate the following agent trace on these criteria:
     
     1. Correctness: Did the agent answer correctly? (0-1)
     2. Hallucination: Did the agent make up facts? (0-1, 0=hallucinating, 1=grounded)
     3. Tool Usage: Did the agent use tools correctly? (0-1)
     4. Reasoning: Was the reasoning clear and logical? (0-1)
     
     Provide a JSON response:
     {
       "correctness_score": 0.95,
       "hallucination_score": 0.9,
       "tool_usage_score": 0.85,
       "reasoning_score": 0.92,
       "overall_score": 0.91,
       "feedback": "..."
     }
     
     Trace:
     Question: {question}
     Tools called: {tools}
     Agent response: {response}
     """
     
     def evaluate_trace(trace):
         prompt = EVALUATOR_PROMPT.format(
             question=trace['question'],
             tools=json.dumps(trace['tool_calls']),
             response=trace['agent_response']
         )
         
         message = client.messages.create(
             model="claude-3-5-haiku-20241022",
             max_tokens=500,
             messages=[{"role": "user", "content": prompt}]
         )
         
         # Parse response, store in DB
         return json.loads(message.content[0].text)
     ```

2. **Batch Evaluation Worker (90 min)**
   - Create `src/evaluator_worker.py` to consume from Kafka:
     ```python
     from kafka import KafkaConsumer
     from evaluator import evaluate_trace
     import psycopg2
     
     consumer = KafkaConsumer('agent-traces', ...)
     
     for message in consumer:
         trace = message.value
         
         # Evaluate
         scores = evaluate_trace(trace)
         
         # Store in PostgreSQL
         conn = psycopg2.connect(...)
         cursor = conn.cursor()
         cursor.execute(
             """INSERT INTO evaluations 
             (trace_id, correctness_score, hallucination_detected, tool_usage_score, claude_feedback)
             VALUES (%s, %s, %s, %s, %s)""",
             (trace['trace_id'], scores['correctness_score'], ...)
         )
         conn.commit()
     ```
   - Run as background worker

3. **Prompt Caching for Cost (45 min)**
   - Leverage Claude's prompt caching to reduce API calls:
     ```python
     message = client.messages.create(
         model="claude-3-5-haiku-20241022",
         max_tokens=500,
         system=[{
             "type": "text",
             "text": EVALUATOR_PROMPT,
             "cache_control": {"type": "ephemeral"}
         }],
         messages=[...]
     )
     ```
   - This caches the system prompt, saves 90% on repeated evals

4. **Batch Evaluation Script (60 min)**
   - Create `demo/batch_evaluate.py`:
     ```python
     from src.evaluator import evaluate_trace
     from src.database import get_unevaluated_traces, store_evaluation
     
     traces = get_unevaluated_traces()  # Get traces without scores
     
     for trace in traces:
         scores = evaluate_trace(trace)
         store_evaluation(trace['trace_id'], scores)
         print(f"Evaluated {trace['trace_id']}: {scores['overall_score']}")
     ```
   - Run: `python demo/batch_evaluate.py`

5. **API Endpoint for Scores (45 min)**
   - Add to collector:
     ```python
     @app.get("/evaluations/{trace_id}")
     async def get_evaluation(trace_id: str):
         # Return evaluation scores
         pass
     
     @app.get("/evaluations/batch")
     async def batch_evaluate(limit: int = 50):
         # Evaluate next 50 unevaluated traces
         pass
     ```

**Validation Checklist:**
- ✅ Claude API key configured (`ANTHROPIC_API_KEY` env var)
- ✅ Evaluator worker running
- ✅ Trace POST → Kafka push → Claude eval → DB store (end-to-end)
- ✅ `/evaluations/{trace_id}` returns scores
- ✅ Can retrieve overall_score, feedback
- ✅ Batch evaluation on 50 traces completes in < 5 min (with caching)
- ✅ Cost ~$0.50 for 100 evaluations (Haiku is cheap)

**End-of-Day Commit:**
```
git commit -m "Day 3: Claude evaluator, batch evaluation, prompt caching, scores stored"
git push
```

---

### DAY 4: ANOMALY DETECTION (4–5 hours)

**Objective:** Baseline detection working, anomalies flagged, quality drift detected

**Deliverables:**
- Baseline score calculation
- Anomaly detection (z-score > 2)
- Quality drift detection
- Alerts system functional

**Tasks:**

1. **Baseline Score Calculator (60 min)**
   - Create `src/anomaly_detector.py`:
     ```python
     import numpy as np
     from src.database import get_evaluations
     
     def calculate_baseline(window_size=100):
         """Calculate baseline score from recent evaluations"""
         evals = get_evaluations(limit=window_size)
         scores = [e['correctness_score'] for e in evals]
         
         return {
             'mean': np.mean(scores),
             'std': np.std(scores),
             'min': np.min(scores),
             'max': np.max(scores),
             'count': len(scores)
         }
     ```

2. **Z-Score Anomaly Detection (75 min)**
   - Add to anomaly_detector:
     ```python
     def detect_anomalies(baseline, new_score):
         """
         z_score = (x - mean) / std
         If z_score < -2, flag as anomaly (score 2 std below mean)
         """
         z_score = (new_score - baseline['mean']) / baseline['std']
         
         is_anomaly = z_score < -2  # More than 2 std below
         
         return {
             'z_score': z_score,
             'is_anomaly': is_anomaly,
             'severity': 'critical' if z_score < -3 else 'warning'
         }
     ```

3. **Quality Drift Detector (75 min)**
   - Detect when baseline itself is shifting (sign of systemic issue):
     ```python
     def detect_drift(baseline_t0, baseline_t1):
         """
         Compare baseline over two windows.
         If mean dropped >15%, flag as drift.
         """
         drift = (baseline_t0['mean'] - baseline_t1['mean']) / baseline_t0['mean']
         
         return {
             'drift_pct': drift * 100,
             'is_drifting': drift > 0.15,  # 15% drop
             'trend': 'degrading' if drift > 0 else 'improving'
         }
     ```

4. **Alert System (60 min)**
   - Create `src/alerter.py`:
     ```python
     import requests
     
     def send_slack_alert(message, severity='warning'):
         """Send alert to Slack webhook"""
         webhook_url = os.getenv('SLACK_WEBHOOK_URL')
         
         color = '#ff0000' if severity == 'critical' else '#ffaa00'
         
         payload = {
             "attachments": [{
                 "color": color,
                 "title": f"Agent Quality Alert ({severity.upper()})",
                 "text": message,
                 "ts": int(time.time())
             }]
         }
         
         requests.post(webhook_url, json=payload)
     ```
   - (Optional: print to console for testing, Slack webhook for production)

5. **Detector Worker (60 min)**
   - Create worker that runs baseline + anomaly detection:
     ```python
     from src.anomaly_detector import calculate_baseline, detect_anomalies
     from src.alerter import send_slack_alert
     
     # Every 5 minutes:
     baseline = calculate_baseline(window_size=100)
     recent_evals = get_recent_evaluations(limit=10)
     
     for eval in recent_evals:
         anomaly = detect_anomalies(baseline, eval['correctness_score'])
         
         if anomaly['is_anomaly']:
             send_slack_alert(
                 f"⚠️ Trace {eval['trace_id']} scored {eval['correctness_score']:.2f} (z={anomaly['z_score']:.2f})",
                 severity=anomaly['severity']
             )
             # Store anomaly record
     ```

6. **Dashboard Stats API (45 min)**
   - Add endpoints:
     ```python
     @app.get("/metrics")
     async def get_metrics():
         return {
             'baseline': calculate_baseline(),
             'trend': detect_drift(...),
             'recent_anomalies': get_anomalies(limit=10),
             'overall_health': 'ok' if baseline_is_stable else 'degraded'
         }
     ```

**Validation Checklist:**
- ✅ Baseline calculated from 100 evals
- ✅ Z-score computed for new evals
- ✅ Anomalies detected (z < -2)
- ✅ Drift detection working (baseline trend)
- ✅ Alerts triggered for anomalies
- ✅ `/metrics` returns baseline + trend + anomalies
- ✅ Alert message includes trace_id, score, z_score

**End-of-Day Commit:**
```
git commit -m "Day 4: Anomaly detection, z-score, drift detection, alerting system"
git push
```

---

### DAY 5: STREAMLIT DASHBOARD (5–6 hours)

**Objective:** Interactive dashboard showing traces, scores, trends, anomalies

**Deliverables:**
- Streamlit app running locally
- Trace list with drill-down
- Score trends over time
- Anomaly visualization
- Real-time updates

**Tasks:**

1. **Basic Streamlit App (90 min)**
   - Create `dashboard/streamlit_app.py`:
     ```python
     import streamlit as st
     import pandas as pd
     from src.database import (
         get_recent_traces, 
         get_evaluation, 
         calculate_baseline,
         get_anomalies
     )
     
     st.set_page_config(page_title="Agent Observability", layout="wide")
     
     st.title("🤖 Real-Time Agent Observability")
     st.subheader("Monitor, Evaluate, Debug")
     
     # Metrics row
     col1, col2, col3, col4 = st.columns(4)
     
     baseline = calculate_baseline()
     
     col1.metric("Avg Score", f"{baseline['mean']:.2f}", "baseline")
     col2.metric("Total Traces", baseline['count'])
     col3.metric("Anomalies", len(get_anomalies()), "last hour")
     col4.metric("Health", "Normal", "✅")
     ```

2. **Recent Traces Table (75 min)**
   - Add to dashboard:
     ```python
     st.subheader("Recent Traces")
     
     traces_df = pd.DataFrame(get_recent_traces(limit=20))
     traces_df['evaluation'] = traces_df['trace_id'].apply(
         lambda tid: get_evaluation(tid)
     )
     traces_df['score'] = traces_df['evaluation'].apply(
         lambda e: e['correctness_score'] if e else None
     )
     
     st.dataframe(
         traces_df[['trace_id', 'question', 'score', 'timestamp']],
         use_container_width=True
     )
     ```

3. **Drill-Down Detail View (75 min)**
   - Add expandable trace details:
     ```python
     selected_trace_id = st.selectbox("View trace details", traces_df['trace_id'])
     
     if selected_trace_id:
         trace = get_trace(selected_trace_id)
         eval = get_evaluation(selected_trace_id)
         
         st.write(f"**Question:** {trace['question']}")
         st.write(f"**Response:** {trace['agent_response']}")
         
         col1, col2, col3, col4 = st.columns(4)
         col1.metric("Correctness", f"{eval['correctness_score']:.2f}")
         col2.metric("Hallucination", f"{eval['hallucination_score']:.2f}")
         col3.metric("Tool Usage", f"{eval['tool_usage_score']:.2f}")
         col4.metric("Reasoning", f"{eval['reasoning_score']:.2f}")
         
         st.write("**Tool Calls:**")
         st.json(trace['tool_calls'])
         
         st.write("**Claude Feedback:**")
         st.write(eval['claude_feedback'])
     ```

4. **Score Trends Chart (75 min)**
   - Add time-series visualization:
     ```python
     import plotly.express as px
     
     st.subheader("Score Trends")
     
     trend_data = pd.DataFrame(get_evaluations(limit=100))
     trend_data['timestamp'] = pd.to_datetime(trend_data['timestamp'])
     
     fig = px.line(
         trend_data,
         x='timestamp',
         y='correctness_score',
         title="Correctness Score Over Time",
         labels={'correctness_score': 'Score', 'timestamp': 'Time'}
     )
     fig.add_hline(y=calculate_baseline()['mean'], line_dash="dash", 
                   annotation_text="Baseline")
     
     st.plotly_chart(fig, use_container_width=True)
     ```

5. **Anomaly Visualization (75 min)**
   - Show flagged anomalies:
     ```python
     st.subheader("Flagged Anomalies")
     
     anomalies = get_anomalies(limit=20)
     
     if anomalies:
         anomaly_df = pd.DataFrame(anomalies)
         
         fig = px.scatter(
             anomaly_df,
             x='flagged_at',
             y='z_score',
             color='anomaly_type',
             size='z_score',
             hover_data=['trace_id']
         )
         fig.add_hline(y=-2, line_dash="dash", line_color="red",
                       annotation_text="Anomaly threshold")
         
         st.plotly_chart(fig, use_container_width=True)
     else:
         st.info("No anomalies detected in the last hour.")
     ```

6. **Run & Deploy (30 min)**
   - Test locally: `streamlit run dashboard/streamlit_app.py`
   - Should open on `localhost:8501`
   - Verify all components render without errors

**Validation Checklist:**
- ✅ Streamlit app runs: `streamlit run dashboard/streamlit_app.py`
- ✅ Metrics display (avg score, count, anomalies)
- ✅ Recent traces table shows data
- ✅ Drill-down view shows full trace details
- ✅ Score trends chart plots correctly
- ✅ Anomaly scatter plot shows flagged traces
- ✅ All queries execute <2 sec

**End-of-Day Commit:**
```
git commit -m "Day 5: Streamlit dashboard, traces table, drill-down, trends chart, anomalies"
git push
```

---

### DAY 6: DEMO DATA + INTEGRATION TEST (4–5 hours)

**Objective:** End-to-end system working with realistic synthetic traces, ready for portfolio

**Deliverables:**
- 500+ synthetic traces pre-generated
- Full pipeline tested (collect → evaluate → detect → dashboard)
- Dashboard showing real data flow
- Demo script ready for interviews

**Tasks:**

1. **Enhance Synthetic Trace Generator (90 min)**
   - Update `demo/synthetic_traces.py` to create realistic traces:
     ```python
     import random
     import json
     from datetime import datetime, timedelta
     
     def generate_realistic_traces(count=500):
         questions = [
             "What's the weather in San Francisco?",
             "Cheapest flights from LA to NYC next week?",
             "Best Italian restaurants in SF?",
             "What's Tesla's stock price?",
             "How to make pasta carbonara?",
             "Who won the World Cup 2022?"
         ]
         
         tools_used = [
             ['search', 'ranking'],
             ['weather_api', 'cache'],
             ['flight_api', 'price_comparison'],
             ['restaurant_db', 'review_aggregator'],
             ['stock_api'],
             ['knowledge_base']
         ]
         
         traces = []
         now = datetime.now()
         
         for i in range(count):
             # Some traces are great (score 0.9+)
             # Some have issues (score 0.3-0.7)
             # A few hallucinate (score 0.0-0.3)
             
             quality_bucket = random.choices(
                 ['excellent', 'good', 'poor', 'hallucinating'],
                 weights=[60, 25, 10, 5]
             )[0]
             
             response = {
                 'excellent': "Based on my search, the answer is X with supporting details.",
                 'good': "According to my search results, X (with minor inaccuracies)",
                 'poor': "X is probably Y (actually uncertain)",
                 'hallucinating': "According to my knowledge, X is Z (completely made up)"
             }[quality_bucket]
             
             trace = {
                 "question": random.choice(questions),
                 "tool_calls": random.choice(tools_used),
                 "agent_response": response,
                 "timestamp": (now - timedelta(minutes=random.randint(0, 1440))).isoformat()
             }
             
             traces.append(trace)
         
         return traces
     ```

2. **Batch Ingestion Script (75 min)**
   - Create `demo/ingest_demo_data.py`:
     ```python
     import requests
     import time
     from demo.synthetic_traces import generate_realistic_traces
     
     traces = generate_realistic_traces(count=500)
     
     print(f"Ingesting {len(traces)} synthetic traces...")
     
     for i, trace in enumerate(traces):
         try:
             response = requests.post(
                 "http://localhost:8000/collect",
                 json=trace,
                 timeout=5
             )
             
             if response.status_code == 200:
                 print(f"✓ Trace {i+1}/{len(traces)}")
             else:
                 print(f"✗ Failed: {response.text}")
         
         except Exception as e:
             print(f"✗ Error: {e}")
         
         # Small delay to avoid overwhelming
         if (i + 1) % 50 == 0:
             time.sleep(1)
     
     print("Ingestion complete!")
     ```

3. **Full Pipeline Test (90 min)**
   - Create `demo/run_full_pipeline.sh`:
     ```bash
     #!/bin/bash
     
     echo "Starting Docker containers..."
     docker-compose up -d
     sleep 10
     
     echo "Starting trace collector..."
     python -m uvicorn src.collector:app --host 0.0.0.0 --port 8000 &
     sleep 5
     
     echo "Starting Kafka consumer..."
     python src/kafka_consumer.py &
     sleep 5
     
     echo "Starting evaluator worker..."
     python src/evaluator_worker.py &
     sleep 5
     
     echo "Starting anomaly detector..."
     python src/anomaly_detector_worker.py &
     sleep 5
     
     echo "Ingesting demo data..."
     python demo/ingest_demo_data.py
     
     sleep 10
     
     echo "Launching dashboard..."
     streamlit run dashboard/streamlit_app.py
     ```

4. **End-to-End Validation (60 min)**
   - Checklist:
     ```
     ✅ Run: bash demo/run_full_pipeline.sh
     ✅ 500 traces ingested
     ✅ All traces appear in /traces endpoint
     ✅ Evaluator scores all traces (5-10 min)
     ✅ /evaluations returns scores
     ✅ Baseline calculated
     ✅ Anomalies detected (some low-quality traces flagged)
     ✅ Dashboard loads all data
     ✅ Charts render correctly
     ✅ No errors in logs
     ```

5. **Demo Walkthrough Script (45 min)**
   - Create `demo/DEMO_WALKTHROUGH.md`:
     ```markdown
     # Demo Walkthrough (5 minutes)
     
     ## Setup (30 sec)
     1. Run pipeline: `bash demo/run_full_pipeline.sh`
     2. Wait for "Launching dashboard..."
     3. Open browser: http://localhost:8501
     
     ## Show Metrics (30 sec)
     - Point to metrics: "Avg score 0.72, 500 traces, 47 anomalies"
     - Explain: "Baseline calculated from 100 most recent"
     
     ## Show Recent Traces (1 min)
     - Scroll through table
     - Point out: "These are real-time traces from synthetic agents"
     - Explain: "Each row is one agent execution"
     
     ## Drill into Poor Trace (1.5 min)
     - Click on low-score trace (z_score < -2)
     - Show: question, tools called, response
     - Show Claude's evaluation: "Correctness 0.35 - Hallucinating"
     - Explain: "Claude LLM-as-judge caught the hallucination"
     
     ## Show Trends (1 min)
     - Scroll to "Score Trends" chart
     - Point to baseline (dashed line)
     - Explain: "This shows quality drift over time"
     
     ## Show Anomalies (1 min)
     - Scroll to anomaly scatter plot
     - Explain: "Red zone = z < -2, flagged traces"
     - Point to outliers: "These are the failures our system caught"
     ```

**Validation Checklist:**
- ✅ 500+ synthetic traces generated
- ✅ All traces ingested successfully
- ✅ Evaluator completes all evals (should take ~8-10 min with batching)
- ✅ Dashboard displays all metrics, tables, charts
- ✅ No SQL errors or API timeouts
- ✅ Anomalies correctly flagged (low-quality traces)
- ✅ Demo script runnable in one command

**End-of-Day Commit:**
```
git commit -m "Day 6: Synthetic data generation, batch ingestion, end-to-end test, demo script"
git push
```

---

### DAY 7: POLISH + AWS DEMO (4–5 hours)

**Objective:** Production-ready code, AWS deployment showcase, polished for portfolio

**Deliverables:**
- Clean, documented code
- AWS Lambda demo (evaluator on Lambda)
- Traces in S3
- Professional README
- GitHub Actions CI passing

**Tasks:**

1. **Code Polish (90 min)**
   - Add docstrings to all functions:
     ```python
     def evaluate_trace(trace: dict) -> dict:
         """
         Evaluate a single trace using Claude LLM-as-judge.
         
         Args:
             trace (dict): Trace with 'question', 'tool_calls', 'agent_response'
         
         Returns:
             dict: Scores and feedback from Claude
         
         Raises:
             ValueError: If trace missing required fields
         """
     ```
   - Add type hints everywhere
   - Add error handling:
     ```python
     try:
         # ... code ...
     except psycopg2.OperationalError as e:
         logger.error(f"Database error: {e}")
         raise
     except anthropic.APIError as e:
         logger.error(f"Claude API error: {e}")
         raise
     ```
   - Add logging:
     ```python
     import logging
     logger = logging.getLogger(__name__)
     logger.info(f"Collected trace {trace_id}")
     ```

2. **AWS Lambda Demo (120 min)**
   - Create `aws/lambda_evaluator.py`:
     ```python
     import json
     import os
     from src.evaluator import evaluate_trace
     import boto3
     
     s3 = boto3.client('s3')
     
     def lambda_handler(event, context):
         """
         AWS Lambda handler for evaluating traces from S3.
         
         Reads trace from S3 bucket, evaluates with Claude,
         stores result back to S3.
         """
         
         bucket = event['Records'][0]['s3']['bucket']['name']
         key = event['Records'][0]['s3']['object']['key']
         
         # Read trace
         response = s3.get_object(Bucket=bucket, Key=key)
         trace = json.loads(response['Body'].read())
         
         # Evaluate
         scores = evaluate_trace(trace)
         
         # Store result
         result_key = f"evaluations/{trace['trace_id']}.json"
         s3.put_object(
             Bucket=bucket,
             Key=result_key,
             Body=json.dumps(scores)
         )
         
         return {
             'statusCode': 200,
             'body': json.dumps(scores)
         }
     ```
   - Create `aws/serverless.yml`:
     ```yaml
     service: agent-observability-lambda
     
     provider:
       name: aws
       runtime: python3.11
       region: us-east-1
     
     functions:
       evaluator:
         handler: aws/lambda_evaluator.lambda_handler
         events:
           - s3:
               bucket: agent-traces
               event: s3:ObjectCreated:*
               rules:
                 - prefix: traces/
     ```

3. **GitHub Actions CI (60 min)**
   - Create `.github/workflows/ci.yml`:
     ```yaml
     name: Tests
     
     on: [push, pull_request]
     
     jobs:
       test:
         runs-on: ubuntu-latest
         
         services:
           postgres:
             image: postgres:15
             env:
               POSTGRES_PASSWORD: postgres
             options: >-
               --health-cmd pg_isready
               --health-interval 10s
               --health-timeout 5s
               --health-retries 5
         
         steps:
           - uses: actions/checkout@v2
           - uses: actions/setup-python@v2
             with:
               python-version: '3.11'
           
           - name: Install dependencies
             run: pip install -r requirements.txt
           
           - name: Run tests
             run: pytest tests/ -v
     ```

4. **Comprehensive README (90 min)**
   - Update `README.md`:
     ```markdown
     # Real-Time LLM Agent Observability Platform
     
     ![Tests](https://github.com/saga0302/agent-observability/workflows/Tests/badge.svg)
     ![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue)
     
     ## Overview
     
     Open-source observability platform for AI agents. Detects semantic failures 
     (hallucinations, tool misuse, reasoning drift) in real-time using streaming 
     architecture + Claude LLM-as-judge evaluation.
     
     **Problem:** AI agents appear to succeed (200 status) but fail semantically 
     (hallucinate, misuse tools). Teams can't detect this until customers complain.
     
     **Solution:** Capture execution traces → Stream via Kafka → Evaluate with Claude → 
     Detect anomalies → Alert team instantly → Debug with full context.
     
     ## Key Features
     
     - **Real-time Trace Collection**: FastAPI endpoint captures every step of agent execution
     - **Streaming Pipeline**: Kafka-based event streaming for scalability
     - **LLM-as-Judge Evaluation**: Claude scores correctness, hallucination, tool usage
     - **Anomaly Detection**: ML-based baseline + z-score detection
     - **Interactive Dashboard**: Streamlit UI for trace exploration + trend analysis
     - **AWS Ready**: Lambda + S3 integration for cloud deployment
     
     ## Architecture
     
     ```
     Agent Execution
         ↓
     FastAPI Collector (port 8000)
         ↓
     Kafka Stream (localhost:9092)
         ↓
     Claude Evaluator (LLM-as-judge)
         ↓
     Anomaly Detector (baseline + z-score)
         ↓
     PostgreSQL Results (localhost:5432)
         ↓
     Streamlit Dashboard (port 8501)
     ```
     
     ## Quick Start
     
     ### Prerequisites
     - Docker + Docker Compose
     - Python 3.11+
     - `ANTHROPIC_API_KEY` env var
     
     ### Setup
     
     ```bash
     # Clone repo
     git clone https://github.com/saga0302/agent-observability.git
     cd agent-observability
     
     # Install dependencies
     pip install -r requirements.txt
     
     # Start Docker containers (Kafka + PostgreSQL)
     docker-compose up -d
     
     # Run full pipeline
     bash demo/run_full_pipeline.sh
     
     # Dashboard opens automatically on localhost:8501
     ```
     
     ### Manual Steps
     
     ```bash
     # Terminal 1: Start collector API
     uvicorn src.collector:app --reload
     
     # Terminal 2: Start Kafka consumer
     python src/kafka_consumer.py
     
     # Terminal 3: Start evaluator worker
     python src/evaluator_worker.py
     
     # Terminal 4: Start anomaly detector
     python src/anomaly_detector_worker.py
     
     # Terminal 5: Start dashboard
     streamlit run dashboard/streamlit_app.py
     
     # Terminal 6: Ingest demo data
     python demo/ingest_demo_data.py
     ```
     
     ## API Endpoints
     
     - `POST /collect` - Submit trace
     - `GET /traces` - List recent traces
     - `GET /traces/{trace_id}` - Get single trace
     - `GET /evaluations/{trace_id}` - Get evaluation scores
     - `GET /metrics` - System metrics + baseline
     - `GET /health` - Health check
     
     ## Cost
     
     - **Development**: $0 (local Docker)
     - **Production Demo**: ~$1-2/month (Claude API)
     - **AWS**: Free tier covers everything
     
     ## Tech Stack
     
     | Component | Technology | Why |
     |-----------|-----------|-----|
     | Collection | FastAPI | Fast, clean REST API |
     | Streaming | Apache Kafka | Real-time, scalable |
     | Storage | PostgreSQL | Queryable, ACID |
     | Evaluation | Claude API | LLM-as-judge |
     | Detection | scikit-learn | Baseline + z-score |
     | Dashboard | Streamlit | Fast iteration |
     | Cloud | AWS Lambda + S3 | Serverless |
     
     ## Example Trace
     
     ```json
     {
       "trace_id": "abc-123",
       "question": "What's the weather in SF?",
       "tool_calls": [
         {"name": "weather_api", "output": "72°F, sunny"}
       ],
       "agent_response": "It's 72°F and sunny in SF"
     }
     ```
     
     ## Evaluation Output
     
     ```json
     {
       "correctness_score": 0.95,
       "hallucination_score": 0.92,
       "tool_usage_score": 0.98,
       "reasoning_score": 0.94,
       "overall_score": 0.95,
       "feedback": "Excellent use of weather_api, response grounded in facts"
     }
     ```
     
     ## Tests
     
     ```bash
     pytest tests/ -v
     ```
     
     ## Author
     
     Sagarika Raju
     MS Analytics, USC 2026
     [GitHub](https://github.com/saga0302) | [LinkedIn](https://linkedin.com/in/sagarika-raju)
     ```

5. **Tests (60 min)**
   - Create `tests/test_collector.py`:
     ```python
     import pytest
     from fastapi.testclient import TestClient
     from src.collector import app
     
     client = TestClient(app)
     
     def test_health():
         response = client.get("/health")
         assert response.status_code == 200
         assert response.json()["status"] == "ok"
     
     def test_collect_trace():
         trace = {
             "question": "What's 2+2?",
             "tool_calls": [],
             "agent_response": "4"
         }
         response = client.post("/collect", json=trace)
         assert response.status_code == 200
         assert "trace_id" in response.json()
     ```
   - Create `tests/test_evaluator.py`
   - Create `tests/test_anomaly_detector.py`

**Validation Checklist:**
- ✅ All code has docstrings
- ✅ Type hints on all functions
- ✅ Error handling with logging
- ✅ AWS Lambda function created
- ✅ GitHub Actions workflow passing
- ✅ Tests pass: `pytest tests/ -v`
- ✅ README comprehensive with examples
- ✅ Code style consistent (black formatting)

**End-of-Day Commit:**
```
git commit -m "Day 7: Code polish, AWS Lambda demo, GitHub Actions CI, comprehensive README"
git push
```

---

### DAY 8: RECORDING + PORTFOLIO (4–5 hours)

**Objective:** Professional demo video, portfolio assets ready for interviews

**Deliverables:**
- Recorded demo video (5 min)
- Screenshot collection
- Portfolio writeup
- LinkedIn post draft
- Interview talking points

**Tasks:**

1. **Record Demo Video (90 min)**
   - Use OBS Studio (free) or ScreenFlow (Mac):
     ```bash
     # Option 1: ScreenFlow (Mac)
     # Record: bash demo/run_full_pipeline.sh → Dashboard walkthrough
     
     # Option 2: OBS Studio (cross-platform)
     # Setup: Source → Display Capture → Record
     ```
   - Script (follow DEMO_WALKTHROUGH.md)
   - Record cleanly: 5 minutes max
   - Export as MP4 to `demo/demo.mp4`

2. **Screenshot Collection (45 min)**
   - Capture key screens:
     - Dashboard metrics
     - Traces table
     - Drill-down view (with scores)
     - Trends chart
     - Anomaly scatter plot
   - Save to `docs/screenshots/`
   - Create `docs/SCREENSHOTS.md` with captions

3. **Portfolio Writeup (75 min)**
   - Create `docs/PORTFOLIO.md`:
     ```markdown
     # Real-Time LLM Agent Observability Platform
     ## Portfolio Project
     
     ### Summary
     Built an open-source, production-grade observability system for AI agents that detects semantic failures in real-time using streaming infrastructure + Claude LLM-as-judge evaluation.
     
     ### Problem
     Companies running autonomous AI agents can't detect when reasoning fails silently. An agent returns a response with a 200 status, but the answer is hallucinated, tools are misused, or reasoning is flawed. Teams find out through customer complaints days later.
     
     ### Solution
     Real-time observability combining three principles:
     1. **Capture everything** - Stream all agent traces via Kafka
     2. **Evaluate instantly** - Score each trace with Claude (LLM-as-judge)
     3. **Detect anomalies** - Flag when quality drops using ML baselines
     
     ### Architecture
     
     **Data Flow:**
     Agent execution → FastAPI collector → Kafka stream → Claude evaluator → Anomaly detector → PostgreSQL → Streamlit dashboard
     
     **Key Components:**
     - **Trace Collector** (FastAPI): REST endpoint capturing question, tools, response
     - **Kafka Pipeline** (Apache): Real-time event stream (500+ traces/min)
     - **Claude Evaluator** (LLM-as-judge): Scores correctness, hallucination, tool usage
     - **Anomaly Detector** (ML): Baseline score + z-score > 2 flagging
     - **Dashboard** (Streamlit): Interactive exploration + trends
     
     ### Tech Stack
     - **Backend**: Python, FastAPI, PostgreSQL
     - **Streaming**: Apache Kafka, Kafka-Python
     - **Evaluation**: Anthropic Claude API
     - **ML**: scikit-learn, NumPy
     - **Dashboard**: Streamlit
     - **Cloud**: AWS Lambda, S3 (demo)
     - **Testing**: pytest, GitHub Actions
     
     ### Key Features
     
     ✅ **Real-time detection** - Flags hallucinations within 60 seconds  
     ✅ **Scalable architecture** - Kafka handles 10K+ traces/min  
     ✅ **LLM evaluation** - Claude scores each trace (correctness, hallucination, tool usage)  
     ✅ **Anomaly detection** - ML-based baseline + z-score flagging  
     ✅ **Interactive dashboard** - Drill-down into failures, see trends  
     ✅ **Production-ready** - Error handling, logging, testing  
     ✅ **AWS-compatible** - Lambda + S3 integration included  
     ✅ **Zero cost dev** - Docker-based local development  
     
     ### Results
     
     **What works:**
     - Evaluated 500+ synthetic traces in < 15 minutes
     - Correctly identified hallucinations (z-score < -2)
     - Baseline + drift detection catching systemic quality drops
     - Dashboard renders all metrics without lag
     - Full pipeline runs on single laptop
     
     ### Key Insights
     
     1. **Claude LLM-as-judge is powerful** - Much faster than human review, consistent scoring across thousands of traces
     2. **Streaming matters** - Kafka enables real-time alerts (not batch, not after-the-fact)
     3. **Anomaly detection is pattern recognition** - Finding systemic issues (all traces hallucinating) is where ML shines, not individual trace scoring
     4. **Production thinking wins** - Infrastructure > accuracy. Teams need observability before they need perfect models.
     
     ### Hiring Signal
     
     This project demonstrates:
     - **Data engineering competency** (Kafka, streaming, pipeline design)
     - **AI systems thinking** (evaluation, agents, LLM integration)
     - **AWS proficiency** (Lambda, S3, cloud architecture)
     - **Production mindset** (error handling, monitoring, scaling)
     - **End-to-end ownership** (backend → ML → dashboard)
     
     **Best fit for:**
     - Anthropic (AI Reliability, Infrastructure)
     - OpenAI (Cloud Inference, Platform Eng)
     - Databricks (Agent Observability)
     - Scale AI (Data Platform)
     - Weights & Biases (ML monitoring)
     
     ### Repo
     https://github.com/saga0302/agent-observability
     
     ### Demo
     Video: [demo.mp4](../demo/demo.mp4)
     Live: `bash demo/run_full_pipeline.sh`
     ```

4. **LinkedIn Post Draft (30 min)**
   - Create `docs/LINKEDIN_POST.md`:
     ```markdown
     🚀 Just shipped: Real-Time LLM Agent Observability Platform
     
     Here's the problem: AI agents appear to succeed (200 status) but fail semantically—they hallucinate, misuse tools, or reason incorrectly. Teams find out through angry customers, not from logs.
     
     I built an open-source observability system that catches these failures *before* they reach users:
     
     💡 Architecture:
     • Kafka streams every agent execution trace
     • Claude LLM-as-judge scores correctness + hallucinations
     • ML anomaly detection flags when quality drops
     • Streamlit dashboard shows exactly what went wrong
     
     🛠️ Tech: Python, FastAPI, Kafka, PostgreSQL, Claude API, AWS Lambda
     
     🎯 Result: Evaluate 10K traces/day, detect failures in <1 minute, 100% automated
     
     This is what every company with production agents actually needs—not just better models, but observability to understand when they fail.
     
     Code: github.com/saga0302/agent-observability
     
     Now applying to Anthropic, OpenAI, Databricks—companies that live and breathe this problem.
     
     #AI #DataEngineering #MLOps #LLMs
     ```

5. **Interview Talking Points (45 min)**
   - Create `docs/INTERVIEW_TALKING_POINTS.md`:
     ```markdown
     # Interview Talking Points: Agent Observability Platform
     
     ## Opening (30 sec)
     "I built a real-time observability platform for AI agents. The core insight: companies can't detect when agents fail semantically. They optimize for inference speed and accuracy, but they have no visibility into why an agent hallucinated or misused a tool. My platform fixes this by streaming traces through Kafka, evaluating each with Claude, and alerting teams instantly."
     
     ## Why This Matters (1 min)
     "Every AI company I applied to—Anthropic, OpenAI, Databricks—is running production agents and struggling with the same problem: silent failures. An agent says it's confident, but it's hallucinating. Or it calls the wrong tool. These aren't crashes; they're silent quality drops. Traditional APM catches that a request succeeded; you need LLM observability to catch that the reasoning failed."
     
     ## Technical Deep Dive (2 min)
     
     ### Architecture
     "The architecture is: Agent execution → FastAPI collector (traces) → Kafka stream → Claude evaluator → Anomaly detector → PostgreSQL → Streamlit dashboard.
     
     The key insight: use Kafka for real-time streaming. Why? Because in production, you can't wait for a batch job at midnight to find out your agent started hallucinating 2 hours ago. You need to know instantly.
     
     Then Claude LLM-as-judge scores each trace on three dimensions: correctness (did you answer right?), hallucination (did you make it up?), and tool usage (did you use the tools correctly?). Claude is fast enough and consistent enough to evaluate thousands of traces.
     
     Finally, anomaly detection: ML baseline + z-score. If a trace scores 2 standard deviations below the baseline, it's flagged. This catches both individual bad traces and systematic quality drift."
     
     ### Challenges & Solutions
     
     **Challenge 1: Scale**
     "Evaluating 10K traces/day with LLM API calls was expensive. Solution: batch evaluation + prompt caching. Cache the system prompt, evaluate traces in batches. Cuts API cost 80%, reduces latency."
     
     **Challenge 2: False positives**
     "Early anomaly detection flagged too much. Solution: windowed baseline (last 100 evals) + z-score threshold 2 (not 1). This balances sensitivity and specificity."
     
     **Challenge 3: Production readiness**
     "Needed to handle network failures, API retries, database timeouts. Solution: exponential backoff for API calls, connection pooling for Postgres, Kafka consumer groups for automatic rebalancing."
     
     ## Why This For Your Company (customized per company)
     
     ### For Anthropic
     "You're scaling Claude to production systems. Every customer running an agentic workflow needs visibility. This platform is exactly what you'd ship to enterprises as a first-party monitoring solution. I built it, so I understand the integration points."
     
     ### For OpenAI
     "GPTs and Agents are core products. You need infrastructure to observe and debug them at scale. This platform shows I can reason about reliability, not just capability."
     
     ### For Databricks
     "You're positioning Databricks as the platform for end-to-end ML. This project bridges the gap: data pipelines (Kafka) → LLM evaluation → dashboarding. It's the monitoring layer on top of your stack."
     
     ## Skills Demonstrated
     
     ✅ Data pipelines (Kafka, real-time streaming)
     ✅ API design (FastAPI, REST endpoints)
     ✅ LLM integration (Claude API, prompt engineering, batch inference)
     ✅ ML operations (baseline detection, anomaly scoring)
     ✅ Cloud architecture (AWS Lambda, S3, free tier design)
     ✅ Full-stack (backend, database, frontend, cloud)
     ✅ Production thinking (error handling, monitoring, scalability)
     
     ## Questions You Might Get
     
     **Q: Why Claude for evaluation instead of GPT-4 or open-source?**
     A: "Claude is faster (Haiku), cheaper, and has better reasoning on edge cases. For evaluation, consistency matters more than raw capability. I also have Anthropic API access and wanted hands-on experience integrating it."
     
     **Q: Why Kafka instead of AWS Kinesis or SQS?**
     A: "Kafka is portable, handles rebalancing automatically, and gives me consumer group semantics that match this use case. Kinesis is fine for production on AWS, but Kafka taught me more about streaming architecture."
     
     **Q: What would you do differently at scale?**
     A: "Switch to managed Kafka (Confluent Cloud or AWS MSK), move PostgreSQL to RDS with read replicas, add caching (Redis) for baseline scores, and consider vector search (Pinecone/Weaviate) for trace similarity clustering. The core architecture scales; it's operational overhead that changes."
     
     **Q: How do you handle prompt injection in agent traces?**
     A: "Good question. The evaluator sees the raw trace (question + response), not the agent's internals. If an agent is compromised, it'll show in the correctness score. For defense: I'd add a separate safety evaluator checking for prompt injection patterns in tool outputs."
     ```

**Validation Checklist:**
- ✅ Demo video recorded and saved (demo.mp4)
- ✅ Screenshots captured (5+ images)
- ✅ Portfolio writeup complete
- ✅ LinkedIn post ready
- ✅ Interview talking points documented
- ✅ README linked to demo video
- ✅ GitHub repo public + comprehensive

**End-of-Day Commit:**
```
git commit -m "Day 8: Demo video, portfolio writeup, LinkedIn post, interview talking points"
git push
```

---

### DAY 9: FINAL POLISH + DEPLOY (3–4 hours)

**Objective:** Production-ready codebase, deployed demo, ready for job applications

**Deliverables:**
- Code review + final fixes
- Streamlit Cloud deployment (optional but impressive)
- Bug fixes + edge cases
- Final README updates
- All tests passing

**Tasks:**

1. **Code Review & Polish (60 min)**
   - Review every file for:
     - Unused imports
     - Inconsistent naming
     - Missing error handling
     - Hardcoded values (use env vars)
   - Run black formatter: `black src/ tests/ dashboard/`
   - Run flake8: `flake8 src/ tests/` (fix style issues)

2. **Streamlit Cloud Deployment (90 min, optional)**
   - Create `.streamlit/config.toml`:
     ```toml
     [theme]
     primaryColor="#FF6B00"
     backgroundColor="#FFFFFF"
     secondaryBackgroundColor="#F0F2F6"
     textColor="#31333F"
     font="sans serif"
     ```
   - Push to GitHub
   - Go to https://streamlit.io/cloud
   - Deploy repo (choose `dashboard/streamlit_app.py`)
   - Share link in README

3. **Final Testing (45 min)**
   - Run full pipeline one more time
   - Check all tests pass: `pytest tests/ -v`
   - Verify dashboard loads without errors
   - Check logs for warnings

4. **Documentation Final Pass (30 min)**
   - Spell-check README
   - Verify all links work
   - Add troubleshooting section:
     ```markdown
     ## Troubleshooting
     
     ### "Port 8000 already in use"
     Kill existing process: `lsof -i :8000 | grep LISTEN | awk '{print $2}' | xargs kill -9`
     
     ### "Kafka broker not reachable"
     Check containers: `docker ps`
     Restart: `docker-compose restart kafka`
     
     ### "Claude API error"
     Verify env var: `echo $ANTHROPIC_API_KEY`
     Check rate limits: https://console.anthropic.com/usage
     ```

**Validation Checklist:**
- ✅ All tests pass: `pytest tests/ -v`
- ✅ Code formatted: `black src/ tests/ dashboard/`
- ✅ No linting issues: `flake8 src/`
- ✅ All env vars documented
- ✅ README complete with troubleshooting
- ✅ GitHub Actions CI passing
- ✅ Demo video uploaded to repo
- ✅ Portfolio writeup in docs/

**End-of-Day Commit:**
```
git commit -m "Day 9: Final polish, testing, documentation, deployment"
git push
```

---

### DAY 10: PORTFOLIO LAUNCH (2–3 hours)

**Objective:** Ready for interviews, applications, portfolio showcase

**Deliverables:**
- GitHub repo polished + featured
- LinkedIn post published
- Wellfound + portfolio website updated
- First interview version ready
- Job applications reference this project

**Tasks:**

1. **GitHub Polish (45 min)**
   - Add GitHub badges to README:
     ```markdown
     ![Tests](https://github.com/saga0302/agent-observability/workflows/Tests/badge.svg)
     ![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue)
     ![MIT License](https://img.shields.io/badge/license-MIT-green)
     ```
   - Add repo description: "Real-time observability for AI agents using Kafka + Claude LLM-as-judge"
   - Add topics: `kafka`, `llm`, `claude`, `observability`, `agents`, `data-engineering`
   - Pin repo to profile

2. **LinkedIn Post (30 min)**
   - Publish the post from Day 8
   - Tag: Anthropic, OpenAI, Databricks
   - Add hashtags: #AI #DataEngineering #MLOps

3. **Portfolio Website Update (30 min)**
   - Add project to portfolio:
     - Title, description, tech stack
     - Link to GitHub repo
     - Link to demo video
     - Key stats: "500+ traces, real-time eval, 0 infrastructure cost"

4. **Wellfound Update (30 min)**
   - Add project:
     - Title, description
     - GitHub link
     - Tech skills demonstrated

5. **Prepare Job Application Narrative (30 min)**
   - Create `docs/APPLICATION_NARRATIVE.md`:
     ```markdown
     # Job Application Narrative
     
     ## Where to mention this project
     
     ### For data engineering roles:
     "Built a real-time data pipeline using Kafka that streams 500+ AI agent execution traces to PostgreSQL, enabling real-time quality monitoring. Integrated Apache Kafka consumer groups for scalable event processing."
     
     ### For ML/AI roles:
     "Implemented LLM-as-judge evaluation framework using Claude API to automatically score agent correctness, hallucination, and tool usage across thousands of traces, replacing manual human review."
     
     ### For infrastructure roles:
     "Architected end-to-end system from trace collection (FastAPI) through real-time streaming (Kafka) to cloud deployment (AWS Lambda + S3), demonstrating scalability, error handling, and production readiness."
     
     ### In cover letters:
     "Shipped Real-Time LLM Agent Observability Platform, an open-source system that detects semantic failures in AI agents using streaming data + Claude LLM-as-judge evaluation. This directly addresses [Company]'s need to scale agent reliability in production."
     
     ### In interviews:
     (See INTERVIEW_TALKING_POINTS.md)
     ```

**Final Validation Checklist:**
- ✅ GitHub repo public + polished
- ✅ Tests passing
- ✅ README complete with demo link
- ✅ LinkedIn post published
- ✅ Portfolio website updated
- ✅ Wellfound updated
- ✅ Application narrative documented
- ✅ Ready to reference in applications

**Final Commit:**
```
git commit -m "Day 10: Portfolio launch, polish, ready for applications"
git push
```

---

## SUCCESS CRITERIA (END OF DAY 10)

✅ **Code**
- Production-grade Python codebase (src/)
- All major components working (collector → Kafka → evaluator → dashboard)
- Tests passing (pytest)
- GitHub Actions CI green
- Clean git history (meaningful commits)

✅ **Demo**
- 5-min video walkthrough (demo.mp4)
- 500+ synthetic traces flowing through pipeline
- Dashboard rendering all data
- No errors in logs

✅ **Portfolio**
- Polished GitHub repo (2K+ stars potential)
- Professional README with architecture diagrams
- Portfolio writeup (docs/PORTFOLIO.md)
- Interview talking points (docs/INTERVIEW_TALKING_POINTS.md)
- LinkedIn post published

✅ **Hiring Signal**
- Can explain architecture + trade-offs
- Shows Kafka + AWS + Claude API hands-on
- Demonstrates production thinking (monitoring, scaling, errors)
- Solves a real problem companies face today

---

## DAILY TIME BREAKDOWN

| Day | Task | Hours | Status |
|-----|------|-------|--------|
| 1 | Setup + Collector | 4-5h | Ready to ship 4 apps |
| 2 | Kafka + Storage | 4-5h | Background: collector running |
| 3 | Claude Evaluator | 5-6h | Background: evaluator worker running |
| 4 | Anomaly Detection | 4-5h | Background: detector running |
| 5 | Streamlit Dashboard | 5-6h | Background: dashboard running |
| 6 | Demo Data + Test | 4-5h | 500+ traces flowing through |
| 7 | Polish + AWS | 4-5h | Code clean, CI passing |
| 8 | Recording + Portfolio | 4-5h | Video + writeup done |
| 9 | Final Polish | 3-4h | Production-ready |
| 10 | Launch | 2-3h | Live + applications ready |
| **Total** | | **40-48h** | |

**Realistic breakdown:** 5-6 hours/day, 10 days = 50-60 hours total  
**Your schedule:** 4 apps/day (3-4h) + 1.5-2h project work + 1h learning = 7-8h/day  
This project fits perfectly in your 1.5-2h daily project slot while doing 4 apps/day.

---

## FREE TIER BUDGET

| Item | Cost | Notes |
|------|------|-------|
| Docker (Kafka + PostgreSQL) | $0 | Local development |
| Python + FastAPI | $0 | Open-source |
| PostgreSQL | $0 | Docker-based |
| Claude API (500 evals @ Haiku) | $0.50–$2 | One-time demo cost |
| Streamlit (free tier) | $0 | Web hosting free |
| AWS Lambda (free tier) | $0 | 1M invocations free |
| GitHub | $0 | Public repo free |
| **Total** | **$0.50–$2** | One-time cost |

---

## NEXT STEPS

1. **Read this document thoroughly** (today)
2. **Day 1 tomorrow:** Start with setup + collector
3. **Track daily progress** in README (commit every day)
4. **Apply for jobs** starting Day 6 (reference this project)
5. **Interview prep** with INTERVIEW_TALKING_POINTS.md

---

## Questions to Revisit

**"Is Claude better than humans for evaluation?"**
No—Claude is *faster* and more *consistent*. Humans are still the arbiters of edge cases. This is humans + AI, not AI replacing humans.

**"Why does this matter for hiring?"**
Because every company with production agents needs this. You're not building a demo; you're solving a real, urgent problem in the market right now.

**"What if it fails?"**
Then you debug it. Document what you learned. That's just as valuable for interviews. Show the thought process, not just success.

---

**Good luck. Ship it. Then tell the world.**

**Sagarika, you've got this.** 🚀

---

*Last Updated: July 15, 2026*  
*Total Development Time: 10 days, 40-50 hours*  
*Cost: $0 (development) + $0.50–$2 (demo)*  
*Impact: Portfolio-ready, interview-winning, production-grade observability platform*
