import request from '../request'

export interface Product {
  id: number
  name: string
  description: string
  price: number
  stock: number
  category: string
  created_at: string
  updated_at: string
}

export interface ProductListResponse {
  items: Product[]
  total: number
}

export interface CreateProductRequest {
  name: string
  description: string
  price: number
  stock: number
  category: string
}

export interface UpdateProductRequest extends Partial<CreateProductRequest> {}

// 获取产品列表
export function getProducts(params: { page: number; limit: number }) {
  return request({
    url: '/api/products',
    method: 'get',
    params
  })
}

// 获取单个产品详情
export function getProduct(id: number) {
  return request({
    url: `/api/products/${id}`,
    method: 'get'
  })
}

// 创建新产品
export function createProduct(data: CreateProductRequest) {
  return request({
    url: '/api/products',
    method: 'post',
    data
  })
}

// 更新产品
export function updateProduct(id: number, data: UpdateProductRequest) {
  return request({
    url: `/api/products/${id}`,
    method: 'put',
    data
  })
}

// 删除产品
export function deleteProduct(id: number) {
  return request({
    url: `/api/products/${id}`,
    method: 'delete'
  })
} 