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
  evaluated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_trace_timestamp ON traces(timestamp);
CREATE INDEX idx_eval_score ON evaluations(correctness_score);