import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.config.database import engine, Base
from src.models.database_models import Order, ProductionPlan, JobSchedule, Prediction, Inventory, SupplyChainRecord

def init_database():
    """初始化数据库，创建所有表"""
    try:
        print("开始创建数据库表...")
        Base.metadata.create_all(bind=engine)
        print("数据库表创建成功！")
    except Exception as e:
        print(f"创建数据库表时出错: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    init_database() 