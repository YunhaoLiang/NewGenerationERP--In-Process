-- 创建task_history表
CREATE TABLE IF NOT EXISTS task_history (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL,
    task_id VARCHAR(50) NOT NULL,
    task_type VARCHAR(50) NOT NULL,
    input JSONB,
    output JSONB,
    status VARCHAR(20) NOT NULL,
    agents_involved JSONB,
    execution_time FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建索引
CREATE INDEX idx_task_history_timestamp ON task_history(timestamp);
CREATE INDEX idx_task_history_task_type ON task_history(task_type);
CREATE INDEX idx_task_history_task_id ON task_history(task_id); 