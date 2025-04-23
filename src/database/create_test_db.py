from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 从环境变量获取数据库连接信息
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres123")

def create_test_database():
    # 连接到默认的 postgres 数据库
    engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/postgres", 
                         isolation_level="AUTOCOMMIT")
    
    with engine.connect() as conn:
        # 先终止所有到测试数据库的连接
        conn.execute(text("""
            SELECT pg_terminate_backend(pg_stat_activity.pid)
            FROM pg_stat_activity
            WHERE pg_stat_activity.datname = 'erp_system_test'
            AND pid <> pg_backend_pid();
        """))
        
        # 删除已存在的数据库
        conn.execute(text("DROP DATABASE IF EXISTS erp_system_test"))
        
        # 创建新的数据库
        conn.execute(text("CREATE DATABASE erp_system_test"))
    
    print("测试数据库创建完成！")

    # 连接到新创建的测试数据库并创建表
    test_engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/erp_system_test")
    with test_engine.connect() as conn:
        # 创建表
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS products (
                product_id SERIAL PRIMARY KEY,
                product_name VARCHAR(255) NOT NULL,
                unit_price FLOAT NOT NULL,
                description TEXT,
                category VARCHAR(50),
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE TABLE IF NOT EXISTS users (
                user_id SERIAL PRIMARY KEY,
                username VARCHAR(50) NOT NULL UNIQUE,
                email VARCHAR(100) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL,
                role VARCHAR(20) NOT NULL,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE TABLE IF NOT EXISTS orders (
                order_id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(user_id),
                product_id INTEGER REFERENCES products(product_id),
                quantity INTEGER NOT NULL,
                total_amount FLOAT NOT NULL,
                status VARCHAR(20) NOT NULL,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE TABLE IF NOT EXISTS inventory (
                inventory_id SERIAL PRIMARY KEY,
                product_id INTEGER REFERENCES products(product_id),
                quantity INTEGER NOT NULL,
                location VARCHAR(100),
                last_updated TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE TABLE IF NOT EXISTS suppliers (
                supplier_id SERIAL PRIMARY KEY,
                supplier_name VARCHAR(100) NOT NULL,
                contact_person VARCHAR(100),
                phone VARCHAR(20),
                email VARCHAR(100),
                address TEXT,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE TABLE IF NOT EXISTS financial_accounts (
                account_id SERIAL PRIMARY KEY,
                account_name VARCHAR(100) NOT NULL UNIQUE,
                account_type VARCHAR(20) NOT NULL,
                balance FLOAT NOT NULL DEFAULT 0,
                currency VARCHAR(3) NOT NULL DEFAULT 'CNY',
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE TABLE IF NOT EXISTS transactions (
                transaction_id SERIAL PRIMARY KEY,
                account_id INTEGER REFERENCES financial_accounts(account_id),
                transaction_type VARCHAR(20) NOT NULL,
                amount FLOAT NOT NULL,
                description TEXT,
                transaction_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE TABLE IF NOT EXISTS budgets (
                budget_id SERIAL PRIMARY KEY,
                department VARCHAR(50) NOT NULL,
                category VARCHAR(50) NOT NULL,
                amount FLOAT NOT NULL,
                actual_amount FLOAT,
                period_start TIMESTAMP WITH TIME ZONE NOT NULL,
                period_end TIMESTAMP WITH TIME ZONE NOT NULL,
                status VARCHAR(20) NOT NULL,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            );
        """))
        conn.commit()
    
    print("数据库表创建完成！")

if __name__ == "__main__":
    create_test_database() 