// 用户类型
export interface User {
  user_id: number;
  username: string;
  email: string;
  role: string;
  created_at?: string;
}

// 产品类型
export interface Product {
  product_id: number;
  name: string;
  description: string;
  price: number;
  stock: number;
  category: string;
  supplier_id?: number;
  created_at: string;
  updated_at: string;
}

// 库存类型
export interface Inventory {
  inventory_id: number;
  product_id: number;
  quantity: number;
  location: string;
  last_updated?: string;
  created_at?: string;
}

// 订单类型
export interface Order {
  order_id: number;
  user_id: number;
  product_id: number;
  quantity: number;
  total_amount: number;
  status: string;
  created_at?: string;
}

// 供应商类型
export interface Supplier {
  supplier_id: number;
  supplier_name: string;
  contact_person: string;
  phone: string;
  email: string;
  address: string;
  created_at?: string;
}

// 财务账户类型
export interface FinancialAccount {
  account_id: number;
  account_name: string;
  account_type: 'cash' | 'bank' | 'credit' | 'other';
  currency: string;
  balance: number;
  created_at: string;
  updated_at: string;
}

// 交易记录类型
export interface Transaction {
  transaction_id: number;
  account_id: number;
  transaction_type: string;
  amount: number;
  description: string;
  transaction_date: string;
  created_at?: string;
  updated_at?: string;
}

// 预算类型
export interface Budget {
  budget_id: number;
  department: string;
  category: string;
  amount: number;
  period_start: string;
  period_end: string;
  actual_amount?: number;
  status: string;
  created_at?: string;
  updated_at?: string;
}

// API响应类型
export interface ApiResponse<T> {
  code: number;
  data: T;
  message: string;
}

// 产品表单类型定义
export interface ProductForm {
  name: string;
  description: string;
  price: number;
  stock: number;
  category: string;
  supplier_id?: number;
}

export interface TransferRequest {
  from_account_id: number;
  to_account_id: number;
  amount: number;
  description: string;
}

export interface UserInfo {
  id: number;
  username: string;
  email: string;
  role: string;
  created_at: string;
  last_login?: string;
}

export interface LoginResponse {
  token: string;
  userInfo: UserInfo;
} 