from src.config.database import SessionLocal
from src.models.models import (
    FinancialAccount, Transaction, FinancialReport, Budget,
    TransactionType, AccountType
)

def view_accounts():
    db = SessionLocal()
    accounts = db.query(FinancialAccount).all()
    print("\n=== 财务账户 ===")
    for account in accounts:
        print(f"账户ID: {account.account_id}")
        print(f"账户名称: {account.account_name}")
        print(f"账户类型: {account.account_type}")
        print(f"余额: {account.balance}")
        print(f"货币: {account.currency}")
        print("---")

def view_transactions():
    db = SessionLocal()
    transactions = db.query(Transaction).all()
    print("\n=== 交易记录 ===")
    for transaction in transactions:
        print(f"交易ID: {transaction.transaction_id}")
        print(f"账户ID: {transaction.account_id}")
        print(f"交易类型: {transaction.transaction_type}")
        print(f"金额: {transaction.amount}")
        print(f"描述: {transaction.description}")
        print(f"交易日期: {transaction.transaction_date}")
        print("---")

def view_reports():
    db = SessionLocal()
    reports = db.query(FinancialReport).all()
    print("\n=== 财务报表 ===")
    for report in reports:
        print(f"报告ID: {report.report_id}")
        print(f"报告类型: {report.report_type}")
        print(f"开始日期: {report.start_date}")
        print(f"结束日期: {report.end_date}")
        print(f"内容: {report.content}")
        print("---")

def view_budgets():
    db = SessionLocal()
    budgets = db.query(Budget).all()
    print("\n=== 预算信息 ===")
    for budget in budgets:
        print(f"预算ID: {budget.budget_id}")
        print(f"部门: {budget.department}")
        print(f"类别: {budget.category}")
        print(f"金额: {budget.amount}")
        print(f"状态: {budget.status}")
        print("---")

def view_finance_data():
    """查看所有财务数据"""
    view_accounts()
    view_transactions()
    view_reports()
    view_budgets()

if __name__ == "__main__":
    view_finance_data() 