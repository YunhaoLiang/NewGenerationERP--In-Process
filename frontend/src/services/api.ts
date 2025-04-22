import axios from 'axios'
import { ElMessage } from 'element-plus'

const api = axios.create({
  baseURL: 'http://localhost:8001', // 修改为正确的端口
  timeout: 50000  // 增加到50秒
})

// 请求拦截器
api.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// 响应拦截器
api.interceptors.response.use(
  response => response.data,
  error => {
    if (error.response) {
      const errorData = error.response.data
      switch (error.response.status) {
        case 401:
          // 未授权，跳转到登录页
          localStorage.removeItem('token')
          window.location.href = '/login'
          break
        case 403:
          ElMessage.error('没有权限访问')
          break
        case 404:
          ElMessage.error('请求的资源不存在')
          break
        case 500:
          // 显示详细的错误信息
          const errorMessage = errorData.detail?.message || errorData.detail || '服务器错误，请稍后重试'
          ElMessage.error(errorMessage)
          break
        default:
          ElMessage.error(errorData.detail?.message || errorData.detail || '请求失败，请重试')
      }
    } else if (error.code === 'ECONNABORTED') {
      ElMessage.error('请求超时，这可能是因为处理较为复杂，请稍后重试')
    } else {
      ElMessage.error('网络错误，请检查网络连接')
    }
    return Promise.reject(error)
  }
)

export default api 