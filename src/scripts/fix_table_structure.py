from sqlalchemy import text
from src.config.database import engine

def fix_table_structure():
    """修复数据库表结构"""
    fix_tables_sql = """
    -- 修复 transactions 表
    DROP TABLE IF EXISTS transactions;
    CREATE TABLE transactions (
        transaction_id SERIAL PRIMARY KEY,
        account_id INTEGER REFERENCES financial_accounts(account_id),
        transaction_type VARCHAR(20) NOT NULL,
        amount NUMERIC(15,2) NOT NULL,
        description TEXT,
        transaction_date TIMESTAMP NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
    -- 修复 products 表
    ALTER TABLE products 
    ADD COLUMN IF NOT EXISTS product_name VARCHAR(100) NOT NULL DEFAULT 'Unknown Product',
    ADD COLUMN IF NOT EXISTS description TEXT,
    ADD COLUMN IF NOT EXISTS category VARCHAR(50),
    ADD COLUMN IF NOT EXISTS unit_price NUMERIC(15,2);
    
    -- 确保所有表都有必要的时间戳字段
    DO $$ 
    DECLARE
        t record;
    BEGIN
        FOR t IN 
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        LOOP
            EXECUTE format('ALTER TABLE %I 
                          ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                          ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP', 
                          t.table_name);
        END LOOP;
    END $$;
    """
    
    with engine.connect() as conn:
        try:
            conn.execute(text(fix_tables_sql))
            conn.commit()
            print("表结构修复成功！")
        except Exception as e:
            print(f"修复表结构时发生错误: {str(e)}")

if __name__ == "__main__":
    fix_table_structure() 