import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from sqlalchemy import inspect
from src.config.database import engine

def check_database():
    """检查数据库中的表"""
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print("\n数据库中的表：")
    for table in tables:
        print(f"- {table}")
        columns = inspector.get_columns(table)
        print("  列：")
        for column in columns:
            print(f"    - {column['name']}: {column['type']}")

if __name__ == "__main__":
    check_database() 