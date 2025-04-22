import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from sqlalchemy import text
from src.config.database import engine, SessionLocal
from sqlalchemy.orm import Session

def drop_table(table_name):
    try:
        with engine.connect() as conn:
            conn.execute(text(f'DROP TABLE IF EXISTS {table_name} CASCADE'))
            conn.commit()
            print(f'已删除表：{table_name}')
    except Exception as e:
        print(f'删除表 {table_name} 时出错：{str(e)}')

def alter_column_name(table_name: str, old_name: str, new_name: str):
    """修改列名"""
    db = SessionLocal()
    try:
        db.execute(text(f"ALTER TABLE {table_name} RENAME COLUMN {old_name} TO {new_name}"))
        db.commit()
        print(f"成功修改表 {table_name} 的列名：{old_name} -> {new_name}")
    except Exception as e:
        print(f"修改列名时出错：{str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == '__main__':
    # 修改orders表的列名
    alter_column_name('orders', 'order_date', 'created_at')
    
    # 删除所有表
    tables = [
        'transactions',
        'financial_reports',
        'financial_accounts',
        'budgets',
        'inventory',
        'orders',
        'products',
        'users',
        'suppliers',
        'alembic_version'
    ]
    
    for table in tables:
        drop_table(table) 