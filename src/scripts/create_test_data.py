import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.config.database import SessionLocal, engine
from src.models.models import User, Product, Inventory, Supplier, Order, FinancialAccount, Transaction, Budget
from datetime import datetime, timedelta
from sqlalchemy import text
from sqlalchemy.orm import Session
from decimal import Decimal

def create_test_data():
    """创建测试数据"""
    with Session(engine) as session:
        try:
            # 检查是否已有数据
            existing_users = session.query(User).count()
            existing_suppliers = session.query(Supplier).count()
            existing_products = session.query(Product).count()
            
            if existing_users == 0:
                # 创建用户
                users = [
                    User(username='admin', password='admin123', email='admin@example.com', role='admin'),
                    User(username='manager', password='manager123', email='manager@example.com', role='manager'),
                    User(username='sales1', password='sales123', email='sales1@example.com', role='sales'),
                    User(username='sales2', password='sales123', email='sales2@example.com', role='sales'),
                    User(username='warehouse1', password='warehouse123', email='warehouse1@example.com', role='warehouse')
                ]
                for user in users:
                    try:
                        session.add(user)
                        session.commit()
                        print(f'已创建用户：{user.username}')
                    except Exception as e:
                        session.rollback()
                        print(f'创建用户 {user.username} 时出错：{str(e)}')
            else:
                print("用户数据已存在，跳过创建")
            
            if existing_suppliers == 0:
                # 创建供应商
                suppliers = [
                    Supplier(supplier_name='联想中国', contact_person='张经理', phone='010-12345678', email='lenovo@example.com', address='北京市海淀区联想大厦'),
                    Supplier(supplier_name='戴尔中国', contact_person='李经理', phone='021-87654321', email='dell@example.com', address='上海市浦东新区陆家嘴'),
                    Supplier(supplier_name='华硕电脑', contact_person='王经理', phone='0755-98765432', email='asus@example.com', address='深圳市南山区科技园'),
                    Supplier(supplier_name='惠普中国', contact_person='刘经理', phone='020-45678901', email='hp@example.com', address='广州市天河区珠江新城'),
                    Supplier(supplier_name='微星科技', contact_person='陈经理', phone='0592-12345678', email='msi@example.com', address='厦门市思明区软件园')
                ]
                for supplier in suppliers:
                    try:
                        session.add(supplier)
                        session.commit()
                        print(f'已创建供应商：{supplier.supplier_name}')
                    except Exception as e:
                        session.rollback()
                        print(f'创建供应商 {supplier.supplier_name} 时出错：{str(e)}')
            else:
                print("供应商数据已存在，跳过创建")
            
            if existing_products == 0:
                # 创建产品
                products = [
                    Product(product_name="ThinkPad X1 Carbon", description="14英寸商务笔记本", unit_price=Decimal("9999.99"), category="笔记本电脑"),
                    Product(product_name="Dell XPS 13", description="13英寸轻薄笔记本", unit_price=Decimal("8999.99"), category="笔记本电脑"),
                    Product(product_name="MacBook Pro", description="13英寸专业笔记本", unit_price=Decimal("12999.99"), category="笔记本电脑"),
                    Product(product_name="HP Spectre x360", description="13.5英寸变形本", unit_price=Decimal("9599.99"), category="笔记本电脑"),
                    Product(product_name="ROG 魔霸新锐", description="17英寸游戏本", unit_price=Decimal("13999.99"), category="笔记本电脑")
                ]
                for product in products:
                    try:
                        session.add(product)
                        session.commit()
                        print(f'已创建产品：{product.product_name}')

                        # 为每个产品创建库存记录
                        inventory = Inventory(
                            product_id=product.product_id,
                            quantity=100,
                            location='A-01-01'
                        )
                        session.add(inventory)
                        session.commit()
                        print(f'已创建库存记录：{inventory.inventory_id}')
                    except Exception as e:
                        session.rollback()
                        print(f'创建产品或库存时出错：{str(e)}')
            else:
                print("产品数据已存在，跳过创建")
            
            # 创建财务账户
            accounts = [
                {'name': '现金账户', 'type': 'asset', 'balance': 1000000.00, 'currency': 'CNY'},
                {'name': '银行账户', 'type': 'asset', 'balance': 5000000.00, 'currency': 'CNY'},
                {'name': '应收账款', 'type': 'asset', 'balance': 200000.00, 'currency': 'CNY'},
                {'name': '应付账款', 'type': 'liability', 'balance': 300000.00, 'currency': 'CNY'},
                {'name': '销售收入', 'type': 'revenue', 'balance': 0.00, 'currency': 'CNY'},
                {'name': '采购支出', 'type': 'expense', 'balance': 0.00, 'currency': 'CNY'}
            ]
            for account_data in accounts:
                try:
                    account = FinancialAccount(
                        account_name=account_data['name'],
                        account_type=account_data['type'],
                        balance=account_data['balance'],
                        currency=account_data['currency']
                    )
                    session.add(account)
                    session.commit()
                    print(f'已创建财务账户：{account.account_name}')
                except Exception as e:
                    session.rollback()
                    print(f'创建财务账户时出错：{str(e)}')

            # 创建预算
            current_year = datetime.now().year
            budgets = [
                {'department': '销售部', 'category': '销售目标', 'amount': 10000000.00, 'period_start': datetime(current_year, 1, 1), 'period_end': datetime(current_year, 12, 31), 'status': 'active'},
                {'department': '采购部', 'category': '采购预算', 'amount': 8000000.00, 'period_start': datetime(current_year, 1, 1), 'period_end': datetime(current_year, 12, 31), 'status': 'active'},
                {'department': '研发部', 'category': '研发投入', 'amount': 2000000.00, 'period_start': datetime(current_year, 1, 1), 'period_end': datetime(current_year, 12, 31), 'status': 'active'},
                {'department': '市场部', 'category': '营销预算', 'amount': 1000000.00, 'period_start': datetime(current_year, 1, 1), 'period_end': datetime(current_year, 12, 31), 'status': 'active'},
                {'department': '行政部', 'category': '日常运营', 'amount': 500000.00, 'period_start': datetime(current_year, 1, 1), 'period_end': datetime(current_year, 12, 31), 'status': 'active'}
            ]
            for budget_data in budgets:
                try:
                    budget = Budget(
                        department=budget_data['department'],
                        category=budget_data['category'],
                        amount=budget_data['amount'],
                        period_start=budget_data['period_start'],
                        period_end=budget_data['period_end'],
                        status=budget_data['status']
                    )
                    session.add(budget)
                    session.commit()
                    print(f'已创建预算：{budget.department} - {budget.category}')
                except Exception as e:
                    session.rollback()
                    print(f'创建预算时出错：{str(e)}')

            # 创建一些交易记录
            transactions = [
                {'account_id': 1, 'type': 'income', 'amount': 50000.00, 'description': '销售收入'},
                {'account_id': 2, 'type': 'expense', 'amount': 30000.00, 'description': '采购支出'},
                {'account_id': 1, 'type': 'transfer', 'amount': 20000.00, 'description': '内部转账'},
                {'account_id': 3, 'type': 'income', 'amount': 15000.00, 'description': '应收账款回收'},
                {'account_id': 4, 'type': 'expense', 'amount': 25000.00, 'description': '支付供应商'}
            ]
            for transaction_data in transactions:
                try:
                    transaction = Transaction(
                        account_id=transaction_data['account_id'],
                        transaction_type=transaction_data['type'],
                        amount=transaction_data['amount'],
                        description=transaction_data['description'],
                        transaction_date=datetime.now()
                    )
                    session.add(transaction)
                    session.commit()
                    print(f'已创建交易记录：{transaction.description}')
                except Exception as e:
                    session.rollback()
                    print(f'创建交易记录时出错：{str(e)}')

            print('测试数据创建完成！')
            
        except Exception as e:
            print(f"创建测试数据时出错：{str(e)}")
            session.rollback()
        finally:
            session.close()

if __name__ == "__main__":
    create_test_data() 