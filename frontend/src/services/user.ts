import api from './api'

export interface LoginForm {
  username: string
  password: string
}

export interface UserInfo {
  user_id: number
  username: string
  email: string
  role: string
  created_at: string
}

export const login = (data: LoginForm) => {
  return api.post('/auth/login', data)
}

export const logout = () => {
  return api.post('/auth/logout')
}

export const getUserInfo = () => {
  return api.get<UserInfo>('/users/me')
}

export const register = (data: {
  username: string
  password: string
  email: string
  role: string
}) => {
  return api.post('/users/register', data)
}

export const updateUserInfo = (userId: number, data: {
  username?: string
  email?: string
  role?: string
}) => {
  return api.put(`/users/${userId}`, data)
}

export const changePassword = (data: {
  old_password: string
  new_password: string
}) => {
  return api.post('/users/change-password', data)
} 