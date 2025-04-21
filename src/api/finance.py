from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
from decimal import Decimal

from src.config.database import get_db
from src.models.models import (
    FinancialAccount, 
    Transaction, 
    FinancialReport, 
    Budget,
    TransactionType,
    AccountType
)

router = APIRouter(prefix="/finance", tags=["finance"])

# Pydantic models
class AccountCreate(BaseModel):
    account_name: str
    account_type: str
    balance: Decimal = Decimal('0')
    currency: str = 'CNY'
    description: Optional[str] = None

class AccountResponse(BaseModel):
    account_id: int
    account_name: str
    account_type: str
    balance: Decimal
    currency: str
    description: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class TransactionCreate(BaseModel):
    account_id: int
    transaction_type: str
    amount: Decimal
    description: Optional[str] = None
    reference_type: Optional[str] = None
    reference_id: Optional[int] = None
    transaction_date: datetime = None

class TransactionResponse(BaseModel):
    transaction_id: int
    account_id: int
    transaction_type: str
    amount: Decimal
    description: Optional[str]
    reference_type: Optional[str]
    reference_id: Optional[int]
    transaction_date: datetime
    created_at: datetime

    class Config:
        orm_mode = True

class ReportCreate(BaseModel):
    report_type: str
    report_date: datetime
    period_start: datetime
    period_end: datetime
    content: str

class ReportResponse(BaseModel):
    report_id: int
    report_type: str
    report_date: datetime
    period_start: datetime
    period_end: datetime
    content: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class BudgetCreate(BaseModel):
    department: str
    category: str
    amount: Decimal
    period_start: datetime
    period_end: datetime
    status: str = 'active'

class BudgetResponse(BaseModel):
    budget_id: int
    department: str
    category: str
    amount: Decimal
    period_start: datetime
    period_end: datetime
    actual_amount: Decimal
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# API endpoints
@router.post("/accounts", response_model=AccountResponse)
async def create_account(account: AccountCreate, db: Session = Depends(get_db)):
    """创建财务账户"""
    db_account = FinancialAccount(**account.dict())
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account

@router.get("/accounts", response_model=List[AccountResponse])
async def get_accounts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """获取账户列表"""
    accounts = db.query(FinancialAccount).offset(skip).limit(limit).all()
    return accounts

