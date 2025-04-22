import request from '@/api/request'
import { ElMessage } from 'element-plus'
import type { AxiosResponse } from 'axios'

export interface NLPRequest {
  text: string
  requireAgents: boolean
}

export interface NLPResponse {
  status: string
  result: {
    type: string
    content: string
    details: Record<string, any>
    processed_at?: string
  }
  message: string
  timestamp: string
}

export const nlpService = {
  processText(data: NLPRequest): Promise<NLPResponse> {
    return request.post('/api/nlp/process', data)
  }
} 