<template>
  <div class="order-list-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>订单管理</span>
          <el-button type="primary" @click="handleAdd">新增订单</el-button>
        </div>
      </template>

      <!-- 搜索栏 -->
      <div class="search-bar">
        <el-input
          v-model="searchQuery"
          placeholder="搜索订单号/客户名称"
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
          v-model="statusFilter"
          placeholder="订单状态"
          clearable
          class="filter-select"
          @change="handleSearch"
        >
          <el-option label="待付款" value="pending" />
          <el-option label="已付款" value="paid" />
          <el-option label="已发货" value="shipped" />
          <el-option label="已完成" value="completed" />
          <el-option label="已取消" value="cancelled" />
        </el-select>
        <el-date-picker
          v-model="dateRange"
          type="daterange"
          range-separator="至"
          start-placeholder="开始日期"
          end-placeholder="结束日期"
          class="date-picker"
          @change="handleSearch"
        />
      </div>

      <!-- 订单表格 -->
      <el-table
        :data="filteredOrders"
        style="width: 100%"
        v-loading="loading"
      >
        <el-table-column prop="order_no" label="订单号" width="180" />
        <el-table-column prop="customer_name" label="客户名称" />
        <el-table-column prop="total_amount" label="订单金额">
          <template #default="{ row }">
            ¥{{ row.total_amount.toFixed(2) }}
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="180" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusTagType(row.status)">
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="250">
          <template #default="{ row }">
            <el-button
              type="primary"
              link
              @click="handleView(row)"
            >
              查看
            </el-button>
            <el-button
              type="primary"
              link
              @click="handleEdit(row)"
              v-if="canEdit(row)"
            >
              编辑
            </el-button>
            <el-button
              type="success"
              link
              @click="handlePay(row)"
              v-if="row.status === 'pending'"
            >
              付款
            </el-button>
            <el-button
              type="warning"
              link
              @click="handleShip(row)"
              v-if="row.status === 'paid'"
            >
              发货
            </el-button>
            <el-button
              type="danger"
              link
              @click="handleCancel(row)"
              v-if="canCancel(row)"
            >
              取消
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

    <!-- 订单表单对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogType === 'add' ? '新增订单' : '编辑订单'"
      width="600px"
    >
      <el-form
        ref="orderFormRef"
        :model="orderForm"
        :rules="orderRules"
        label-width="100px"
      >
        <el-form-item label="客户名称" prop="customer_name">
          <el-input v-model="orderForm.customer_name" />
        </el-form-item>
        <el-form-item label="联系电话" prop="phone">
          <el-input v-model="orderForm.phone" />
        </el-form-item>
        <el-form-item label="收货地址" prop="address">
          <el-input
            v-model="orderForm.address"
            type="textarea"
            :rows="3"
          />
        </el-form-item>
        <el-form-item label="订单商品">
          <div class="order-items">
            <div
              v-for="(item, index) in orderForm.items"
              :key="index"
              class="order-item"
            >
              <el-select
                v-model="item.product_id"
                placeholder="选择商品"
                class="item-product"
                @change="handleProductChange($event, index)"
              >
                <el-option
                  v-for="product in products"
                  :key="product.id"
                  :label="product.name"
                  :value="product.id"
                />
              </el-select>
              <el-input-number
                v-model="item.quantity"
                :min="1"
                :max="99"
                class="item-quantity"
                @change="calculateTotal"
              />
              <span class="item-price">
                ¥{{ (item.price * item.quantity).toFixed(2) }}
              </span>
              <el-button
                type="danger"
                circle
                @click="removeOrderItem(index)"
              >
                <el-icon><Delete /></el-icon>
              </el-button>
            </div>
            <el-button
              type="primary"
              plain
              @click="addOrderItem"
            >
              添加商品
            </el-button>
          </div>
        </el-form-item>
        <el-form-item label="订单金额">
          <span class="order-total">¥{{ orderForm.total_amount.toFixed(2) }}</span>
        </el-form-item>
        <el-form-item label="备注" prop="remark">
          <el-input
            v-model="orderForm.remark"
            type="textarea"
            :rows="3"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit">
            确定
          </el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 订单详情对话框 -->
    <el-dialog
      v-model="detailDialogVisible"
      title="订单详情"
      width="800px"
    >
      <el-descriptions :column="2" border>
        <el-descriptions-item label="订单号">
          {{ currentOrder.order_no }}
        </el-descriptions-item>
        <el-descriptions-item label="订单状态">
          <el-tag :type="getStatusTagType(currentOrder.status)">
            {{ getStatusText(currentOrder.status) }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="客户名称">
          {{ currentOrder.customer_name }}
        </el-descriptions-item>
        <el-descriptions-item label="联系电话">
          {{ currentOrder.phone }}
        </el-descriptions-item>
        <el-descriptions-item label="收货地址" :span="2">
          {{ currentOrder.address }}
        </el-descriptions-item>
        <el-descriptions-item label="创建时间">
          {{ currentOrder.created_at }}
        </el-descriptions-item>
        <el-descriptions-item label="订单金额">
          ¥{{ currentOrder.total_amount?.toFixed(2) }}
        </el-descriptions-item>
        <el-descriptions-item label="备注" :span="2">
          {{ currentOrder.remark || '无' }}
        </el-descriptions-item>
      </el-descriptions>

      <el-table
        :data="currentOrder.items || []"
        style="width: 100%; margin-top: 20px"
      >
        <el-table-column prop="product_name" label="商品名称" />
        <el-table-column prop="price" label="单价">
          <template #default="{ row }">
            ¥{{ row.price.toFixed(2) }}
          </template>
        </el-table-column>
        <el-table-column prop="quantity" label="数量" width="100" />
        <el-table-column label="小计" width="150">
          <template #default="{ row }">
            ¥{{ (row.price * row.quantity).toFixed(2) }}
          </template>
        </el-table-column>
      </el-table>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { FormInstance } from 'element-plus'
import { Search, Delete } from '@element-plus/icons-vue'

interface OrderItem {
  product_id: number
  product_name: string
  price: number
  quantity: number
}

interface Order {
  id: number
  order_no: string
  customer_name: string
  phone: string
  address: string
  total_amount: number
  status: 'pending' | 'paid' | 'shipped' | 'completed' | 'cancelled'
  created_at: string
  remark?: string
  items: OrderItem[]
}

// 搜索相关
const searchQuery = ref('')
const statusFilter = ref('')
const dateRange = ref<[Date, Date] | null>(null)

// 分页相关
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)

