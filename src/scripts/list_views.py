import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.config.database import SessionLocal
from sqlalchemy import text

def list_views():
    """列出数据库中的所有视图"""
    db = SessionLocal()
    try:
        # 查询所有视图
        result = db.execute(text("""
            SELECT table_name 
            FROM information_schema.views 
            WHERE table_schema = 'public'
        """)).fetchall()
        
        print("\n=== 数据库视图列表 ===")
        for row in result:
            print(f"视图名称: {row[0]}")
            # 获取视图定义
            view_def = db.execute(text(f"""
                SELECT view_definition 
                FROM information_schema.views 
                WHERE table_schema = 'public' 
                AND table_name = '{row[0]}'
            """)).fetchone()
            print(f"视图定义:\n{view_def[0]}")
            print("---")
            
    except Exception as e:
        print(f"查询视图时出错：{str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    list_views() 