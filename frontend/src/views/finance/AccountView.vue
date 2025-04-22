<template>
  <div class="account-container">
    <div class="toolbar">
      <el-button type="primary" @click="handleAdd">
        新增账户
      </el-button>
    </div>

    <el-table :data="accounts" style="width: 100%" v-loading="loading">
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="name" label="账户名称" />
      <el-table-column prop="type" label="账户类型">
        <template #default="{ row }: { row: Account }">
          <el-tag>{{ accountTypes[row.type] }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="balance" label="余额">
        <template #default="{ row }: { row: Account }">
          <span :class="{ 'text-red': row.balance < 0 }">
            ¥ {{ row.balance.toFixed(2) }}
          </span>
        </template>
      </el-table-column>
      <el-table-column prop="status" label="状态" width="100">
        <template #default="{ row }: { row: Account }">
          <el-tag :type="row.status === 'active' ? 'success' : 'danger'">
            {{ row.status === 'active' ? '启用' : '禁用' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="200" fixed="right">
        <template #default="{ row }: { row: Account }">
          <el-button-group>
            <el-button type="primary" @click="handleEdit(row)" :icon="Edit">编辑</el-button>
            <el-button type="danger" @click="handleDelete(row)" :icon="Delete">删除</el-button>
          </el-button-group>
        </template>
      </el-table-column>
    </el-table>

    <!-- 账户表单对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogType === 'add' ? '新增账户' : '编辑账户'"
      width="500px"
    >
      <el-form
        ref="accountFormRef"
        :model="accountForm"
        :rules="rules"
        label-width="100px"
      >
        <el-form-item label="账户名称" prop="name">
          <el-input v-model="accountForm.name" />
        </el-form-item>
        <el-form-item label="账户类型" prop="type">
          <el-select v-model="accountForm.type" style="width: 100%">
            <el-option
              v-for="(name, type) in accountTypes"
              :key="type"
              :label="name"
              :value="type"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="初始余额" prop="balance">
          <el-input-number
            v-model="accountForm.balance"
            :precision="2"
            :step="100"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-select v-model="accountForm.status" style="width: 100%">
            <el-option label="启用" value="active" />
            <el-option label="禁用" value="inactive" />
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
import { ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { FormInstance } from 'element-plus'
import { Edit, Delete } from '@element-plus/icons-vue'

// 账户类型
type AccountType = 'cash' | 'bank' | 'alipay' | 'wechat' | 'credit' | 'other'

const accountTypes: Record<AccountType, string> = {
  cash: '现金',
  bank: '银行账户',
  alipay: '支付宝',
  wechat: '微信支付',
  credit: '信用卡',
  other: '其他'
}

interface Account {
  id: number
  name: string
  type: AccountType
  balance: number
  status: 'active' | 'inactive'
}

// 状态定义
const loading = ref(false)
const dialogVisible = ref(false)
const dialogType = ref<'add' | 'edit'>('add')
const accountFormRef = ref<FormInstance>()

// 表单数据
const accountForm = ref<Account>({
  id: 0,
  name: '',
  type: 'bank',
  balance: 0,
  status: 'active'
})

// 表单验证规则
const rules = {
  name: [
    { required: true, message: '请输入账户名称', trigger: 'blur' },
    { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
  ],
  type: [
    { required: true, message: '请选择账户类型', trigger: 'change' }
  ],
  status: [
    { required: true, message: '请选择状态', trigger: 'change' }
  ]
}

// 模拟数据
const accounts = ref<Account[]>([
  {
    id: 1,
    name: '企业基本户',
    type: 'bank',
    balance: 100000.00,
    status: 'active'
  },
  {
    id: 2,
    name: '微信商户号',
    type: 'wechat',
    balance: 50000.00,
    status: 'active'
  },
  {
    id: 3,
    name: '备用金',
    type: 'cash',
    balance: 5000.00,
    status: 'active'
  }
])

// 处理新增
const handleAdd = () => {
  dialogType.value = 'add'
  accountForm.value = {
    id: 0,
    name: '',
    type: 'bank',
    balance: 0,
    status: 'active'
  }
  dialogVisible.value = true
}

// 处理编辑
const handleEdit = (row: Account) => {
  dialogType.value = 'edit'
  accountForm.value = { ...row }
  dialogVisible.value = true
}

// 处理删除
const handleDelete = (row: Account) => {
  ElMessageBox.confirm(
    '确定要删除该账户吗？删除后将无法恢复。',
    '警告',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  )
    .then(() => {
      // 这里应该调用删除API
      const index = accounts.value.findIndex(item => item.id === row.id)
      if (index > -1) {
        accounts.value.splice(index, 1)
        ElMessage.success('删除成功')
      }
    })
    .catch(() => {
      ElMessage.info('已取消删除')
    })
}

// 处理表单提交
const handleSubmit = async () => {
  if (!accountFormRef.value) return

  await accountFormRef.value.validate((valid, fields) => {
    if (valid) {
      // 这里应该调用添加/更新API
      if (dialogType.value === 'add') {
        accountForm.value.id = accounts.value.length + 1
        accounts.value.push({ ...accountForm.value })
        ElMessage.success('添加成功')
      } else {
        const index = accounts.value.findIndex(item => item.id === accountForm.value.id)
        if (index > -1) {
          accounts.value[index] = { ...accountForm.value }
          ElMessage.success('更新成功')
        }
      }
      dialogVisible.value = false
    } else {
      console.error('表单验证失败:', fields)
    }
  })
}
</script>

<style scoped>
.account-container {
  padding: 20px 0;
}

.toolbar {
  margin-bottom: 20px;
}

.text-red {
  color: #f56c6c;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style> 