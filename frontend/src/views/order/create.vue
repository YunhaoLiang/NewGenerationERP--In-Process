<template>
  <div class="create-order-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>新建订单</span>
          <el-button type="primary" @click="handleSubmit">提交订单</el-button>
        </div>
      </template>

      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="100px"
      >
        <!-- 基本信息 -->
        <el-divider content-position="left">基本信息</el-divider>
        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="客户名称" prop="customerName">
              <el-select
                v-model="form.customerName"
                filterable
                remote
                :remote-method="handleCustomerSearch"
                :loading="customerLoading"
                style="width: 100%"
              >
                <el-option
                  v-for="item in customers"
                  :key="item.id"
                  :label="item.name"
                  :value="item.name"
                />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="订单类型" prop="orderType">
              <el-select v-model="form.orderType" style="width: 100%">
                <el-option label="普通订单" value="normal" />
                <el-option label="批发订单" value="wholesale" />
                <el-option label="定制订单" value="custom" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="支付方式" prop="paymentMethod">
              <el-select v-model="form.paymentMethod" style="width: 100%">
                <el-option label="现金" value="cash" />
                <el-option label="银行转账" value="bank_transfer" />
                <el-option label="支付宝" value="alipay" />
                <el-option label="微信支付" value="wechat_pay" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <!-- 商品信息 -->
        <el-divider content-position="left">商品信息</el-divider>
        <el-table :data="form.items" style="width: 100%">
          <el-table-column label="商品名称" min-width="200">
            <template #default="{ row, $index }">
              <el-select
                v-model="row.productId"
                filterable
                remote
                :remote-method="(query) => handleProductSearch(query, $index)"
                :loading="productLoading"
                style="width: 100%"
                @change="handleProductChange($index)"
              >
                <el-option
                  v-for="item in products"
                  :key="item.id"
                  :label="item.name"
                  :value="item.id"
                />
              </el-select>
            </template>
          </el-table-column>
          <el-table-column label="单价" width="120">
            <template #default="{ row }">
              <span>¥ {{ row.unitPrice.toFixed(2) }}</span>
            </template>
          </el-table-column>
          <el-table-column label="数量" width="120">
            <template #default="{ row, $index }">
              <el-input-number
                v-model="row.quantity"
                :min="1"
                @change="handleQuantityChange($index)"
              />
            </template>
          </el-table-column>
          <el-table-column label="小计" width="120">
            <template #default="{ row }">
              <span>¥ {{ (row.unitPrice * row.quantity).toFixed(2) }}</span>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="100">
            <template #default="{ $index }">
              <el-button type="danger" link @click="handleRemoveItem($index)">
                删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
        <div style="margin-top: 10px">
          <el-button type="primary" link @click="handleAddItem">
            <el-icon><Plus /></el-icon>添加商品
          </el-button>
        </div>

        <!-- 收货信息 -->
        <el-divider content-position="left">收货信息</el-divider>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="收货人" prop="shippingName">
              <el-input v-model="form.shippingName" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="联系电话" prop="shippingPhone">
              <el-input v-model="form.shippingPhone" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="收货地址" prop="shippingAddress">
          <el-input
            v-model="form.shippingAddress"
            type="textarea"
            :rows="2"
          />
        </el-form-item>

        <!-- 订单备注 -->
        <el-divider content-position="left">订单备注</el-divider>
        <el-form-item label="备注" prop="remark">
          <el-input
            v-model="form.remark"
            type="textarea"
            :rows="3"
            placeholder="请输入订单备注"
          />
        </el-form-item>

        <!-- 订单金额 -->
        <el-divider content-position="left">订单金额</el-divider>
        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="商品总额">
              <span>¥ {{ totalAmount.toFixed(2) }}</span>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="运费">
              <el-input-number
                v-model="form.shippingFee"
                :min="0"
                :precision="2"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="优惠金额">
              <el-input-number
                v-model="form.discount"
                :min="0"
                :precision="2"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="实付金额">
          <span class="final-amount">¥ {{ finalAmount.toFixed(2) }}</span>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
import { Plus } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import type { FormInstance } from 'element-plus'

const formRef = ref<FormInstance>()

const form = reactive({
  customerName: '',
  orderType: 'normal',
  paymentMethod: '',
  items: [
    {
      productId: '',
      productName: '',
      unitPrice: 0,
      quantity: 1,
      subtotal: 0
    }
  ],
  shippingName: '',
  shippingPhone: '',
  shippingAddress: '',
  shippingFee: 0,
  discount: 0,
  remark: ''
})

const rules = {
  customerName: [
    { required: true, message: '请选择客户', trigger: 'change' }
  ],
  orderType: [
    { required: true, message: '请选择订单类型', trigger: 'change' }
  ],
  paymentMethod: [
    { required: true, message: '请选择支付方式', trigger: 'change' }
  ],
  shippingName: [
    { required: true, message: '请输入收货人', trigger: 'blur' }
  ],
  shippingPhone: [
    { required: true, message: '请输入联系电话', trigger: 'blur' }
  ],
  shippingAddress: [
    { required: true, message: '请输入收货地址', trigger: 'blur' }
  ]
}

// 客户搜索
const customerLoading = ref(false)
const customers = ref([
  { id: 1, name: '张三' },
  { id: 2, name: '李四' },
  { id: 3, name: '王五' }
])

const handleCustomerSearch = (query: string) => {
  if (query) {
    customerLoading.value = true
    // TODO: 实现客户搜索逻辑
    setTimeout(() => {
      customerLoading.value = false
    }, 500)
  }
}

// 商品搜索
const productLoading = ref(false)
const products = ref([
  { id: 1, name: 'ThinkPad X1 Carbon', price: 9999.00 },
  { id: 2, name: 'MacBook Pro', price: 12999.00 },
  { id: 3, name: 'Dell XPS 13', price: 8999.00 }
])

const handleProductSearch = (query: string, index: number) => {
  if (query) {
    productLoading.value = true
    // TODO: 实现商品搜索逻辑
    setTimeout(() => {
      productLoading.value = false
    }, 500)
  }
}

const handleProductChange = (index: number) => {
  const product = products.value.find(p => p.id.toString() === form.items[index].productId)
  if (product) {
    form.items[index].productName = product.name
    form.items[index].unitPrice = product.price
    form.items[index].subtotal = product.price * form.items[index].quantity
  }
}

const handleQuantityChange = (index: number) => {
  // 数量变化时自动计算小计
  const item = form.items[index]
  item.subtotal = item.unitPrice * item.quantity
}

const handleAddItem = () => {
  form.items.push({
    productId: '',
    productName: '',
    unitPrice: 0,
    quantity: 1,
    subtotal: 0
  })
}

const handleRemoveItem = (index: number) => {
  form.items.splice(index, 1)
}

// 计算订单金额
const totalAmount = computed(() => {
  return form.items.reduce((sum, item) => {
    return sum + item.unitPrice * item.quantity
  }, 0)
})

const finalAmount = computed(() => {
  return totalAmount.value + form.shippingFee - form.discount
})

const handleSubmit = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate((valid) => {
    if (valid) {
      // TODO: 实现订单提交逻辑
      ElMessage.success('订单创建成功')
    }
  })
}
</script>

<style scoped>
.create-order-container {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.final-amount {
  font-size: 20px;
  font-weight: bold;
  color: #f56c6c;
}
</style> 