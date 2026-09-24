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