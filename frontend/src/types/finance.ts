export interface Account {
  id: number;
  name: string;
  type: 'savings' | 'checking' | 'investment';
  balance: number;
  currency: string;
  created_at: string;
  updated_at: string;
  description?: string;
  status: 'active' | 'inactive' | 'frozen';
}

export interface Transaction {
  id: number;
  from_account_id: number;
  to_account_id: number;
  amount: number;
  currency: string;
  type: 'transfer' | 'deposit' | 'withdrawal';
  status: 'pending' | 'completed' | 'failed';
  created_at: string;
  description?: string;
}

export interface Report {
  id: number;
  type: 'income' | 'expense' | 'balance';
  period: string;
  data: any;
  generated_at: string;
  status: 'generated' | 'processing' | 'failed';
}

export interface TransferRequest {
  from_account_id: number;
  to_account_id: number;
  amount: number;
  description?: string;
}

export interface AccountBalance {
  account_id: number;
  current_balance: number;
  available_balance: number;
  currency: string;
  last_updated: string;
}

export interface FinancialSummary {
  total_assets: number;
  total_liabilities: number;
  net_worth: number;
  currency: string;
  period: string;
  last_updated: string;
} 