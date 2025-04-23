from sqlalchemy import inspect, text
from src.config.database import engine

def check_table_structure():
    """检查数据库中的表结构"""
    inspector = inspect(engine)
    
    # 获取所有表名
    table_names = inspector.get_table_names()
    print("\n=== 数据库中的所有表 ===")
    for table_name in table_names:
        print(f"\n表名: {table_name}")
        
        # 获取表的列信息
        columns = inspector.get_columns(table_name)
        print("列信息:")
        for column in columns:
            print(f"  - {column['name']}: {column['type']} (nullable: {column['nullable']})")

if __name__ == "__main__":
    check_table_structure() 