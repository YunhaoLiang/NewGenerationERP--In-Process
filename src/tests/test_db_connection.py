import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.config.database import engine
import sqlalchemy as sa

def test_connection():
    try:
        # 测试连接
        with engine.connect() as connection:
            result = connection.execute(sa.text("SELECT 1"))
            print("数据库连接成功！")
            
            # 测试查询库存视图
            inventory = connection.execute(sa.text("SELECT * FROM 库存状态视图")).fetchall()
            print("\n库存状态：")
            for item in inventory:
                print(item)
            
    except Exception as e:
        print(f"连接失败：{str(e)}")

if __name__ == "__main__":
    test_connection() 