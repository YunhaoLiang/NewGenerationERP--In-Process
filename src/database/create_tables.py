from src.config.database import Base, engine
from src.models.models import User, Product, Order, Inventory, Supplier, FinancialAccount, Transaction, Budget
from sqlalchemy import text

def create_tables():
    print("正在创建数据库表...")
    try:
        # 打印所有要创建的表
        tables = Base.metadata.tables
        print(f"将要创建以下表：{', '.join(tables.keys())}")
        
        # 使用 CASCADE 选项删除所有现有的表
        print("删除现有表...")
        with engine.connect() as conn:
            conn.execute(text("DROP SCHEMA public CASCADE"))
            conn.execute(text("CREATE SCHEMA public"))
            conn.commit()
        
        # 创建新表
        print("创建新表...")
        Base.metadata.create_all(bind=engine)
        print("数据库表创建成功！")
        
        # 验证表是否创建成功
        from sqlalchemy import inspect
        inspector = inspect(engine)
        created_tables = inspector.get_table_names()
        print(f"已创建的表：{', '.join(created_tables)}")
        
    except Exception as e:
        print(f"创建数据库表时出错: {str(e)}")
        raise

if __name__ == "__main__":
    create_tables() 