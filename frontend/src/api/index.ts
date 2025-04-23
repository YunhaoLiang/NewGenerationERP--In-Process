import axios from 'axios';
import { ElMessage } from 'element-plus';
import type { ApiResponse } from '@/types/models';

// 创建 axios 实例
const request = axios.create({
  baseURL: 'http://localhost:8001',  // 移除 /api 前缀，因为后端路由已经包含了
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json'
  }
});

// 请求拦截器
request.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 响应拦截器
request.interceptors.response.use(
  (response) => {
    return response.data;
  },
  (error) => {
    if (error.response) {
      const { status, data } = error.response;
      
      switch (status) {
        case 401:
          ElMessage.error('未授权，请重新登录');
          // 可以在这里处理登出逻辑
          break;
        case 403:
          ElMessage.error('拒绝访问');
          break;
        case 404:
          ElMessage.error('请求的资源不存在');
          break;
        case 500:
          ElMessage.error('服务器错误，请稍后重试');
          break;
        default:
          ElMessage.error(data.message || '发生未知错误');
      }
    } else {
      ElMessage.error('网络错误，请检查您的网络连接');
    }
    return Promise.reject(error);
  }
);

// 导出类型安全的请求函数
export const requestFunctions = {
  get: <T>(url: string, params?: any): Promise<ApiResponse<T>> =>
    request.get(url, { params }),
  
  post: <T>(url: string, data?: any): Promise<ApiResponse<T>> =>
    request.post(url, data),
  
  put: <T>(url: string, data?: any): Promise<ApiResponse<T>> =>
    request.put(url, data),
  
  delete: <T>(url: string): Promise<ApiResponse<T>> =>
    request.delete(url),
};

export default request; 