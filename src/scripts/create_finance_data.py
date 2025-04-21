from src.config.database import SessionLocal
from src.models.models import (
    FinancialAccount, Transaction, FinancialReport, Budget,
    TransactionType, AccountType
)
from datetime import datetime, timedelta

def create_finance_data():
    db = SessionLocal()
    try:
        # 创建财务账户
        accounts = [
            FinancialAccount(
                account_name="现金账户",
                account_type="asset",
                balance=1000000.00,
                currency="CNY"
            ),
            FinancialAccount(
                account_name="银行账户",
                account_type="asset",
                balance=5000000.00,
                currency="CNY"
            ),
            FinancialAccount(
                account_name="应收账款",
                account_type="asset",
                balance=2000000.00,
                currency="CNY"
            ),
            FinancialAccount(
                account_name="应付账款",
                account_type="liability",
                balance=1500000.00,
                currency="CNY"
            ),
            FinancialAccount(
                account_name="销售收入",
                account_type="revenue",
                balance=0.00,
                currency="CNY"
            ),
            FinancialAccount(
                account_name="采购成本",
                account_type="expense",
                balance=0.00,
                currency="CNY"
            )
        ]
        
        for account in accounts:
            db.add(account)
        db.commit()
        
        # 创建交易记录
        transactions = [
            Transaction(
                account_id=1,  # 现金账户
                transaction_type="income",
                amount=19999.98,
                description="销售ThinkPad X1 Carbon",
                transaction_date=datetime.now() - timedelta(days=1)
            ),
            Transaction(
                account_id=6,  # 采购成本
                transaction_type="expense",
                amount=15000.00,
                description="采购ThinkPad X1 Carbon",
                transaction_date=datetime.now() - timedelta(days=2)
            ),
            Transaction(
                account_id=2,  # 银行账户
                transaction_type="income",
                amount=129999.90,
                description="销售MacBook Pro",
                transaction_date=datetime.now() - timedelta(days=3)
            )
        ]
        
        for transaction in transactions:
            db.add(transaction)
        db.commit()
        
        # 创建财务报表
        reports = [
            FinancialReport(
                report_type="balance_sheet",
                start_date=datetime.now() - timedelta(days=30),
                end_date=datetime.now(),
                content="资产负债表内容..."
            ),
            FinancialReport(
                report_type="income_statement",
                start_date=datetime.now() - timedelta(days=30),
                end_date=datetime.now(),
                content="利润表内容..."
            ),
            FinancialReport(
                report_type="cash_flow",
                start_date=datetime.now() - timedelta(days=30),
                end_date=datetime.now(),
                content="现金流量表内容..."
            )
        ]
        
        for report in reports:
            db.add(report)
        db.commit()
        
        # 创建预算
        budgets = [
            Budget(
                department="销售部",
                category="市场推广",
                amount=500000.00,
                status="active"
            ),
            Budget(
                department="采购部",
                category="设备采购",
                amount=1000000.00,
                status="active"
            ),
            Budget(
                department="研发部",
                category="研发投入",
                amount=2000000.00,
                status="active"
            )
        ]
        
        for budget in budgets:
            db.add(budget)
        db.commit()
        
        print("财务测试数据创建完成！")
        
    except Exception as e:
        db.rollback()
        print(f"创建财务测试数据时出错：{str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    create_finance_data() 