from sqlalchemy import text
from src.config.database import engine

def create_budgets_table():
    """创建预算表"""
    create_table_sql = """
    DO $$ 
    BEGIN
        IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'budget_status') THEN
            CREATE TYPE budget_status AS ENUM ('active', 'completed', 'cancelled');
        END IF;
    END $$;

    DROP TABLE IF EXISTS budgets;
    
    CREATE TABLE budgets (
        budget_id SERIAL PRIMARY KEY,
        department VARCHAR(100) NOT NULL,
        category VARCHAR(100) NOT NULL,
        amount NUMERIC(15,2) NOT NULL,
        period_start TIMESTAMP NOT NULL,
        period_end TIMESTAMP NOT NULL,
        actual_amount NUMERIC(15,2),
        status VARCHAR(20) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
    CREATE INDEX IF NOT EXISTS ix_budgets_budget_id ON budgets (budget_id);
    """
    
    with engine.connect() as conn:
        try:
            conn.execute(text(create_table_sql))
            conn.commit()
            print("预算表创建成功！")
        except Exception as e:
            print(f"创建预算表时发生错误: {str(e)}")

if __name__ == "__main__":
    create_budgets_table() 