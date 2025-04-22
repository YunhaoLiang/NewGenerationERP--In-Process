import request from '@/utils/request'

export interface LoginRequest {
  username: string
  password: string
}

export interface LoginResponse {
  token: string
}

export interface UserInfo {
  id: number
  username: string
  email: string
  role: string
  avatar?: string
  created_at: string
  updated_at: string
}

// 登录
export const apiLogin = (data: LoginRequest): Promise<LoginResponse> => {
  return request({
    url: '/api/auth/login',
    method: 'post',
    data
  })
}

// 登出
export const apiLogout = () => {
  return request({
    url: '/api/auth/logout',
    method: 'post'
  })
}

// 获取用户信息
export const apiGetUserInfo = (): Promise<UserInfo> => {
  return request({
    url: '/api/auth/user-info',
    method: 'get'
  })
}

// 修改密码
export const apiChangePassword = (data: { oldPassword: string; newPassword: string }) => {
  return request({
    url: '/api/auth/change-password',
    method: 'post',
    data
  })
} 