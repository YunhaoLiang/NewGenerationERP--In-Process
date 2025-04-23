from sqlalchemy.orm import Session
from src.config.database import SessionLocal
from src.models.models import User, Product, Order, Inventory, Supplier, FinancialAccount, Transaction, Budget

def view_data():
    db = SessionLocal()
    try:
        print("\n=== 用户数据 ===")
        users = db.query(User).all()
        for user in users:
            print(f"用户ID: {user.user_id}, 用户名: {user.username}, 角色: {user.role}")

        print("\n=== 供应商数据 ===")
        suppliers = db.query(Supplier).all()
        for supplier in suppliers:
            print(f"供应商: {supplier.supplier_name}, 联系人: {supplier.contact_person}, 地址: {supplier.address}")

        print("\n=== 产品数据 ===")
        products = db.query(Product).all()
        for product in products:
            print(f"产品: {product.product_name}, 价格: {product.unit_price}, 类别: {product.category}")
            # 查询对应的库存
            inventory = db.query(Inventory).filter(Inventory.product_id == product.product_id).first()
            if inventory:
                print(f"  库存数量: {inventory.quantity}, 位置: {inventory.location}")

        print("\n=== 订单数据 ===")
        orders = db.query(Order).all()
        for order in orders:
            user = db.query(User).filter(User.user_id == order.user_id).first()
            product = db.query(Product).filter(Product.product_id == order.product_id).first()
            print(f"订单ID: {order.order_id}, 用户: {user.username if user else '未知'}")
            print(f"  产品: {product.product_name if product else '未知'}, 数量: {order.quantity}, 总金额: {order.total_amount}, 状态: {order.status}")

        print("\n=== 财务账户数据 ===")
        accounts = db.query(FinancialAccount).all()
        for account in accounts:
            print(f"账户: {account.account_name}, 类型: {account.account_type}, 余额: {account.balance} {account.currency}")

        print("\n=== 最近交易记录 ===")
        transactions = db.query(Transaction).order_by(Transaction.transaction_date.desc()).limit(5).all()
        for trans in transactions:
            account = db.query(FinancialAccount).filter(FinancialAccount.account_id == trans.account_id).first()
            print(f"交易: {trans.description}, 类型: {trans.transaction_type}, 金额: {trans.amount}")
            print(f"  账户: {account.account_name if account else '未知'}, 日期: {trans.transaction_date}")

        print("\n=== 部门预算 ===")
        budgets = db.query(Budget).all()
        for budget in budgets:
            print(f"部门: {budget.department}, 类别: {budget.category}")
            print(f"  预算金额: {budget.amount}, 实际支出: {budget.actual_amount}")
            print(f"  执行率: {(budget.actual_amount/budget.amount*100):.2f}%")

    except Exception as e:
        print(f"查询数据时出错: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    view_data() 