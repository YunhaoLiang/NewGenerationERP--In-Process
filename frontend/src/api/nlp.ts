import request from '@/utils/request'

export interface NLPRequest {
  text: string
  requireAgents?: boolean
}

export interface AgentInfo {
  name: string
  type: string
  status: string
  priority: number
}

export interface FinancialPlan {
  estimated_revenue: number
  estimated_cost: number
  estimated_profit: number
  profit_margin: number
}

export interface ProductionPlan {
  phase: string
  start_date: string
  end_date: string
  quantity: number
}

export interface ProcurementPlan {
  item: string
  quantity: number
  estimated_cost: number
  supplier: string
}

export interface OrderInfo {
  order_no: string
  customer_name: string
  total_amount: number
  delivery_date: string
  shipping_address: string
}

export interface NLPResponse {
  status: string
  result: {
    type: string
    content: string
    details: {
      order?: OrderInfo
      production_plan?: ProductionPlan[]
      procurement_plan?: ProcurementPlan[]
      financial_plan?: FinancialPlan
    }
  }
  message: string
  timestamp: string
  agents?: AgentInfo[]
}

export const processNLPRequest = (data: NLPRequest): Promise<NLPResponse> => {
  return request.post('/nlp/process', data)
} 