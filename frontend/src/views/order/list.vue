<template>
  <div class="order-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <div class="header-left">
            <el-input
              v-model="searchForm.orderNo"
              placeholder="订单号"
              style="width: 200px"
              clearable
            />
            <el-select v-model="searchForm.status" placeholder="订单状态" clearable>
              <el-option label="待付款" value="pending_payment" />
              <el-option label="待发货" value="pending_shipment" />
              <el-option label="已发货" value="shipped" />
              <el-option label="已完成" value="completed" />
              <el-option label="已取消" value="cancelled" />
            </el-select>
            <el-date-picker
              v-model="searchForm.dateRange"
              type="daterange"
              range-separator="至"
              start-placeholder="开始日期"
              end-placeholder="结束日期"
              value-format="YYYY-MM-DD"
            />
          </div>
          <div class="header-right">
            <el-button type="primary" @click="handleAdd">新建订单</el-button>
            <el-button type="success" @click="testRoute">测试路由</el-button>
          </div>
        </div>
      </template>

      <el-table :data="orders" style="width: 100%">
        <el-table-column prop="orderNo" label="订单号" width="180" />
        <el-table-column prop="customerName" label="客户名称" width="150" />
        <el-table-column prop="totalAmount" label="订单金额" width="120">
          <template #default="{ row }">
            ¥ {{ row.totalAmount.toFixed(2) }}
          </template>
        </el-table-column>
        <el-table-column prop="status" label="订单状态" width="120">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="createTime" label="创建时间" width="180" />
        <el-table-column prop="paymentTime" label="付款时间" width="180" />
        <el-table-column prop="shipmentTime" label="发货时间" width="180" />
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link @click="handleView(row)">查看</el-button>
            <el-button 
              v-if="row.status === 'pending_payment'"
              type="success" 
              link 
              @click="handlePayment(row)"
            >
              收款
            </el-button>
            <el-button 
              v-if="row.status === 'pending_shipment'"
              type="warning" 
              link 
              @click="handleShipment(row)"
            >
              发货
            </el-button>
            <el-button 
              v-if="['pending_payment', 'pending_shipment'].includes(row.status)"
              type="danger" 
              link 
              @click="handleCancel(row)"
            >
              取消
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next"
          :total="total"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>

    <!-- 订单详情对话框 -->
    <el-dialog
      v-model="detailVisible"
      title="订单详情"
      width="800px"
    >
      <el-descriptions :column="2" border>
        <el-descriptions-item label="订单号">{{ detail.orderNo }}</el-descriptions-item>
        <el-descriptions-item label="客户名称">{{ detail.customerName }}</el-descriptions-item>
        <el-descriptions-item label="订单状态">
          <el-tag :type="getStatusType(detail.status)">
            {{ getStatusText(detail.status) }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="订单金额">¥ {{ detail.totalAmount.toFixed(2) }}</el-descriptions-item>
        <el-descriptions-item label="创建时间">{{ detail.createTime }}</el-descriptions-item>
        <el-descriptions-item label="付款时间">{{ detail.paymentTime }}</el-descriptions-item>
        <el-descriptions-item label="发货时间">{{ detail.shipmentTime }}</el-descriptions-item>
        <el-descriptions-item label="收货地址">{{ detail.shippingAddress }}</el-descriptions-item>
      </el-descriptions>

      <el-table :data="detail.items" style="width: 100%; margin-top: 20px">
        <el-table-column prop="productName" label="商品名称" />
        <el-table-column prop="quantity" label="数量" width="100" />
        <el-table-column prop="unitPrice" label="单价" width="120">
          <template #default="{ row }">
            ¥ {{ row.unitPrice.toFixed(2) }}
          </template>
        </el-table-column>
        <el-table-column prop="subtotal" label="小计" width="120">
          <template #default="{ row }">
            ¥ {{ (row.quantity * row.unitPrice).toFixed(2) }}
          </template>
        </el-table-column>
      </el-table>
    </el-dialog>

    <!-- 收款对话框 -->
    <el-dialog
      v-model="paymentVisible"
      title="订单收款"
      width="500px"
    >
      <el-form
        ref="paymentFormRef"
        :model="paymentForm"
        :rules="paymentRules"
        label-width="100px"
      >
        <el-form-item label="订单号">
          <span>{{ paymentForm.orderNo }}</span>
        </el-form-item>
        <el-form-item label="订单金额">
          <span>¥ {{ paymentForm.amount.toFixed(2) }}</span>
        </el-form-item>
        <el-form-item label="支付方式" prop="paymentMethod">
          <el-select v-model="paymentForm.paymentMethod" style="width: 100%">
            <el-option label="现金" value="cash" />
            <el-option label="银行转账" value="bank_transfer" />
            <el-option label="支付宝" value="alipay" />
            <el-option label="微信支付" value="wechat_pay" />
          </el-select>
        </el-form-item>
        <el-form-item label="备注" prop="remark">
          <el-input
            v-model="paymentForm.remark"
            type="textarea"
            :rows="2"
            placeholder="请输入备注"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="paymentVisible = false">取消</el-button>
          <el-button type="primary" @click="handlePaymentSubmit">确定</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 发货对话框 -->
    <el-dialog
      v-model="shipmentVisible"
      title="订单发货"
      width="500px"
    >
      <el-form
        ref="shipmentFormRef"
        :model="shipmentForm"
        :rules="shipmentRules"
        label-width="100px"
      >
        <el-form-item label="订单号">
          <span>{{ shipmentForm.orderNo }}</span>
        </el-form-item>
        <el-form-item label="收货地址">
          <span>{{ shipmentForm.shippingAddress }}</span>
        </el-form-item>
        <el-form-item label="物流公司" prop="shippingCompany">
          <el-select v-model="shipmentForm.shippingCompany" style="width: 100%">
            <el-option label="顺丰速运" value="sf" />
            <el-option label="中通快递" value="zt" />
            <el-option label="圆通速递" value="yt" />
            <el-option label="韵达快递" value="yd" />
          </el-select>
        </el-form-item>
        <el-form-item label="物流单号" prop="trackingNumber">
          <el-input v-model="shipmentForm.trackingNumber" />
        </el-form-item>
        <el-form-item label="备注" prop="remark">
          <el-input
            v-model="shipmentForm.remark"
            type="textarea"
            :rows="2"
            placeholder="请输入备注"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="shipmentVisible = false">取消</el-button>
          <el-button type="primary" @click="handleShipmentSubmit">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import type { FormInstance } from 'element-plus'
import { useRouter } from 'vue-router'

const router = useRouter()

// 分页相关
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(100)

// 搜索表单
const searchForm = reactive({
  orderNo: '',
  status: '',
  dateRange: []
})

// 订单列表数据
const orders = ref([
  {
    orderNo: 'ORD20240315001',
    customerName: '张三',
    totalAmount: 12800.00,
    status: 'pending_payment',
    createTime: '2024-03-15 10:30:00',
    paymentTime: '',
    shipmentTime: ''
  },
  {
    orderNo: 'ORD20240315002',
    customerName: '李四',
    totalAmount: 8500.00,
    status: 'pending_shipment',
    createTime: '2024-03-15 11:20:00',
    paymentTime: '2024-03-15 11:25:00',
    shipmentTime: ''
  },
  {
    orderNo: 'ORD20240315003',
    customerName: '王五',
    totalAmount: 15200.00,
    status: 'shipped',
    createTime: '2024-03-15 14:15:00',
    paymentTime: '2024-03-15 14:20:00',
    shipmentTime: '2024-03-15 15:30:00'
  }
])

// 订单状态相关
const getStatusType = (status: string) => {
  const statusMap: Record<string, string> = {
    pending_payment: 'danger',
    pending_shipment: 'warning',
    shipped: 'primary',
    completed: 'success',
    cancelled: 'info'
  }
  return statusMap[status] || ''
}

const getStatusText = (status: string) => {
  const statusMap: Record<string, string> = {
    pending_payment: '待付款',
    pending_shipment: '待发货',
    shipped: '已发货',
    completed: '已完成',
    cancelled: '已取消'
  }
  return statusMap[status] || ''
}

// 订单详情
const detailVisible = ref(false)
const detail = reactive({
  orderNo: '',
  customerName: '',
  status: '',
  totalAmount: 0,
  createTime: '',
  paymentTime: '',
  shipmentTime: '',
  shippingAddress: '',
  items: []
})

// 收款表单
const paymentVisible = ref(false)
const paymentFormRef = ref<FormInstance>()
const paymentForm = reactive({
  orderNo: '',
  amount: 0,
  paymentMethod: '',
  remark: ''
})

const paymentRules = {
  paymentMethod: [
    { required: true, message: '请选择支付方式', trigger: 'change' }
  ]
}

// 发货表单
const shipmentVisible = ref(false)
const shipmentFormRef = ref<FormInstance>()
const shipmentForm = reactive({
  orderNo: '',
  shippingAddress: '',
  shippingCompany: '',
  trackingNumber: '',
  remark: ''
})

const shipmentRules = {
  shippingCompany: [
    { required: true, message: '请选择物流公司', trigger: 'change' }
  ],
  trackingNumber: [
    { required: true, message: '请输入物流单号', trigger: 'blur' }
  ]
}

// 搜索和分页方法
const handleSearch = () => {
  // TODO: 实现搜索逻辑
}

const handleSizeChange = (val: number) => {
  pageSize.value = val
  // TODO: 重新加载数据
}

const handleCurrentChange = (val: number) => {
  currentPage.value = val
  // TODO: 重新加载数据
}

// 订单操作方法
const handleAdd = () => {
  // TODO: 实现新建订单逻辑
}

const handleView = (row: any) => {
  router.push(`/order/detail/${row.orderNo}`)
}

const handlePayment = (row: any) => {
  paymentForm.orderNo = row.orderNo
  paymentForm.amount = row.totalAmount
  paymentForm.paymentMethod = ''
  paymentForm.remark = ''
  paymentVisible.value = true
}

const handlePaymentSubmit = async () => {
  if (!paymentFormRef.value) return
  
  await paymentFormRef.value.validate((valid) => {
    if (valid) {
      // TODO: 实现收款逻辑
      ElMessage.success('收款成功')
      paymentVisible.value = false
    }
  })
}

const handleShipment = (row: any) => {
  shipmentForm.orderNo = row.orderNo
  shipmentForm.shippingAddress = row.shippingAddress
  shipmentForm.shippingCompany = ''
  shipmentForm.trackingNumber = ''
  shipmentForm.remark = ''
  shipmentVisible.value = true
}

const handleShipmentSubmit = async () => {
  if (!shipmentFormRef.value) return
  
  await shipmentFormRef.value.validate((valid) => {
    if (valid) {
      // TODO: 实现发货逻辑
      ElMessage.success('发货成功')
      shipmentVisible.value = false
    }
  })
}

const handleCancel = (row: any) => {
  // TODO: 实现取消订单逻辑
  ElMessage.success('订单已取消')
}

// 测试路由跳转
const testRoute = () => {
  router.push('/order/detail/ORD20240315001')
}
</script>

<style scoped>
.order-container {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-left {
  display: flex;
  gap: 10px;
}

.header-right {
  display: flex;
  gap: 10px;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style> 