// 加载状态
const loading = ref(false)

// 模拟数据
const orders = ref<Order[]>([
  {
    id: 1,
    order_no: 'ORD202401010001',
    customer_name: '张三',
    phone: '13800138000',
    address: '北京市朝阳区xxx街道xxx号',
    total_amount: 5999,
    status: 'pending',
    created_at: '2024-01-01 10:00:00',
    items: [
      {
        product_id: 1,
        product_name: '笔记本电脑',
        price: 5999,
        quantity: 1
      }
    ]
  }
])

const products = ref([
  {
    id: 1,
    name: '笔记本电脑',
    price: 5999
  },
  {
    id: 2,
    name: '办公椅',
    price: 299
  }
])

// 过滤订单
const filteredOrders = computed(() => {
  let result = orders.value

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(order =>
      order.order_no.toLowerCase().includes(query) ||
      order.customer_name.toLowerCase().includes(query)
    )
  }

  if (statusFilter.value) {
    result = result.filter(order => order.status === statusFilter.value)
  }

  if (dateRange.value) {
    const [start, end] = dateRange.value
    result = result.filter(order => {
      const orderDate = new Date(order.created_at)
      return orderDate >= start && orderDate <= end
    })
  }

  return result
})

// 对话框相关
const dialogVisible = ref(false)
const dialogType = ref<'add' | 'edit'>('add')
const orderFormRef = ref<FormInstance>()
const orderForm = ref({
  customer_name: '',
  phone: '',
  address: '',
  items: [] as OrderItem[],
  total_amount: 0,
  remark: ''
})

