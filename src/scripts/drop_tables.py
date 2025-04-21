import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from sqlalchemy import text
from src.config.database import engine

def drop_table(table_name):
    try:
        with engine.connect() as conn:
            conn.execute(text(f'DROP TABLE IF EXISTS {table_name} CASCADE'))
            conn.commit()
            print(f'已删除表：{table_name}')
    except Exception as e:
        print(f'删除表 {table_name} 时出错：{str(e)}')

if __name__ == '__main__':
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