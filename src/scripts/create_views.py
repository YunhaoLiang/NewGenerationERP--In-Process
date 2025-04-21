import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from sqlalchemy import text
from src.config.database import engine

def create_view(view_name, view_sql):
    try:
        with engine.connect() as conn:
            # 先删除已存在的视图
            conn.execute(text(f'DROP VIEW IF EXISTS {view_name} CASCADE'))
            # 创建新视图
            conn.execute(text(view_sql))
            conn.commit()
            print(f'已创建视图：{view_name}')
    except Exception as e:
        print(f'创建视图 {view_name} 时出错：{str(e)}')

if __name__ == '__main__':
    # 订单详情视图
    order_view_sql = """
    CREATE VIEW vw_order_details AS
    SELECT 
        o.order_id,
        u.username,
        p.product_name,
        o.quantity,
        o.total_amount,
        o.status,
        o.created_at as order_date
    FROM orders o
    JOIN users u ON o.user_id = u.user_id
    JOIN products p ON o.product_id = p.product_id
    """
    create_view('vw_order_details', order_view_sql)

    # 库存状态视图
    inventory_view_sql = """
    CREATE VIEW vw_inventory_status AS
    SELECT 
        i.inventory_id,
        p.product_name,
        i.quantity,
        i.location,
        p.unit_price,
        (p.unit_price * i.quantity) as total_value,
        i.last_updated
    FROM inventory i
    JOIN products p ON i.product_id = p.product_id
    """
    create_view('vw_inventory_status', inventory_view_sql)

    # 财务账户余额视图
    account_view_sql = """
    CREATE VIEW vw_account_balance AS
    SELECT 
        fa.account_id,
        fa.account_name,
        fa.account_type,
        fa.balance,
        fa.currency,
        fa.updated_at as last_updated
    FROM financial_accounts fa
    """
    create_view('vw_account_balance', account_view_sql)

    # 预算执行情况视图
    budget_view_sql = """
    CREATE VIEW vw_budget_execution AS
    SELECT 
        b.budget_id,
        b.department,
        b.category,
        b.amount as budget_amount,
        b.actual_amount,
        CASE 
            WHEN b.actual_amount IS NULL THEN 0
            ELSE (b.actual_amount / b.amount * 100)
        END as execution_rate,
        b.period_start,
        b.period_end,
        b.status
    FROM budgets b
    """
    create_view('vw_budget_execution', budget_view_sql)

    # 交易记录视图
    transaction_view_sql = """
    CREATE VIEW vw_transaction_details AS
    SELECT 
        t.transaction_id,
        fa.account_name,
        t.transaction_type,
        t.amount,
        t.description,
        t.transaction_date,
        t.created_at
    FROM transactions t
    JOIN financial_accounts fa ON t.account_id = fa.account_id
    """
    create_view('vw_transaction_details', transaction_view_sql)

    # 供应商产品视图
    supplier_products_sql = """
    CREATE VIEW vw_supplier_products AS
    SELECT 
        s.supplier_id,
        s.supplier_name,
        s.contact_person,
        s.phone,
        s.email,
        p.product_id,
        p.product_name,
        p.unit_price,
        i.quantity as current_stock,
        i.location as stock_location
    FROM suppliers s
    CROSS JOIN products p
    LEFT JOIN inventory i ON p.product_id = i.product_id
    """
    create_view('vw_supplier_products', supplier_products_sql)

    print('所有视图创建完成！') 