from sqlalchemy import inspect
from sqlalchemy.orm import Session
from src.config.database import engine, SessionLocal
from src.models.models import User, Product, Inventory, Order, Supplier, FinancialAccount, Transaction, Budget

def print_table_data(session: Session, model):
    """打印指定表的所有数据"""
    print(f"\n{'='*20} {model.__tablename__} 表 {'='*20}")
    records = session.query(model).all()
    if not records:
        print("表中暂无数据")
        return
    
    # 获取所有列名
    columns = [column.key for column in inspect(model).columns]
    
    # 打印表头
    header = " | ".join(f"{col:<15}" for col in columns)
    print("\n" + header)
    print("-" * len(header))
    
    # 打印数据
    for record in records:
        row = []
        for col in columns:
            value = getattr(record, col)
            # 将值转换为字符串并限制长度
            value_str = str(value)[:15] if value is not None else "None"
            row.append(f"{value_str:<15}")
        print(" | ".join(row))

def main():
    """主函数：显示所有表的数据"""
    print("\n=== ERP系统数据库内容 ===\n")
    
    # 创建数据库会话
    session = SessionLocal()
    
    try:
        # 所有模型类
        models = [User, Product, Inventory, Order, Supplier, 
                 FinancialAccount, Transaction, Budget]
        
        # 打印每个表的数据
        for model in models:
            print_table_data(session, model)
            
    except Exception as e:
        print(f"查询数据时发生错误: {str(e)}")
    finally:
        session.close()

if __name__ == "__main__":
    main() 