import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.config.database import SessionLocal, engine
from src.models.models import User, Product, Inventory, Order, Supplier, FinancialAccount, Transaction, Budget
from sqlalchemy import text
from tabulate import tabulate

def view_users():
    db = SessionLocal()
    users = db.query(User).all()
    print("\n=== 用户数据 ===")
    for user in users:
        print(f"用户ID: {user.user_id}")
        print(f"用户名: {user.username}")
        print(f"邮箱: {user.email}")
        print(f"角色: {user.role}")
        print("---")
    db.close()

def view_products():
    db = SessionLocal()
    products = db.query(Product).all()
    print("\n=== 产品数据 ===")
    for product in products:
        print(f"产品ID: {product.product_id}")
        print(f"产品名称: {product.product_name}")
        print(f"价格: {product.unit_price}")
        print(f"描述: {product.description}")
        print(f"类别: {product.category}")
        print("---")
    db.close()

def view_inventory():
    db = SessionLocal()
    inventory = db.query(Inventory).all()
    print("\n=== 库存数据 ===")
    for item in inventory:
        print(f"产品ID: {item.product_id}")
        print(f"数量: {item.quantity}")
        print(f"位置: {item.location}")
        print("---")
    db.close()

def view_orders():
    db = SessionLocal()
    orders = db.query(Order).all()
    print("\n=== 订单数据 ===")
    for order in orders:
        print(f"订单ID: {order.order_id}")
        print(f"用户ID: {order.user_id}")
        print(f"产品ID: {order.product_id}")
        print(f"数量: {order.quantity}")
        print(f"总金额: {order.total_amount}")
        print(f"状态: {order.status}")
        print("---")
    db.close()

def view_suppliers():
    db = SessionLocal()
    suppliers = db.query(Supplier).all()
    print("\n=== 供应商数据 ===")
    for supplier in suppliers:
        print(f"供应商ID: {supplier.supplier_id}")
        print(f"名称: {supplier.supplier_name}")
        print(f"联系人: {supplier.contact_person}")
        print(f"电话: {supplier.phone}")
        print(f"邮箱: {supplier.email}")
        print(f"地址: {supplier.address}")
        print("---")
    db.close()

def view_financial_accounts():
    db = SessionLocal()
    accounts = db.query(FinancialAccount).all()
    print("\n=== 财务账户数据 ===")
    for account in accounts:
        print(f"账户ID: {account.account_id}")
        print(f"账户名称: {account.account_name}")
        print(f"账户类型: {account.account_type}")
        print(f"余额: {account.balance}")
        print(f"币种: {account.currency}")
        print("---")
    db.close()

def view_transactions():
    db = SessionLocal()
    transactions = db.query(Transaction).all()
    print("\n=== 交易数据 ===")
    for trans in transactions:
        print(f"交易ID: {trans.transaction_id}")
        print(f"账户ID: {trans.account_id}")
        print(f"交易类型: {trans.transaction_type}")
        print(f"金额: {trans.amount}")
        print(f"描述: {trans.description}")
        print("---")
    db.close()

def view_budgets():
    db = SessionLocal()
    budgets = db.query(Budget).all()
    print("\n=== 预算数据 ===")
    for budget in budgets:
        print(f"预算ID: {budget.budget_id}")
        print(f"部门: {budget.department}")
        print(f"类别: {budget.category}")
        print(f"金额: {budget.amount}")
        print(f"开始日期: {budget.period_start}")
        print(f"结束日期: {budget.period_end}")
        print(f"状态: {budget.status}")
        print("---")
    db.close()

def view_views():
    """查看所有视图数据"""
    try:
        with engine.connect() as conn:
            # 查看订单详情视图
            print("\n=== 订单详情视图 ===")
            result = conn.execute(text("SELECT * FROM vw_order_details"))
            rows = result.fetchall()
            if rows:
                print(tabulate(rows, headers=result.keys(), tablefmt="grid"))
            
            # 查看库存状态视图
            print("\n=== 库存状态视图 ===")
            result = conn.execute(text("SELECT * FROM vw_inventory_status"))
            rows = result.fetchall()
            if rows:
                print(tabulate(rows, headers=result.keys(), tablefmt="grid"))
            
            # 查看账户余额视图
            print("\n=== 账户余额视图 ===")
            result = conn.execute(text("SELECT * FROM vw_account_balance"))
            rows = result.fetchall()
            if rows:
                print(tabulate(rows, headers=result.keys(), tablefmt="grid"))
            
            # 查看预算执行情况视图
            print("\n=== 预算执行情况视图 ===")
            result = conn.execute(text("SELECT * FROM vw_budget_execution"))
            rows = result.fetchall()
            if rows:
                print(tabulate(rows, headers=result.keys(), tablefmt="grid"))
            
            # 查看交易记录视图
            print("\n=== 交易记录视图 ===")
            result = conn.execute(text("SELECT * FROM vw_transaction_details"))
            rows = result.fetchall()
            if rows:
                print(tabulate(rows, headers=result.keys(), tablefmt="grid"))
            
            # 查看供应商产品视图
            print("\n=== 供应商产品视图 ===")
            result = conn.execute(text("SELECT * FROM vw_supplier_products"))
            rows = result.fetchall()
            if rows:
                print(tabulate(rows, headers=result.keys(), tablefmt="grid"))

    except Exception as e:
        print(f"查看视图数据时出错：{str(e)}")

def view_data():
    """查看数据库中的所有数据"""
    try:
        # 查看基础数据
        view_users()
        view_products()
        view_inventory()
        view_orders()
        view_suppliers()
        view_financial_accounts()
        view_transactions()
        view_budgets()
        
        # 查看视图数据
        view_views()
            
    except Exception as e:
        print(f"查看数据时出错：{str(e)}")

if __name__ == "__main__":
    view_data() 