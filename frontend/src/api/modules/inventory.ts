import { request } from '../index';
import type { Inventory } from '@/types/models';

export const inventoryApi = {
  // 获取库存列表
  getInventoryList() {
    return request.get<Inventory[]>('/inventory');
  },

  // 获取单个库存记录
  getInventoryItem(id: number) {
    return request.get<Inventory>(`/inventory/${id}`);
  },

  // 更新库存
  updateInventory(id: number, data: Partial<Inventory>) {
    return request.put<Inventory>(`/inventory/${id}`, data);
  },

  // 获取指定产品的库存
  getProductInventory(productId: number) {
    return request.get<Inventory[]>('/inventory', { product_id: productId });
  },

  // 获取指定位置的库存
  getLocationInventory(location: string) {
    return request.get<Inventory[]>('/inventory', { location });
  },
}; 