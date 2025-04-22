import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.config.database import SessionLocal
from src.models.models import User, Product, Inventory, Order, Supplier, FinancialAccount, Transaction, Budget
from datetime import datetime, timedelta

def create_test_data():
    """创建测试数据"""
    db = SessionLocal()
    try:
        # 检查是否已存在数据
        existing_users = db.query(User).count()
        if existing_users > 0:
            print("用户数据已存在，跳过创建")
        else:
            # 创建用户数据
            users = [
                User(username="admin", email="admin@example.com", role="admin"),
                User(username="manager", email="manager@example.com", role="manager"),
                User(username="sales1", email="sales1@example.com", role="sales"),
                User(username="sales2", email="sales2@example.com", role="sales"),
                User(username="purchase", email="purchase@example.com", role="purchase")
            ]
            db.add_all(users)
            db.commit()
            print("用户数据创建成功")

        # 检查财务账户
        existing_accounts = db.query(FinancialAccount).count()
        if existing_accounts > 0:
            print("财务账户数据已存在，跳过创建")
        else:
            # 创建财务账户
            accounts = [
                FinancialAccount(
                    account_name="现金账户",
                    account_type="asset",
                    balance=100000.00,
                    currency="CNY"
                ),
                FinancialAccount(
                    account_name="银行账户",
                    account_type="asset",
                    balance=500000.00,
                    currency="CNY"
                ),
                FinancialAccount(
                    account_name="应付账款",
                    account_type="liability",
                    balance=200000.00,
                    currency="CNY"
                )
            ]
            db.add_all(accounts)
            db.commit()
            print("财务账户数据创建成功")

        # 检查交易记录
        existing_transactions = db.query(Transaction).count()
        if existing_transactions > 0:
            print("交易数据已存在，跳过创建")
        else:
            # 创建交易记录
            transactions = [
                Transaction(
                    account_id=1,
                    transaction_type="income",
                    amount=50000.00,
                    description="销售订单收入"
                ),
                Transaction(
                    account_id=2,
                    transaction_type="expense",
                    amount=30000.00,
                    description="采购支出"
                ),
                Transaction(
                    account_id=3,
                    transaction_type="transfer",
                    amount=10000.00,
                    description="内部转账"
                )
            ]
            db.add_all(transactions)
            db.commit()
            print("交易数据创建成功")

        # 检查预算记录
        existing_budgets = db.query(Budget).count()
        if existing_budgets > 0:
            print("预算数据已存在，跳过创建")
        else:
            # 创建预算记录
            budgets = [
                Budget(
                    department="销售部",
                    category="市场推广",
                    amount=50000.00,
                    period_start=datetime.now(),
                    period_end=datetime.now() + timedelta(days=30),
                    status="active"
                ),
                Budget(
                    department="采购部",
                    category="原材料采购",
                    amount=200000.00,
                    period_start=datetime.now(),
                    period_end=datetime.now() + timedelta(days=30),
                    status="active"
                )
            ]
            db.add_all(budgets)
            db.commit()
            print("预算数据创建成功")

    except Exception as e:
        print(f"创建测试数据时出错：{str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    create_test_data() 