<template>
  <div class="inventory-container">
    <div class="header-actions">
      <el-button type="primary" @click="handleRefresh">
        <el-icon><Refresh /></el-icon>刷新库存
      </el-button>
      <el-input
        v-model="searchQuery"
        placeholder="搜索产品名称"
        class="search-input"
        clearable
        @clear="handleSearch"
        @input="handleSearch"
      >
        <template #prefix>
          <el-icon><Search /></el-icon>
        </template>
      </el-input>
    </div>

    <el-table
      v-loading="loading"
      :data="inventoryList"
      border
      style="width: 100%"
    >
      <el-table-column prop="inventory_id" label="库存ID" width="100" />
      <el-table-column prop="product_name" label="产品名称" />
      <el-table-column prop="quantity" label="数量" width="120">
        <template #default="{ row }">
          <el-input-number
            v-model="row.quantity"
            :min="0"
            @change="(value) => handleQuantityChange(row, value)"
          />
        </template>
      </el-table-column>
      <el-table-column prop="location" label="库位" />
      <el-table-column prop="last_updated" label="最后更新时间" width="180">
        <template #default="{ row }">
          {{ formatDate(row.last_updated) }}
        </template>
      </el-table-column>
      <el-table-column label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="getStockStatus(row.quantity).type">
            {{ getStockStatus(row.quantity).label }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="200" fixed="right">
        <template #default="{ row }">
          <el-button-group>
            <el-button
              type="primary"
              @click="handleMove(row)"
            >
              移库
            </el-button>
            <el-button
              type="warning"
              @click="handleAdjust(row)"
            >
              调整
            </el-button>
          </el-button-group>
        </template>
      </el-table-column>
    </el-table>

    <!-- 移库对话框 -->
    <el-dialog
      v-model="moveDialogVisible"
      title="移库"
      width="400px"
    >
      <el-form
        ref="moveFormRef"
        :model="moveForm"
        :rules="moveRules"
        label-width="100px"
      >
        <el-form-item label="目标库位" prop="location">
          <el-input v-model="moveForm.location" />
        </el-form-item>
        <el-form-item label="移动数量" prop="quantity">
          <el-input-number
            v-model="moveForm.quantity"
            :min="1"
            :max="currentItem?.quantity"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="moveDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitMove">
            确认
          </el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 调整对话框 -->
    <el-dialog
      v-model="adjustDialogVisible"
      title="库存调整"
      width="400px"
    >
      <el-form
        ref="adjustFormRef"
        :model="adjustForm"
        :rules="adjustRules"
        label-width="100px"
      >
        <el-form-item label="调整数量" prop="quantity">
          <el-input-number
            v-model="adjustForm.quantity"
            :min="0"
          />
        </el-form-item>
        <el-form-item label="调整原因" prop="reason">
          <el-input
            v-model="adjustForm.reason"
            type="textarea"
            :rows="3"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="adjustDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitAdjust">
            确认
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Refresh, Search } from '@element-plus/icons-vue'
import type { FormInstance } from 'element-plus'
import { inventoryApi } from '@/api/modules/inventory'
import type { Inventory } from '@/types/models'

// 状态
const loading = ref(false)
const searchQuery = ref('')
const inventoryList = ref<Inventory[]>([])
const moveDialogVisible = ref(false)
const adjustDialogVisible = ref(false)
const currentItem = ref<Inventory | null>(null)

// 移库表单
const moveFormRef = ref<FormInstance>()
const moveForm = ref({
  location: '',
  quantity: 1
})

// 调整表单
const adjustFormRef = ref<FormInstance>()
const adjustForm = ref({
  quantity: 0,
  reason: ''
})

// 表单验证规则
const moveRules = {
  location: [
    { required: true, message: '请输入目标库位', trigger: 'blur' }
  ],
  quantity: [
    { required: true, message: '请输入移动数量', trigger: 'blur' }
  ]
}

const adjustRules = {
  quantity: [
    { required: true, message: '请输入调整数量', trigger: 'blur' }
  ],
  reason: [
    { required: true, message: '请输入调整原因', trigger: 'blur' }
  ]
}

// 获取库存状态
const getStockStatus = (quantity: number) => {
  if (quantity <= 0) {
    return { type: 'danger', label: '无库存' }
  }
  if (quantity < 10) {
    return { type: 'warning', label: '低库存' }
  }
  return { type: 'success', label: '正常' }
}

// 格式化日期
const formatDate = (date: string) => {
  return new Date(date).toLocaleString()
}

// 获取库存列表
const fetchInventory = async () => {
  try {
    loading.value = true
    const response = await inventoryApi.getInventoryList()
    inventoryList.value = response.data
  } catch (error) {
    ElMessage.error('获取库存列表失败')
  } finally {
    loading.value = false
  }
}

// 搜索处理
const handleSearch = () => {
  // 实现搜索逻辑
  console.log('搜索:', searchQuery.value)
}

// 刷新库存
const handleRefresh = () => {
  fetchInventory()
}

// 数量变更处理
const handleQuantityChange = async (row: Inventory, value: number) => {
  try {
    await inventoryApi.updateInventory(row.inventory_id, { quantity: value })
    ElMessage.success('更新成功')
  } catch (error) {
    ElMessage.error('更新失败')
    // 回滚数量
    row.quantity = row.quantity
  }
}

// 移库处理
const handleMove = (row: Inventory) => {
  currentItem.value = row
  moveForm.value = {
    location: '',
    quantity: 1
  }
  moveDialogVisible.value = true
}

// 提交移库
const submitMove = async () => {
  if (!moveFormRef.value) return
  
  try {
    await moveFormRef.value.validate()
    // 实现移库逻辑
    moveDialogVisible.value = false
    ElMessage.success('移库成功')
    await fetchInventory()
  } catch (error) {
    ElMessage.error('移库失败')
  }
}

// 调整处理
const handleAdjust = (row: Inventory) => {
  currentItem.value = row
  adjustForm.value = {
    quantity: row.quantity,
    reason: ''
  }
  adjustDialogVisible.value = true
}

// 提交调整
const submitAdjust = async () => {
  if (!adjustFormRef.value) return
  
  try {
    await adjustFormRef.value.validate()
    if (!currentItem.value) return
    
    await inventoryApi.updateInventory(
      currentItem.value.inventory_id,
      { quantity: adjustForm.value.quantity }
    )
    
    adjustDialogVisible.value = false
    ElMessage.success('调整成功')
    await fetchInventory()
  } catch (error) {
    ElMessage.error('调整失败')
  }
}

// 初始化
onMounted(() => {
  fetchInventory()
})
</script>

<style scoped>
.inventory-container {
  padding: 20px;
}

.header-actions {
  margin-bottom: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.search-input {
  width: 300px;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style> 