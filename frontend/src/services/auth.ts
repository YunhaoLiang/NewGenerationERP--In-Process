import axios from 'axios'
import { ElMessage } from 'element-plus'

const API_BASE_URL = 'http://localhost:8000'

export interface LoginForm {
  username: string
  password: string
}

export interface User {
  id: number
  username: string
  role: string
}

export interface LoginResponse {
  token: string
  user: User
}

export async function login(form: LoginForm): Promise<LoginResponse> {
  try {
    const response = await axios.post(`${API_BASE_URL}/api/auth/login`, form)
    const { access_token, user } = response.data
    localStorage.setItem('token', access_token)
    return { 
      token: access_token,
      user: user
    }
  } catch (error) {
    if (axios.isAxiosError(error)) {
      const message = error.response?.data?.detail || '登录失败'
      ElMessage.error(message)
    } else {
      ElMessage.error('登录失败')
    }
    throw error
  }
} 