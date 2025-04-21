import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from sqlalchemy import create_engine, text

def grant_permissions():
    """授予用户权限"""
    # 使用 postgres 用户连接数据库
    postgres_engine = create_engine("postgresql://postgres:postgres123@localhost:5432/erp_system")
    
    tables = [
        'users',
        'products',
        'inventory',
        'orders',
        'suppliers',
        'alembic_version'
    ]
    
    sequences = [
        'users_用户id_seq',
        'products_产品id_seq',
        'inventory_库存id_seq',
        'orders_订单id_seq',
        'suppliers_供应商id_seq'
    ]
    
    # 授予表权限
    for table in tables:
        with postgres_engine.connect() as conn:
            try:
                conn.execute(text(f'GRANT ALL PRIVILEGES ON TABLE "{table}" TO erp_admin'))
                conn.commit()
                print(f"已授予 erp_admin 用户对表 {table} 的权限")
            except Exception as e:
                print(f"授予表权限时出错：{str(e)}")
    
    # 授予序列权限
    for sequence in sequences:
        with postgres_engine.connect() as conn:
            try:
                conn.execute(text(f'GRANT ALL PRIVILEGES ON SEQUENCE "{sequence}" TO erp_admin'))
                conn.commit()
                print(f"已授予 erp_admin 用户对序列 {sequence} 的权限")
            except Exception as e:
                print(f"授予序列权限时出错：{str(e)}")

if __name__ == "__main__":
    grant_permissions() 