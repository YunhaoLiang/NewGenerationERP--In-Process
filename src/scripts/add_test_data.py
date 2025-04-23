from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from src.config.database import SessionLocal
from src.models.models import (
    User, Product, Inventory, Order, Supplier,
    FinancialAccount, Transaction, Budget
)

def add_test_users(session: Session):
    """添加测试用户"""
    users = [
        User(
            username="admin",
            email="admin@erp.com",
            password="admin123",  # 实际应用中应该加密
            role="admin"
        ),
        User(
            username="manager",
            email="manager@erp.com",
            password="manager123",
            role="manager"
        ),
        User(
            username="staff",
            email="staff@erp.com",
            password="staff123",
            role="staff"
        )
    ]
    session.add_all(users)
    return users

def add_test_products(session: Session):
    """添加测试产品"""
    products = [
        Product(
            product_name="ThinkPad X1 Carbon",
            unit_price=12999.00,
            description="14寸商务笔记本，i7处理器，16GB内存",
            category="laptop"
        ),
        Product(
            product_name="Dell XPS 15",
            unit_price=15999.00,
            description="15寸工作站，i9处理器，32GB内存",
            category="laptop"
        ),
        Product(
            product_name="机械键盘",
            unit_price=599.00,
            description="Cherry轴机械键盘",
            category="accessories"
        )
    ]
    session.add_all(products)
    return products

def add_test_inventory(session: Session, products):
    """添加测试库存"""
    inventory_items = [
        Inventory(
            product_id=products[0].product_id,
            quantity=50,
            location="北京仓库"
        ),
        Inventory(
            product_id=products[1].product_id,
            quantity=30,
            location="上海仓库"
        ),
        Inventory(
            product_id=products[2].product_id,
            quantity=200,
            location="深圳仓库"
        )
    ]
    session.add_all(inventory_items)

def add_test_suppliers(session: Session):
    """添加测试供应商"""
    suppliers = [
        Supplier(
            supplier_name="联想中国",
            contact_person="王经理",
            phone="13811111111",
            email="lenovo@supplier.com",
            address="北京市海淀区联想大厦"
        ),
        Supplier(
            supplier_name="戴尔中国",
            contact_person="李经理",
            phone="13822222222",
            email="dell@supplier.com",
            address="上海市浦东新区张江高科技园区"
        )
    ]
    session.add_all(suppliers)

def add_test_financial_accounts(session: Session):
    """添加测试财务账户"""
    accounts = [
        FinancialAccount(
            account_name="运营资金账户",
            account_type="asset",
            balance=2000000.00,
            currency="CNY"
        ),
        FinancialAccount(
            account_name="销售收入账户",
            account_type="revenue",
            balance=500000.00,
            currency="CNY"
        ),
        FinancialAccount(
            account_name="采购支出账户",
            account_type="expense",
            balance=300000.00,
            currency="CNY"
        )
    ]
    session.add_all(accounts)
    return accounts

def add_test_transactions(session: Session, accounts):
    """添加测试交易记录"""
    transactions = [
        Transaction(
            account_id=accounts[0].account_id,
            transaction_type="income",
            amount=50000.00,
            description="销售收入",
            transaction_date=datetime.now()
        ),
        Transaction(
            account_id=accounts[1].account_id,
            transaction_type="expense",
            amount=30000.00,
            description="采购支出",
            transaction_date=datetime.now() - timedelta(days=1)
        )
    ]
    session.add_all(transactions)

def add_test_orders(session: Session, users, products):
    """添加测试订单"""
    orders = [
        Order(
            user_id=users[0].user_id,
            product_id=products[0].product_id,
            quantity=2,
            total_amount=25998.00,
            status="completed",
            created_at=datetime.now() - timedelta(days=5)
        ),
        Order(
            user_id=users[1].user_id,
            product_id=products[1].product_id,
            quantity=1,
            total_amount=15999.00,
            status="processing",
            created_at=datetime.now()
        )
    ]
    session.add_all(orders)

def add_test_budgets(session: Session):
    """添加测试预算"""
    current_month = datetime.now().replace(day=1)
    next_month = current_month + timedelta(days=32)
    next_month = next_month.replace(day=1)
    
    budgets = [
        Budget(
            department="IT部门",
            category="设备采购",
            amount=100000.00,
            actual_amount=80000.00,
            period_start=current_month,
            period_end=next_month - timedelta(days=1),
            status="active",
            created_at=datetime.now(),
            updated_at=datetime.now()
        ),
        Budget(
            department="销售部门",
            category="营销支出",
            amount=50000.00,
            actual_amount=30000.00,
            period_start=current_month,
            period_end=next_month - timedelta(days=1),
            status="active",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
    ]
    session.add_all(budgets)

def main():
    """主函数：添加所有测试数据"""
    session = SessionLocal()
    try:
        # 清空现有数据（谨慎使用！）
        session.query(Transaction).delete()
        session.query(Order).delete()
        session.query(Budget).delete()
        session.query(Inventory).delete()
        session.query(Product).delete()
        session.query(User).delete()
        session.query(Supplier).delete()
        session.query(FinancialAccount).delete()
        
        # 添加测试数据
        print("正在添加测试数据...")
        users = add_test_users(session)
        products = add_test_products(session)
        add_test_inventory(session, products)
        add_test_suppliers(session)
        accounts = add_test_financial_accounts(session)
        add_test_transactions(session, accounts)
        add_test_orders(session, users, products)
        add_test_budgets(session)
        
        # 提交事务
        session.commit()
        print("测试数据添加成功！")
        
    except Exception as e:
        session.rollback()
        print(f"添加测试数据时发生错误: {str(e)}")
    finally:
        session.close()

if __name__ == "__main__":
    main() 