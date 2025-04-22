<template>
  <div class="inventory-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>库存管理</span>
          <div class="header-actions">
            <el-button type="primary" @click="handleStockIn">入库</el-button>
            <el-button type="warning" @click="handleStockOut">出库</el-button>
          </div>
        </div>
      </template>

      <!-- 搜索栏 -->
      <div class="search-bar">
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
        <el-select
          v-model="categoryFilter"
          placeholder="产品类别"
          clearable
          class="filter-select"
          @change="handleSearch"
        >
          <el-option
            v-for="item in categories"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          />
        </el-select>
        <el-select
          v-model="stockStatusFilter"
          placeholder="库存状态"
          clearable
          class="filter-select"
          @change="handleSearch"
        >
          <el-option label="库存充足" value="sufficient" />
          <el-option label="库存不足" value="insufficient" />
          <el-option label="库存告警" value="warning" />
        </el-select>
      </div>

      <!-- 库存表格 -->
      <el-table
        :data="filteredInventory"
        style="width: 100%"
        v-loading="loading"
      >
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="product_name" label="产品名称" />
        <el-table-column prop="category" label="类别" />
        <el-table-column prop="current_stock" label="当前库存" />
        <el-table-column prop="min_stock" label="最低库存" />
        <el-table-column prop="max_stock" label="最高库存" />
        <el-table-column prop="unit" label="单位" width="80" />
        <el-table-column prop="last_updated" label="最后更新时间" />
        <el-table-column label="库存状态" width="120">
          <template #default="{ row }">
            <el-tag :type="getStockStatusType(row)">
              {{ getStockStatusText(row) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200">
          <template #default="{ row }">
            <el-button
              type="primary"
              link
              @click="handleAdjustStock(row)"
            >
              调整库存
            </el-button>
            <el-button
              type="info"
              link
              @click="handleViewHistory(row)"
            >
              查看记录
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="total"
          layout="total, sizes, prev, pager, next"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>

    <!-- 库存调整对话框 -->
    <el-dialog
      v-model="adjustDialogVisible"
      :title="adjustDialogType === 'in' ? '入库' : '出库'"
      width="500px"
    >
      <el-form
        ref="adjustFormRef"
        :model="adjustForm"
        :rules="adjustRules"
        label-width="100px"
      >
        <el-form-item label="产品名称">
          <span>{{ adjustForm.product_name }}</span>
        </el-form-item>
        <el-form-item label="当前库存">
          <span>{{ adjustForm.current_stock }}</span>
        </el-form-item>
        <el-form-item label="调整数量" prop="quantity">
          <el-input-number
            v-model="adjustForm.quantity"
            :min="1"
            :step="1"
            :precision="0"
          />
        </el-form-item>
        <el-form-item label="备注" prop="remark">
          <el-input
            v-model="adjustForm.remark"
            type="textarea"
            :rows="3"
            placeholder="请输入调整原因或备注"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="adjustDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleAdjustSubmit">
            确定
          </el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 库存记录对话框 -->
    <el-dialog
      v-model="historyDialogVisible"
      title="库存记录"
      width="800px"
    >
      <el-table :data="stockHistory" style="width: 100%">
        <el-table-column prop="date" label="日期" width="180" />
        <el-table-column prop="type" label="类型" width="100">
          <template #default="{ row }">
            <el-tag :type="row.type === 'in' ? 'success' : 'danger'">
              {{ row.type === 'in' ? '入库' : '出库' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="quantity" label="数量" width="100" />
        <el-table-column prop="operator" label="操作人" width="120" />
        <el-table-column prop="remark" label="备注" />
      </el-table>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { FormInstance } from 'element-plus'
import { Search } from '@element-plus/icons-vue'

interface InventoryItem {
  id: number
  product_name: string
  category: string
  current_stock: number
  min_stock: number
  max_stock: number
  unit: string
  last_updated: string
}

interface StockHistory {
  date: string
  type: 'in' | 'out'
  quantity: number
  operator: string
  remark: string
}

// 搜索相关
const searchQuery = ref('')
const categoryFilter = ref('')
const stockStatusFilter = ref('')
const categories = [
  { label: '电子产品', value: 'electronics' },
  { label: '办公用品', value: 'office' },
  { label: '家具', value: 'furniture' }
]

const filteredInventory = computed(() => {
  let result = inventory.value
  if (searchQuery.value) {
    result = result.filter(item =>
      item.product_name.toLowerCase().includes(searchQuery.value.toLowerCase())
    )
  }
  if (categoryFilter.value) {
    result = result.filter(item => item.category === categoryFilter.value)
  }
  if (stockStatusFilter.value) {
    result = result.filter(item => {
      const status = getStockStatus(item)
      return status === stockStatusFilter.value
    })
  }
  return result
})

// 分页相关
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)

// 库存数据
const inventory = ref<InventoryItem[]>([
  {
    id: 1,
    product_name: '笔记本电脑',
    category: 'electronics',
    current_stock: 50,
    min_stock: 10,
    max_stock: 100,
    unit: '台',
    last_updated: '2024-01-01 10:00:00'
  },
  {
    id: 2,
    product_name: '办公椅',
    category: 'furniture',
    current_stock: 20,
    min_stock: 5,
    max_stock: 50,
    unit: '把',
    last_updated: '2024-01-01 11:00:00'
  }
])

// 加载状态
const loading = ref(false)

// 库存调整对话框相关
const adjustDialogVisible = ref(false)
const adjustDialogType = ref<'in' | 'out'>('in')
const adjustFormRef = ref<FormInstance>()
const adjustForm = ref({
  product_name: '',
  current_stock: 0,
  quantity: 1,
  remark: ''
})

// 库存记录对话框相关
const historyDialogVisible = ref(false)
const stockHistory = ref<StockHistory[]>([
  {
    date: '2024-01-01 10:00:00',
    type: 'in',
    quantity: 100,
    operator: 'admin',
    remark: '初始入库'
  },
  {
    date: '2024-01-01 11:00:00',
    type: 'out',
    quantity: 50,
    operator: 'admin',
    remark: '销售出库'
  }
])

// 表单验证规则
const adjustRules = {
  quantity: [
    { required: true, message: '请输入调整数量', trigger: 'blur' },
    { type: 'number', min: 1, message: '数量必须大于0', trigger: 'blur' }
  ]
}

// 获取库存状态
const getStockStatus = (item: InventoryItem) => {
  if (item.current_stock <= item.min_stock) return 'insufficient'
  if (item.current_stock >= item.max_stock) return 'sufficient'
  return 'warning'
}

// 获取库存状态类型
const getStockStatusType = (item: InventoryItem) => {
  const status = getStockStatus(item)
  switch (status) {
    case 'sufficient':
      return 'success'
    case 'insufficient':
      return 'danger'
    case 'warning':
      return 'warning'
    default:
      return 'info'
  }
}

// 获取库存状态文本
const getStockStatusText = (item: InventoryItem) => {
  const status = getStockStatus(item)
  switch (status) {
    case 'sufficient':
      return '库存充足'
    case 'insufficient':
      return '库存不足'
    case 'warning':
      return '库存告警'
    default:
      return '未知'
  }
}

// 搜索处理
const handleSearch = () => {
  currentPage.value = 1
}

// 分页处理
const handleSizeChange = (val: number) => {
  pageSize.value = val
  currentPage.value = 1
}

const handleCurrentChange = (val: number) => {
  currentPage.value = val
}

// 入库
const handleStockIn = () => {
  adjustDialogType.value = 'in'
  adjustForm.value = {
    product_name: '',
    current_stock: 0,
    quantity: 1,
    remark: ''
  }
  adjustDialogVisible.value = true
}

// 出库
const handleStockOut = () => {
  adjustDialogType.value = 'out'
  adjustForm.value = {
    product_name: '',
    current_stock: 0,
    quantity: 1,
    remark: ''
  }
  adjustDialogVisible.value = true
}

// 调整库存
const handleAdjustStock = (row: InventoryItem) => {
  adjustForm.value = {
    product_name: row.product_name,
    current_stock: row.current_stock,
    quantity: 1,
    remark: ''
  }
  adjustDialogVisible.value = true
}

// 查看记录
const handleViewHistory = (row: InventoryItem) => {
  // TODO: 根据产品ID获取库存记录
  historyDialogVisible.value = true
}

// 提交库存调整
const handleAdjustSubmit = async () => {
  if (!adjustFormRef.value) return
  
  try {
    await adjustFormRef.value.validate()
    // TODO: 调用库存调整API
    ElMessage.success(adjustDialogType.value === 'in' ? '入库成功' : '出库成功')
    adjustDialogVisible.value = false
  } catch (error) {
    console.error('表单验证失败:', error)
  }
}
</script>

<style scoped>
.inventory-container {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-actions {
  display: flex;
  gap: 12px;
}

.search-bar {
  margin-bottom: 20px;
  display: flex;
  gap: 16px;
}

.search-input {
  width: 300px;
}

.filter-select {
  width: 200px;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style> 