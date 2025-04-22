CREATE TABLE IF NOT EXISTS task_history (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL,
    task_id VARCHAR(36) NOT NULL,
    task_type VARCHAR(50) NOT NULL,
    input TEXT NOT NULL,
    output TEXT NOT NULL,
    status VARCHAR(20) NOT NULL,
    agents_involved TEXT NOT NULL,
    execution_time FLOAT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
); 