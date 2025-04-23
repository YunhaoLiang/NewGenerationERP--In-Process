from datetime import datetime
from sqlalchemy.orm import Session
from src.config.database import SessionLocal
from src.models.models import User, Product, Order, Inventory, Supplier, FinancialAccount, Transaction, Budget

def seed_data():
    db = SessionLocal()
    try:
        print("开始添加电脑公司示例数据...")

        # 创建用户
        users = [
            User(username="admin", email="admin@techpc.com", role="admin"),
            User(username="sales_manager", email="sales@techpc.com", role="manager"),
            User(username="technician", email="tech@techpc.com", role="staff"),
            User(username="accountant", email="finance@techpc.com", role="finance")
        ]
        db.bulk_save_objects(users)
        print("用户数据添加成功")

        # 创建供应商
        suppliers = [
            Supplier(supplier_name="英特尔中国", contact_person="张三", phone="13800138000", email="intel@supplier.com", address="上海市浦东新区"),
            Supplier(supplier_name="AMD中国", contact_person="李四", phone="13900139000", email="amd@supplier.com", address="北京市朝阳区"),
            Supplier(supplier_name="华硕电脑", contact_person="王五", phone="13700137000", email="asus@supplier.com", address="深圳市南山区"),
            Supplier(supplier_name="技嘉科技", contact_person="赵六", phone="13600136000", email="gigabyte@supplier.com", address="广州市天河区")
        ]
        db.bulk_save_objects(suppliers)
        print("供应商数据添加成功")

        # 创建产品
        products = [
            Product(product_name="商务办公本 Pro", unit_price=5999.00, description="Intel i5/16GB/512GB SSD", category="笔记本电脑"),
            Product(product_name="游戏本旗舰版", unit_price=9999.00, description="AMD R7/32GB/1TB SSD/RTX4060", category="笔记本电脑"),
            Product(product_name="组装台式机", unit_price=4999.00, description="Intel i5/16GB/500GB SSD/RTX3060", category="台式电脑"),
            Product(product_name="高性能工作站", unit_price=15999.00, description="AMD TR/128GB/2TB SSD/RTX4090", category="工作站"),
            Product(product_name="显示器27寸", unit_price=1999.00, description="2K分辨率/165Hz", category="显示器"),
            Product(product_name="机械键盘", unit_price=399.00, description="红轴/RGB背光", category="配件")
        ]
        db.bulk_save_objects(products)
        print("产品数据添加成功")

        # 提交以获取ID
        db.commit()

        # 创建库存记录
        inventory_items = [
            Inventory(product_id=1, quantity=50, location="A区-笔记本区", last_updated=datetime.now()),
            Inventory(product_id=2, quantity=30, location="A区-笔记本区", last_updated=datetime.now()),
            Inventory(product_id=3, quantity=20, location="B区-台式机区", last_updated=datetime.now()),
            Inventory(product_id=4, quantity=10, location="B区-工作站区", last_updated=datetime.now()),
            Inventory(product_id=5, quantity=100, location="C区-显示器区", last_updated=datetime.now()),
            Inventory(product_id=6, quantity=200, location="D区-配件区", last_updated=datetime.now())
        ]
        db.bulk_save_objects(inventory_items)
        print("库存数据添加成功")

        # 创建财务账户
        accounts = [
            FinancialAccount(account_name="电脑销售收入", account_type="revenue", balance=2000000.00, currency="CNY"),
            FinancialAccount(account_name="配件销售收入", account_type="revenue", balance=500000.00, currency="CNY"),
            FinancialAccount(account_name="硬件采购支出", account_type="expense", balance=1500000.00, currency="CNY"),
            FinancialAccount(account_name="维修服务收入", account_type="revenue", balance=300000.00, currency="CNY"),
            FinancialAccount(account_name="运营费用", account_type="expense", balance=200000.00, currency="CNY"),
            FinancialAccount(account_name="现金", account_type="asset", balance=1000000.00, currency="CNY")
        ]
        db.bulk_save_objects(accounts)
        print("财务账户数据添加成功")

        # 创建一些订单
        orders = [
            Order(user_id=2, product_id=1, quantity=5, total_amount=29995.00, status="completed", created_at=datetime.now()),
            Order(user_id=2, product_id=2, quantity=3, total_amount=29997.00, status="processing", created_at=datetime.now()),
            Order(user_id=2, product_id=3, quantity=10, total_amount=49990.00, status="pending", created_at=datetime.now()),
            Order(user_id=2, product_id=4, quantity=2, total_amount=31998.00, status="completed", created_at=datetime.now()),
            Order(user_id=2, product_id=5, quantity=20, total_amount=39980.00, status="completed", created_at=datetime.now())
        ]
        db.bulk_save_objects(orders)
        print("订单数据添加成功")

        # 创建一些交易记录
        transactions = [
            Transaction(account_id=1, transaction_type="income", amount=29995.00, description="商务本批量销售", transaction_date=datetime.now()),
            Transaction(account_id=1, transaction_type="income", amount=31998.00, description="工作站销售", transaction_date=datetime.now()),
            Transaction(account_id=2, transaction_type="income", amount=39980.00, description="显示器批量销售", transaction_date=datetime.now()),
            Transaction(account_id=3, transaction_type="expense", amount=100000.00, description="CPU批量采购", transaction_date=datetime.now()),
            Transaction(account_id=4, transaction_type="income", amount=5000.00, description="电脑维修服务", transaction_date=datetime.now())
        ]
        db.bulk_save_objects(transactions)
        print("交易记录添加成功")

        # 创建预算
        budgets = [
            Budget(department="销售部", category="产品采购", amount=2000000.00, actual_amount=1500000.00, 
                  period_start=datetime(2024, 1, 1), period_end=datetime(2024, 12, 31), status="active"),
            Budget(department="技术部", category="维修设备", amount=300000.00, actual_amount=150000.00,
                  period_start=datetime(2024, 1, 1), period_end=datetime(2024, 12, 31), status="active"),
            Budget(department="市场部", category="营销推广", amount=500000.00, actual_amount=200000.00,
                  period_start=datetime(2024, 1, 1), period_end=datetime(2024, 12, 31), status="active"),
            Budget(department="售后部", category="配件储备", amount=400000.00, actual_amount=250000.00,
                  period_start=datetime(2024, 1, 1), period_end=datetime(2024, 12, 31), status="active")
        ]
        db.bulk_save_objects(budgets)
        print("预算数据添加成功")

        # 最终提交所有更改
        db.commit()
        print("所有示例数据添加成功！")

    except Exception as e:
        db.rollback()
        print(f"添加示例数据时出错: {str(e)}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_data() 