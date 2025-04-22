<template>
  <div class="transactions-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>交易记录</span>
          <el-button type="primary" @click="handleAdd">新增交易</el-button>
        </div>
      </template>
      
      <el-table :data="transactions" style="width: 100%">
        <el-table-column prop="transactionNo" label="交易编号" width="180" />
        <el-table-column prop="transactionType" label="交易类型">
          <template #default="{ row }">
            <el-tag :type="getTransactionTypeTag(row.transactionType)">
              {{ row.transactionType }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="amount" label="金额" />
        <el-table-column prop="account" label="账户" />
        <el-table-column prop="description" label="描述" />
        <el-table-column prop="createTime" label="交易时间" width="180" />
        <el-table-column label="操作" width="150">
          <template #default="{ row }">
            <el-button type="primary" link @click="handleView(row)">查看</el-button>
            <el-button type="danger" link @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 新增交易对话框 -->
    <el-dialog
      v-model="dialogVisible"
      title="新增交易"
      width="500px"
    >
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="100px"
      >
        <el-form-item label="交易类型" prop="transactionType">
          <el-select v-model="form.transactionType" style="width: 100%">
            <el-option label="收入" value="income" />
            <el-option label="支出" value="expense" />
            <el-option label="转账" value="transfer" />
          </el-select>
        </el-form-item>
        <el-form-item label="金额" prop="amount">
          <el-input-number v-model="form.amount" :precision="2" style="width: 100%" />
        </el-form-item>
        <el-form-item label="账户" prop="account">
          <el-select v-model="form.account" style="width: 100%">
            <el-option
              v-for="account in accounts"
              :key="account.id"
              :label="account.name"
              :value="account.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input
            v-model="form.description"
            type="textarea"
            :rows="3"
            placeholder="请输入交易描述"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit">确定</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 查看交易详情对话框 -->
    <el-dialog
      v-model="detailVisible"
      title="交易详情"
      width="500px"
    >
      <el-descriptions :column="1" border>
        <el-descriptions-item label="交易编号">{{ detail.transactionNo }}</el-descriptions-item>
        <el-descriptions-item label="交易类型">
          <el-tag :type="getTransactionTypeTag(detail.transactionType)">
            {{ detail.transactionType }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="金额">{{ detail.amount }}</el-descriptions-item>
        <el-descriptions-item label="账户">{{ detail.account }}</el-descriptions-item>
        <el-descriptions-item label="描述">{{ detail.description }}</el-descriptions-item>
        <el-descriptions-item label="交易时间">{{ detail.createTime }}</el-descriptions-item>
      </el-descriptions>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import type { FormInstance } from 'element-plus'

const transactions = ref([
  {
    transactionNo: 'TRX20240315001',
    transactionType: 'income',
    amount: 12800,
    account: '主营业务收入',
    description: '销售商品收入',
    createTime: '2024-03-15 10:30:00'
  },
  {
    transactionNo: 'TRX20240315002',
    transactionType: 'expense',
    amount: 5600,
    account: '库存商品',
    description: '采购商品支出',
    createTime: '2024-03-15 11:20:00'
  }
])

const accounts = ref([
  { id: 1, name: '主营业务收入' },
  { id: 2, name: '库存商品' }
])

const dialogVisible = ref(false)
const detailVisible = ref(false)
const formRef = ref<FormInstance>()

const form = reactive({
  transactionType: '',
  amount: 0,
  account: '',
  description: ''
})

const detail = reactive({
  transactionNo: '',
  transactionType: '',
  amount: 0,
  account: '',
  description: '',
  createTime: ''
})

const rules = {
  transactionType: [
    { required: true, message: '请选择交易类型', trigger: 'change' }
  ],
  amount: [
    { required: true, message: '请输入交易金额', trigger: 'blur' }
  ],
  account: [
    { required: true, message: '请选择账户', trigger: 'change' }
  ]
}

const getTransactionTypeTag = (type: string) => {
  const typeMap: Record<string, string> = {
    income: 'success',
    expense: 'danger',
    transfer: 'warning'
  }
  return typeMap[type] || ''
}

const handleAdd = () => {
  form.transactionType = ''
  form.amount = 0
  form.account = ''
  form.description = ''
  dialogVisible.value = true
}

const handleView = (row: any) => {
  Object.assign(detail, row)
  detailVisible.value = true
}

const handleDelete = (row: any) => {
  // TODO: 实现删除逻辑
}

const handleSubmit = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate((valid) => {
    if (valid) {
      // TODO: 实现提交逻辑
      dialogVisible.value = false
    }
  })
}
</script>

<style scoped>
.transactions-container {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style> 