import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.config.database import engine
from src.models.models import Base

def create_tables():
    """创建所有数据库表"""
    try:
        Base.metadata.create_all(bind=engine)
        print("成功创建所有数据库表")
    except Exception as e:
        print(f"创建数据库表时出错：{str(e)}")

if __name__ == "__main__":
    create_tables() 