@router.get("/accounts/{account_id}", response_model=AccountResponse)
async def get_account(account_id: int, db: Session = Depends(get_db)):
    """获取账户详情"""
    account = db.query(FinancialAccount).filter(FinancialAccount.account_id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account

@router.post("/transactions", response_model=TransactionResponse)
async def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    """创建交易记录"""
    if not transaction.transaction_date:
        transaction.transaction_date = datetime.now()
    
    # 检查账户是否存在
    account = db.query(FinancialAccount).filter(FinancialAccount.account_id == transaction.account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    # 创建交易记录
    db_transaction = Transaction(**transaction.dict())
    db.add(db_transaction)
    
    # 更新账户余额
    if transaction.transaction_type in [TransactionType.INCOME.value, TransactionType.LOAN.value]:
        account.balance += transaction.amount
    elif transaction.transaction_type in [TransactionType.EXPENSE.value, TransactionType.REPAYMENT.value]:
        account.balance -= transaction.amount
    
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

@router.get("/transactions", response_model=List[TransactionResponse])
async def get_transactions(
    skip: int = 0, 
    limit: int = 100, 
    account_id: Optional[int] = None,
    transaction_type: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    """获取交易记录列表"""
    query = db.query(Transaction)
    
    if account_id:
        query = query.filter(Transaction.account_id == account_id)
    if transaction_type:
        query = query.filter(Transaction.transaction_type == transaction_type)
    if start_date:
        query = query.filter(Transaction.transaction_date >= start_date)
    if end_date:
        query = query.filter(Transaction.transaction_date <= end_date)
    
    transactions = query.offset(skip).limit(limit).all()
    return transactions

@router.post("/reports", response_model=ReportResponse)
async def create_report(report: ReportCreate, db: Session = Depends(get_db)):
    """创建财务报表"""
    db_report = FinancialReport(**report.dict())
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report

@router.get("/reports", response_model=List[ReportResponse])
async def get_reports(
    skip: int = 0,
    limit: int = 100,
    report_type: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    """获取财务报表列表"""
    query = db.query(FinancialReport)
    
    if report_type:
        query = query.filter(FinancialReport.report_type == report_type)
    if start_date:
        query = query.filter(FinancialReport.report_date >= start_date)
    if end_date:
        query = query.filter(FinancialReport.report_date <= end_date)
    
    reports = query.offset(skip).limit(limit).all()
    return reports

@router.post("/budgets", response_model=BudgetResponse)
async def create_budget(budget: BudgetCreate, db: Session = Depends(get_db)):
    """创建预算"""
    db_budget = Budget(**budget.dict())
    db.add(db_budget)
    db.commit()
    db.refresh(db_budget)
    return db_budget

@router.get("/budgets", response_model=List[BudgetResponse])
async def get_budgets(
    skip: int = 0,
    limit: int = 100,
    department: Optional[str] = None,
    category: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """获取预算列表"""
    query = db.query(Budget)
    
    if department:
        query = query.filter(Budget.department == department)
    if category:
        query = query.filter(Budget.category == category)
    if status:
        query = query.filter(Budget.status == status)
    
    budgets = query.offset(skip).limit(limit).all()
    return budgets

@router.get("/reports/balance-sheet")
async def get_balance_sheet(date: Optional[datetime] = None, db: Session = Depends(get_db)):
    """获取资产负债表"""
    if not date:
        date = datetime.now()
    
    # 获取所有账户余额
    accounts = db.query(FinancialAccount).all()
    
    # 计算资产和负债
    assets = sum(account.balance for account in accounts 
                if account.account_type in [AccountType.CASH.value, AccountType.BANK.value, AccountType.RECEIVABLE.value])
    liabilities = sum(account.balance for account in accounts 
                     if account.account_type == AccountType.PAYABLE.value)
    equity = assets - liabilities
    
    return {
        "date": date,
        "assets": assets,
        "liabilities": liabilities,
        "equity": equity,
        "accounts": [
            {
                "account_name": account.account_name,
                "account_type": account.account_type,
                "balance": account.balance
            }
            for account in accounts
        ]
    }

@router.get("/reports/income-statement")
async def get_income_statement(
    start_date: datetime,
    end_date: datetime,
    db: Session = Depends(get_db)
):
    """获取利润表"""
    # 获取指定期间的收入和支出
    transactions = db.query(Transaction).filter(
        Transaction.transaction_date.between(start_date, end_date)
    ).all()
    
    income = sum(t.amount for t in transactions if t.transaction_type == TransactionType.INCOME.value)
    expenses = sum(t.amount for t in transactions if t.transaction_type == TransactionType.EXPENSE.value)
    profit = income - expenses
    
    return {
        "period_start": start_date,
        "period_end": end_date,
        "income": income,
        "expenses": expenses,
        "profit": profit,
        "transactions": [
            {
                "type": t.transaction_type,
                "amount": t.amount,
                "description": t.description,
                "date": t.transaction_date
            }
            for t in transactions
        ]
    }

@router.get("/reports/cash-flow")
async def get_cash_flow(
    start_date: datetime,
    end_date: datetime,
    db: Session = Depends(get_db)
):
    """获取现金流量表"""
    # 获取现金账户的交易记录
    cash_accounts = db.query(FinancialAccount).filter(
        FinancialAccount.account_type.in_([AccountType.CASH.value, AccountType.BANK.value])
    ).all()
    
    cash_transactions = db.query(Transaction).filter(
        Transaction.account_id.in_([acc.account_id for acc in cash_accounts]),
        Transaction.transaction_date.between(start_date, end_date)
    ).all()
    
    operating_cash_flow = sum(t.amount for t in cash_transactions 
                            if t.transaction_type in [TransactionType.INCOME.value, TransactionType.EXPENSE.value])
    investing_cash_flow = sum(t.amount for t in cash_transactions 
                            if t.transaction_type == TransactionType.INVESTMENT.value)
    financing_cash_flow = sum(t.amount for t in cash_transactions 
                            if t.transaction_type in [TransactionType.LOAN.value, TransactionType.REPAYMENT.value])
    
    return {
        "period_start": start_date,
        "period_end": end_date,
        "operating_cash_flow": operating_cash_flow,
        "investing_cash_flow": investing_cash_flow,
        "financing_cash_flow": financing_cash_flow,
        "net_cash_flow": operating_cash_flow + investing_cash_flow + financing_cash_flow,
        "transactions": [
            {
                "type": t.transaction_type,
                "amount": t.amount,
                "description": t.description,
                "date": t.transaction_date
            }
            for t in cash_transactions
        ]
    } 