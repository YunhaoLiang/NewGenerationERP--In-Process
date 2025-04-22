import axios from 'axios'

// 创建axios实例
const request = axios.create({
  baseURL: 'http://localhost:8001',
  timeout: 10000
})

// 响应拦截器
request.interceptors.response.use(
  (response) => response.data,
  (error) => Promise.reject(error)
)

export default request 