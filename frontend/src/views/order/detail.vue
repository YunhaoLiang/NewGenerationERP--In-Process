<template>
  <div class="order-detail-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>订单详情</span>
          <div class="header-buttons">
            <el-button
              v-if="order.status === 'pending_payment'"
              type="success"
              @click="handlePayment"
            >
              收款
            </el-button>
            <el-button
              v-if="order.status === 'pending_shipment'"
              type="warning"
              @click="handleShipment"
            >
              发货
            </el-button>
            <el-button
              v-if="['pending_payment', 'pending_shipment'].includes(order.status)"
              type="danger"
              @click="handleCancel"
            >
              取消订单
            </el-button>
            <el-button @click="handleBack">返回</el-button>
          </div>
        </div>
      </template>

      <!-- 基本信息 -->
      <el-descriptions title="基本信息" :column="3" border>
        <el-descriptions-item label="订单号">{{ order.orderNo }}</el-descriptions-item>
        <el-descriptions-item label="订单状态">
          <el-tag :type="getStatusType(order.status)">
            {{ getStatusText(order.status) }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="订单类型">{{ getOrderTypeText(order.orderType) }}</el-descriptions-item>
        <el-descriptions-item label="客户名称">{{ order.customerName }}</el-descriptions-item>
        <el-descriptions-item label="创建时间">{{ order.createTime }}</el-descriptions-item>
        <el-descriptions-item label="支付方式">{{ getPaymentMethodText(order.paymentMethod) }}</el-descriptions-item>
      </el-descriptions>

      <!-- 商品信息 -->
      <el-descriptions title="商品信息" :column="1" border style="margin-top: 20px">
        <el-descriptions-item>
          <el-table :data="order.items" style="width: 100%">
            <el-table-column prop="productName" label="商品名称" />
            <el-table-column prop="quantity" label="数量" width="100" />
            <el-table-column prop="unitPrice" label="单价" width="120">
              <template #default="{ row }">
                ¥ {{ row.unitPrice.toFixed(2) }}
              </template>
            </el-table-column>
            <el-table-column prop="subtotal" label="小计" width="120">
              <template #default="{ row }">
                ¥ {{ (row.unitPrice * row.quantity).toFixed(2) }}
              </template>
            </el-table-column>
          </el-table>
        </el-descriptions-item>
      </el-descriptions>

      <!-- 收货信息 -->
      <el-descriptions title="收货信息" :column="2" border style="margin-top: 20px">
        <el-descriptions-item label="收货人">{{ order.shippingName }}</el-descriptions-item>
        <el-descriptions-item label="联系电话">{{ order.shippingPhone }}</el-descriptions-item>
        <el-descriptions-item label="收货地址" :span="2">{{ order.shippingAddress }}</el-descriptions-item>
      </el-descriptions>

      <!-- 订单金额 -->
      <el-descriptions title="订单金额" :column="3" border style="margin-top: 20px">
        <el-descriptions-item label="商品总额">¥ {{ order.totalAmount.toFixed(2) }}</el-descriptions-item>
        <el-descriptions-item label="运费">¥ {{ order.shippingFee.toFixed(2) }}</el-descriptions-item>
        <el-descriptions-item label="优惠金额">¥ {{ order.discount.toFixed(2) }}</el-descriptions-item>
        <el-descriptions-item label="实付金额" :span="3">
          <span class="final-amount">¥ {{ (order.totalAmount + order.shippingFee - order.discount).toFixed(2) }}</span>
        </el-descriptions-item>
      </el-descriptions>

      <!-- 订单备注 -->
      <el-descriptions title="订单备注" :column="1" border style="margin-top: 20px">
        <el-descriptions-item>{{ order.remark || '无' }}</el-descriptions-item>
      </el-descriptions>

      <!-- 订单日志 -->
      <el-descriptions title="订单日志" :column="1" border style="margin-top: 20px">
        <el-descriptions-item>
          <el-timeline>
            <el-timeline-item
              v-for="log in order.logs"
              :key="log.id"
              :timestamp="log.createTime"
              :type="getLogType(log.type)"
            >
              {{ log.content }}
            </el-timeline-item>
          </el-timeline>
        </el-descriptions-item>
      </el-descriptions>
    </el-card>

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
import { ref, reactive, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import type { FormInstance } from 'element-plus'

// 定义接口
interface OrderItem {
  productName: string
  quantity: number
  unitPrice: number
}

interface OrderLog {
  id: number
  type: string
  content: string
  createTime: string
}

interface Order {
  orderNo: string
  status: string
  orderType: string
  customerName: string
  createTime: string
  paymentMethod: string
  items: OrderItem[]
  shippingName: string
  shippingPhone: string
  shippingAddress: string
  totalAmount: number
  shippingFee: number
  discount: number
  remark: string
  logs: OrderLog[]
}

const route = useRoute()
const router = useRouter()

// 订单数据
const order = reactive<Order>({
  orderNo: '',
  status: '',
  orderType: '',
  customerName: '',
  createTime: '',
  paymentMethod: '',
  items: [],
  shippingName: '',
  shippingPhone: '',
  shippingAddress: '',
  totalAmount: 0,
  shippingFee: 0,
  discount: 0,
  remark: '',
  logs: []
})

// 加载订单数据
const loadOrderData = async () => {
  const orderNo = route.params.orderNo as string
  try {
    // TODO: 调用后端API获取订单数据
    // 这里使用模拟数据
    Object.assign(order, {
      orderNo,
      status: 'pending_payment',
      orderType: 'normal',
      customerName: '张三',
      createTime: '2024-03-15 10:30:00',
      paymentMethod: 'alipay',
      items: [
        {
          productName: 'ThinkPad X1 Carbon',
          quantity: 1,
          unitPrice: 9999.00
        },
        {
          productName: 'MacBook Pro',
          quantity: 1,
          unitPrice: 12999.00
        }
      ],
      shippingName: '张三',
      shippingPhone: '13800138000',
      shippingAddress: '北京市海淀区中关村大街1号',
      totalAmount: 22998.00,
      shippingFee: 0.00,
      discount: 0.00,
      remark: '请尽快发货',
      logs: [
        {
          id: 1,
          type: 'create',
          content: '订单创建',
          createTime: '2024-03-15 10:30:00'
        }
      ]
    })
  } catch (error) {
    ElMessage.error('加载订单数据失败')
    router.back()
  }
}

onMounted(() => {
  loadOrderData()
})

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

const getOrderTypeText = (type: string) => {
  const typeMap: Record<string, string> = {
    normal: '普通订单',
    wholesale: '批发订单',
    custom: '定制订单'
  }
  return typeMap[type] || ''
}

const getPaymentMethodText = (method: string) => {
  const methodMap: Record<string, string> = {
    cash: '现金',
    bank_transfer: '银行转账',
    alipay: '支付宝',
    wechat_pay: '微信支付'
  }
  return methodMap[method] || ''
}

const getLogType = (type: string) => {
  const typeMap: Record<string, string> = {
    create: 'primary',
    payment: 'success',
    shipment: 'warning',
    complete: 'success',
    cancel: 'danger'
  }
  return typeMap[type] || ''
}

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

// 操作方法
const handleBack = () => {
  router.back()
}

const handlePayment = () => {
  paymentForm.orderNo = order.orderNo
  paymentForm.amount = order.totalAmount + order.shippingFee - order.discount
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

const handleShipment = () => {
  shipmentForm.orderNo = order.orderNo
  shipmentForm.shippingAddress = order.shippingAddress
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

const handleCancel = () => {
  // TODO: 实现取消订单逻辑
  ElMessage.success('订单已取消')
}
</script>

<style scoped>
.order-detail-container {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-buttons {
  display: flex;
  gap: 10px;
}

.final-amount {
  font-size: 20px;
  font-weight: bold;
  color: #f56c6c;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style> 