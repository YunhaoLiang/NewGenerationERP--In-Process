<template>
  <div class="accounts-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>账户列表</span>
          <el-button type="primary" @click="handleAdd">新增账户</el-button>
        </div>
      </template>
      
      <el-table :data="accounts" style="width: 100%">
        <el-table-column prop="accountName" label="账户名称" />
        <el-table-column prop="accountType" label="账户类型">
          <template #default="{ row }">
            <el-tag :type="getAccountTypeTag(row.accountType)">
              {{ row.accountType }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="balance" label="余额" />
        <el-table-column prop="currency" label="币种" width="80" />
        <el-table-column prop="createTime" label="创建时间" width="180" />
        <el-table-column label="操作" width="200">
          <template #default="{ row }">
            <el-button type="primary" link @click="handleEdit(row)">编辑</el-button>
            <el-button type="danger" link @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 新增/编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogType === 'add' ? '新增账户' : '编辑账户'"
      width="500px"
    >
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="100px"
      >
        <el-form-item label="账户名称" prop="accountName">
          <el-input v-model="form.accountName" />
        </el-form-item>
        <el-form-item label="账户类型" prop="accountType">
          <el-select v-model="form.accountType" style="width: 100%">
            <el-option label="资产" value="asset" />
            <el-option label="负债" value="liability" />
            <el-option label="收入" value="revenue" />
            <el-option label="支出" value="expense" />
          </el-select>
        </el-form-item>
        <el-form-item label="初始余额" prop="balance">
          <el-input-number v-model="form.balance" :precision="2" style="width: 100%" />
        </el-form-item>
        <el-form-item label="币种" prop="currency">
          <el-select v-model="form.currency" style="width: 100%">
            <el-option label="人民币" value="CNY" />
            <el-option label="美元" value="USD" />
            <el-option label="欧元" value="EUR" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import type { FormInstance } from 'element-plus'

const accounts = ref([
  {
    id: 1,
    accountName: '主营业务收入',
    accountType: 'revenue',
    balance: 1234567.89,
    currency: 'CNY',
    createTime: '2024-03-15 10:00:00'
  },
  {
    id: 2,
    accountName: '库存商品',
    accountType: 'asset',
    balance: 890123.45,
    currency: 'CNY',
    createTime: '2024-03-15 10:00:00'
  }
])

const dialogVisible = ref(false)
const dialogType = ref<'add' | 'edit'>('add')
const formRef = ref<FormInstance>()

const form = reactive({
  id: 0,
  accountName: '',
  accountType: '',
  balance: 0,
  currency: 'CNY'
})

const rules = {
  accountName: [
    { required: true, message: '请输入账户名称', trigger: 'blur' }
  ],
  accountType: [
    { required: true, message: '请选择账户类型', trigger: 'change' }
  ],
  currency: [
    { required: true, message: '请选择币种', trigger: 'change' }
  ]
}

const getAccountTypeTag = (type: string) => {
  const typeMap: Record<string, string> = {
    asset: 'success',
    liability: 'danger',
    revenue: 'warning',
    expense: 'info'
  }
  return typeMap[type] || ''
}

const handleAdd = () => {
  dialogType.value = 'add'
  form.id = 0
  form.accountName = ''
  form.accountType = ''
  form.balance = 0
  form.currency = 'CNY'
  dialogVisible.value = true
}

const handleEdit = (row: any) => {
  dialogType.value = 'edit'
  Object.assign(form, row)
  dialogVisible.value = true
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
.accounts-container {
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