import type { Account, Transaction, TransferRequest, AccountBalance, FinancialSummary, Report } from '../../types/finance'
import request from '../request'

// 获取账户列表
export const getAccounts = () => {
  return request.get<Account[]>('/api/finance/accounts')
}

// 获取单个账户详情
export const getAccountById = (id: number) => {
  return request.get<Account>(`/api/finance/accounts/${id}`)
}

// 创建新账户
export const createAccount = (data: Partial<Account>) => {
  return request.post<Account>('/api/finance/accounts', data)
}

// 更新账户信息
export const updateAccount = (id: number, data: Partial<Account>) => {
  return request.put<Account>(`/api/finance/accounts/${id}`, data)
}

// 删除账户
export const deleteAccount = (id: string) => {
  return request.delete(`/api/finance/accounts/${id}`)
}

// 获取账户余额
export const getAccountBalance = (accountId: number) => {
  return request.get<AccountBalance>(`/api/finance/accounts/${accountId}/balance`)
}

// 转账
export const transferFunds = (data: TransferRequest) => {
  return request.post<Transaction>('/api/finance/transfer', data)
}

// 获取交易记录
export const getTransactions = (params?: { 
  account_id?: number
  type?: Transaction['type']
  start_date?: string
  end_date?: string
}) => {
  return request.get<Transaction[]>('/api/finance/transactions', { params })
}

// 获取财务报表
export const getFinancialReport = (params: {
  type: Report['type']
  period: string
}) => {
  return request.get<Report>('/api/finance/reports', { params })
}

// 获取财务摘要
export const getFinancialSummary = (period: string) => {
  return request.get<FinancialSummary>('/api/finance/summary', { 
    params: { period } 
  })
} 