// 订单详情对话框
const detailDialogVisible = ref(false)
const currentOrder = ref<Order>({} as Order)

// 表单验证规则
const orderRules = {
  customer_name: [
    { required: true, message: '请输入客户名称', trigger: 'blur' }
  ],
  phone: [
    { required: true, message: '请输入联系电话', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
  ],
  address: [
    { required: true, message: '请输入收货地址', trigger: 'blur' }
  ]
}

// 获取状态标签类型
const getStatusTagType = (status: string) => {
  const typeMap: Record<string, string> = {
    pending: 'warning',
    paid: 'success',
    shipped: 'info',
    completed: 'success',
    cancelled: 'danger'
  }
  return typeMap[status] || 'info'
}

// 获取状态文本
const getStatusText = (status: string) => {
  const textMap: Record<string, string> = {
    pending: '待付款',
    paid: '已付款',
    shipped: '已发货',
    completed: '已完成',
    cancelled: '已取消'
  }
  return textMap[status] || '未知'
}

// 判断是否可以编辑
const canEdit = (order: Order) => {
  return ['pending'].includes(order.status)
}

// 判断是否可以取消
const canCancel = (order: Order) => {
  return ['pending', 'paid'].includes(order.status)
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

// 新增订单
const handleAdd = () => {
  dialogType.value = 'add'
  orderForm.value = {
    customer_name: '',
    phone: '',
    address: '',
    items: [],
    total_amount: 0,
    remark: ''
  }
  dialogVisible.value = true
}

// 编辑订单
const handleEdit = (row: Order) => {
  dialogType.value = 'edit'
  orderForm.value = {
    ...row,
    items: [...row.items]
  }
  dialogVisible.value = true
}

// 查看订单
const handleView = (row: Order) => {
  currentOrder.value = row
  detailDialogVisible.value = true
}

// 付款
const handlePay = (row: Order) => {
  ElMessageBox.confirm('确认已收到付款？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    // TODO: 调用付款API
    ElMessage.success('付款确认成功')
  })
}

// 发货
const handleShip = (row: Order) => {
  ElMessageBox.confirm('确认发货？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    // TODO: 调用发货API
    ElMessage.success('发货成功')
  })
}

// 取消订单
const handleCancel = (row: Order) => {
  ElMessageBox.confirm('确认取消订单？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    // TODO: 调用取消订单API
    ElMessage.success('订单已取消')
  })
}

// 添加订单商品
const addOrderItem = () => {
  orderForm.value.items.push({
    product_id: 0,
    product_name: '',
    price: 0,
    quantity: 1
  })
}

// 移除订单商品
const removeOrderItem = (index: number) => {
  orderForm.value.items.splice(index, 1)
  calculateTotal()
}

// 商品选择变更
const handleProductChange = (productId: number, index: number) => {
  const product = products.value.find(p => p.id === productId)
  if (product) {
    orderForm.value.items[index] = {
      ...orderForm.value.items[index],
      product_id: product.id,
      product_name: product.name,
      price: product.price
    }
    calculateTotal()
  }
}

// 计算总金额
const calculateTotal = () => {
  orderForm.value.total_amount = orderForm.value.items.reduce(
    (total, item) => total + item.price * item.quantity,
    0
  )
}

// 提交表单
const handleSubmit = async () => {
  if (!orderFormRef.value) return
  
  try {
    await orderFormRef.value.validate()
    // TODO: 调用新增/编辑API
    ElMessage.success(dialogType.value === 'add' ? '新增成功' : '编辑成功')
    dialogVisible.value = false
  } catch (error) {
    console.error('表单验证失败:', error)
  }
}
</script>

<style scoped>
.order-list-container {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
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
  width: 150px;
}

.date-picker {
  width: 350px;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.order-items {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.order-item {
  display: flex;
  align-items: center;
  gap: 12px;
}

.item-product {
  width: 200px;
}

.item-quantity {
  width: 120px;
}

.item-price {
  width: 100px;
  text-align: right;
}

.order-total {
  font-size: 18px;
  color: #f56c6c;
  font-weight: bold;
}
</style> 