import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.config.database import SessionLocal
from src.models.models import User, Product, Inventory, Order, Supplier
from sqlalchemy import text

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

def view_inventory():
    db = SessionLocal()
    inventory = db.query(Inventory).all()
    print("\n=== 库存数据 ===")
    for item in inventory:
        print(f"产品ID: {item.product_id}")
        print(f"数量: {item.quantity}")
        print(f"位置: {item.location}")
        print("---")

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

def view_data():
    """查看数据库中的所有数据"""
    db = SessionLocal()
    try:
        # 查看用户
        view_users()
        
        # 查看产品
        view_products()
        
        # 查看库存
        view_inventory()
        
        # 查看订单
        view_orders()
        
        # 查看供应商
        view_suppliers()

        # 查看订单详情视图
        print("\n=== 订单详情视图 ===")
        order_details = db.execute(text("SELECT * FROM vw_order_details")).fetchall()
        for order in order_details:
            print(f"订单ID: {order.order_id}")
            print(f"用户名: {order.username}")
            print(f"产品名称: {order.product_name}")
            print(f"数量: {order.quantity}")
            print(f"总金额: {order.total_amount}")
            print(f"状态: {order.status}")
            print(f"下单时间: {order.order_date}")
            print("---")

        # 查看库存状态视图
        print("\n=== 库存状态视图 ===")
        inventory_status = db.execute(text("SELECT * FROM vw_inventory_status")).fetchall()
        for item in inventory_status:
            print(f"库存ID: {item.inventory_id}")
            print(f"产品名称: {item.product_name}")
            print(f"数量: {item.quantity}")
            print(f"位置: {item.location}")
            print(f"单价: {item.unit_price}")
            print(f"总价值: {item.total_value}")
            print(f"最后更新: {item.last_updated}")
            print("---")

        # 查看供应商产品视图
        print("\n=== 供应商产品视图 ===")
        supplier_products = db.execute(text("SELECT * FROM vw_supplier_products")).fetchall()
        for item in supplier_products:
            print(f"供应商ID: {item.supplier_id}")
            print(f"供应商名称: {item.supplier_name}")
            print(f"联系人: {item.contact_person}")
            print(f"电话: {item.phone}")
            print(f"邮箱: {item.email}")
            print(f"产品ID: {item.product_id}")
            print(f"产品名称: {item.product_name}")
            print(f"单价: {item.unit_price}")
            print(f"当前库存: {item.current_stock}")
            print(f"库存位置: {item.stock_location}")
            print("---")

        # 查看财务账户余额视图
        print("\n=== 财务账户余额视图 ===")
        account_balance = db.execute(text("SELECT * FROM vw_account_balance")).fetchall()
        for account in account_balance:
            print(f"账户ID: {account.account_id}")
            print(f"账户名称: {account.account_name}")
            print(f"账户类型: {account.account_type}")
            print(f"余额: {account.balance}")
            print(f"币种: {account.currency}")
            print(f"最后更新: {account.last_updated}")
            print("---")

        # 查看预算执行情况视图
        print("\n=== 预算执行情况视图 ===")
        budget_execution = db.execute(text("SELECT * FROM vw_budget_execution")).fetchall()
        for budget in budget_execution:
            print(f"预算ID: {budget.budget_id}")
            print(f"部门: {budget.department}")
            print(f"类别: {budget.category}")
            print(f"预算金额: {budget.budget_amount}")
            print(f"实际金额: {budget.actual_amount}")
            print(f"执行率: {budget.execution_rate}%")
            print(f"开始日期: {budget.period_start}")
            print(f"结束日期: {budget.period_end}")
            print(f"状态: {budget.status}")
            print("---")

        # 查看交易记录视图
        print("\n=== 交易记录视图 ===")
        transaction_details = db.execute(text("SELECT * FROM vw_transaction_details")).fetchall()
        for trans in transaction_details:
            print(f"交易ID: {trans.transaction_id}")
            print(f"账户名称: {trans.account_name}")
            print(f"交易类型: {trans.transaction_type}")
            print(f"金额: {trans.amount}")
            print(f"描述: {trans.description}")
            print(f"交易日期: {trans.transaction_date}")
            print(f"创建时间: {trans.created_at}")
            print("---")
            
    except Exception as e:
        print(f"查看数据时出错：{str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    view_data() 