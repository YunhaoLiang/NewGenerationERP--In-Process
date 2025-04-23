<template>
  <div class="orders-container">
    <div class="header-actions">
      <el-button type="primary" @click="handleAdd">
        <el-icon><Plus /></el-icon>新建订单
      </el-button>
      <el-input
        v-model="searchQuery"
        placeholder="搜索订单号"
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
      :data="orders"
      border
      style="width: 100%"
    >
      <el-table-column prop="order_id" label="订单号" width="120" />
      <el-table-column prop="user_id" label="客户ID" width="100" />
      <el-table-column prop="product_id" label="产品ID" width="100" />
      <el-table-column prop="quantity" label="数量" width="100" />
      <el-table-column prop="total_amount" label="总金额">
        <template #default="{ row }">
          ¥{{ formatPrice(row.total_amount) }}
        </template>
      </el-table-column>
      <el-table-column prop="status" label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="getStatusType(row.status)">
            {{ getStatusLabel(row.status) }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="created_at" label="创建时间" width="180">
        <template #default="{ row }">
          {{ formatDate(row.created_at) }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="200" fixed="right">
        <template #default="{ row }">
          <el-button-group>
            <el-button type="primary" @click="handleView(row)">查看</el-button>
            <el-button
              v-if="row.status === 'pending'"
              type="success"
              @click="handleProcess(row)"
            >
              处理
            </el-button>
            <el-button
              v-if="row.status === 'pending'"
              type="danger"
              @click="handleCancel(row)"
            >
              取消
            </el-button>
          </el-button-group>
        </template>
      </el-table-column>
    </el-table>

    <!-- 订单表单对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑订单' : '新建订单'"
      width="500px"
    >
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="100px"
      >
        <el-form-item label="产品" prop="product_id">
          <el-select v-model="form.product_id" placeholder="请选择产品">
            <el-option
              v-for="product in products"
              :key="product.product_id"
              :label="product.name"
              :value="product.product_id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="数量" prop="quantity">
          <el-input-number
            v-model="form.quantity"
            :min="1"
            :max="selectedProduct?.stock || 999999"
          />
        </el-form-item>
        <el-form-item label="总金额">
          <span>¥{{ calculateTotal }}</span>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit">
            确认
          </el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 订单详情对话框 -->
    <el-dialog
      v-model="detailVisible"
      title="订单详情"
      width="600px"
    >
      <el-descriptions :column="2" border>
        <el-descriptions-item label="订单号">
          {{ currentOrder?.order_id }}
        </el-descriptions-item>
        <el-descriptions-item label="客户ID">
          {{ currentOrder?.user_id }}
        </el-descriptions-item>
        <el-descriptions-item label="产品ID">
          {{ currentOrder?.product_id }}
        </el-descriptions-item>
        <el-descriptions-item label="数量">
          {{ currentOrder?.quantity }}
        </el-descriptions-item>
        <el-descriptions-item label="总金额">
          ¥{{ formatPrice(currentOrder?.total_amount || 0) }}
        </el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="getStatusType(currentOrder?.status || '')">
            {{ getStatusLabel(currentOrder?.status || '') }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="创建时间" :span="2">
          {{ formatDate(currentOrder?.created_at || '') }}
        </el-descriptions-item>
      </el-descriptions>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Search } from '@element-plus/icons-vue'
import type { FormInstance } from 'element-plus'
import type { Order, Product } from '@/types/models'

// 状态
const loading = ref(false)
const orders = ref<Order[]>([])
const products = ref<Product[]>([])
const searchQuery = ref('')
const dialogVisible = ref(false)
const detailVisible = ref(false)
const isEdit = ref(false)
const formRef = ref<FormInstance>()
const currentOrder = ref<Order | null>(null)

// 表单数据
const form = ref({
  product_id: undefined as number | undefined,
  quantity: 1
})

// 表单验证规则
const rules = {
  product_id: [
    { required: true, message: '请选择产品', trigger: 'change' }
  ],
  quantity: [
    { required: true, message: '请输入数量', trigger: 'blur' }
  ]
}

// 获取选中的产品
const selectedProduct = computed(() => {
  return products.value.find(p => p.product_id === form.value.product_id)
})

// 计算总金额
const calculateTotal = computed(() => {
  if (!selectedProduct.value) return '0.00'
  return formatPrice(selectedProduct.value.price * form.value.quantity)
})

// 格式化价格
const formatPrice = (price: number) => {
  return price.toFixed(2)
}

// 格式化日期
const formatDate = (date: string) => {
  return new Date(date).toLocaleString()
}

// 获取状态类型
const getStatusType = (status: string) => {
  const types: Record<string, string> = {
    pending: 'warning',
    processing: 'primary',
    completed: 'success',
    cancelled: 'danger'
  }
  return types[status] || 'info'
}

// 获取状态标签
const getStatusLabel = (status: string) => {
  const labels: Record<string, string> = {
    pending: '待处理',
    processing: '处理中',
    completed: '已完成',
    cancelled: '已取消'
  }
  return labels[status] || status
}

// 获取订单列表
const fetchOrders = async () => {
  try {
    loading.value = true
    // 这里应该调用订单列表API
    // const response = await orderApi.getOrders()
    // orders.value = response.data
    
    // 模拟数据
    orders.value = []
  } catch (error) {
    ElMessage.error('获取订单列表失败')
  } finally {
    loading.value = false
  }
}

// 获取产品列表
const fetchProducts = async () => {
  try {
    // 这里应该调用产品列表API
    // const response = await productApi.getProducts()
    // products.value = response.data
    
    // 模拟数据
    products.value = []
  } catch (error) {
    ElMessage.error('获取产品列表失败')
  }
}

// 搜索处理
const handleSearch = () => {
  // 实现搜索逻辑
  console.log('搜索:', searchQuery.value)
}

// 新建订单
const handleAdd = () => {
  isEdit.value = false
  form.value = {
    product_id: undefined,
    quantity: 1
  }
  dialogVisible.value = true
}

// 查看订单
const handleView = (row: Order) => {
  currentOrder.value = row
  detailVisible.value = true
}

// 处理订单
const handleProcess = async (row: Order) => {
  try {
    await ElMessageBox.confirm(
      '确定要处理该订单吗？',
      '提示',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'info'
      }
    )
    
    // 这里应该调用处理订单API
    // await orderApi.processOrder(row.order_id)
    ElMessage.success('订单处理成功')
    await fetchOrders()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('订单处理失败')
    }
  }
}

// 取消订单
const handleCancel = async (row: Order) => {
  try {
    await ElMessageBox.confirm(
      '确定要取消该订单吗？此操作不可恢复',
      '警告',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    // 这里应该调用取消订单API
    // await orderApi.cancelOrder(row.order_id)
    ElMessage.success('订单取消成功')
    await fetchOrders()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('订单取消失败')
    }
  }
}

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
    
    // 这里应该调用创建订单API
    // const data = {
    //   product_id: form.value.product_id,
    //   quantity: form.value.quantity
    // }
    // await orderApi.createOrder(data)
    
    ElMessage.success('订单创建成功')
    dialogVisible.value = false
    await fetchOrders()
  } catch (error) {
    ElMessage.error('订单创建失败')
  }
}

// 初始化
onMounted(() => {
  fetchOrders()
  fetchProducts()
})
</script>

<style scoped>
.orders-container {
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