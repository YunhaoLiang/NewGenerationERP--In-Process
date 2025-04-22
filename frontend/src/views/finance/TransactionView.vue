<template>
  <div class="transaction-container">
    <div class="toolbar">
      <el-button type="primary" @click="handleAdd">
        新增交易
      </el-button>
      <el-date-picker
        v-model="dateRange"
        type="daterange"
        range-separator="至"
        start-placeholder="开始日期"
        end-placeholder="结束日期"
        :shortcuts="dateShortcuts"
        @change="handleDateChange"
        class="date-picker"
      />
    </div>

    <el-table :data="transactions" style="width: 100%" v-loading="loading">
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="date" label="交易日期" width="120">
        <template #default="{ row }: { row: Transaction }">
          {{ formatDate(row.date) }}
        </template>
      </el-table-column>
      <el-table-column prop="type" label="类型" width="100">
        <template #default="{ row }: { row: Transaction }">
          <el-tag :type="row.type === 'income' ? 'success' : 'danger'">
            {{ row.type === 'income' ? '收入' : '支出' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="amount" label="金额" width="120">
        <template #default="{ row }: { row: Transaction }">
          <span :class="{ 'text-red': row.type === 'expense' }">
            {{ row.type === 'expense' ? '-' : '+' }} ¥ {{ row.amount.toFixed(2) }}
          </span>
        </template>
      </el-table-column>
      <el-table-column prop="category" label="类别" />
      <el-table-column prop="account" label="账户" />
      <el-table-column prop="description" label="描述" show-overflow-tooltip />
      <el-table-column label="操作" width="200" fixed="right">
        <template #default="{ row }: { row: Transaction }">
          <el-button-group>
            <el-button type="primary" @click="handleEdit(row)" :icon="Edit">编辑</el-button>
            <el-button type="danger" @click="handleDelete(row)" :icon="Delete">删除</el-button>
          </el-button-group>
        </template>
      </el-table-column>
    </el-table>

    <!-- 交易表单对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogType === 'add' ? '新增交易' : '编辑交易'"
      width="500px"
    >
      <el-form
        ref="transactionFormRef"
        :model="transactionForm"
        :rules="rules"
        label-width="100px"
      >
        <el-form-item label="交易类型" prop="type">
          <el-select v-model="transactionForm.type" style="width: 100%">
            <el-option label="收入" value="income" />
            <el-option label="支出" value="expense" />
          </el-select>
        </el-form-item>
        <el-form-item label="交易日期" prop="date">
          <el-date-picker
            v-model="transactionForm.date"
            type="date"
            placeholder="选择日期"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="金额" prop="amount">
          <el-input-number
            v-model="transactionForm.amount"
            :precision="2"
            :step="100"
            :min="0"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="类别" prop="category">
          <el-select v-model="transactionForm.category" style="width: 100%">
            <el-option-group
              v-for="group in categoryOptions"
              :key="group.type"
              :label="group.label"
            >
              <el-option
                v-for="item in group.options"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              />
            </el-option-group>
          </el-select>
        </el-form-item>
        <el-form-item label="账户" prop="account">
          <el-select v-model="transactionForm.account" style="width: 100%">
            <el-option
              v-for="account in accountOptions"
              :key="account.value"
              :label="account.label"
              :value="account.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input
            v-model="transactionForm.description"
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
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { FormInstance } from 'element-plus'
import { Edit, Delete } from '@element-plus/icons-vue'

interface Transaction {
  id: number
  date: Date
  type: 'income' | 'expense'
  amount: number
  category: string
  account: string
  description: string
}

// 日期快捷选项
const dateShortcuts = [
  {
    text: '最近一周',
    value: () => {
      const end = new Date()
      const start = new Date()
      start.setTime(start.getTime() - 3600 * 1000 * 24 * 7)
      return [start, end]
    }
  },
  {
    text: '最近一个月',
    value: () => {
      const end = new Date()
      const start = new Date()
      start.setMonth(start.getMonth() - 1)
      return [start, end]
    }
  },
  {
    text: '最近三个月',
    value: () => {
      const end = new Date()
      const start = new Date()
      start.setMonth(start.getMonth() - 3)
      return [start, end]
    }
  }
]

// 类别选项
const categoryOptions = [
  {
    type: 'income',
    label: '收入类别',
    options: [
      { value: 'salary', label: '工资' },
      { value: 'bonus', label: '奖金' },
      { value: 'investment', label: '投资收益' },
      { value: 'other_income', label: '其他收入' }
    ]
  },
  {
    type: 'expense',
    label: '支出类别',
    options: [
      { value: 'office', label: '办公用品' },
      { value: 'utility', label: '水电费' },
      { value: 'rent', label: '房租' },
      { value: 'salary_expense', label: '工资支出' },
      { value: 'other_expense', label: '其他支出' }
    ]
  }
]

// 账户选项
const accountOptions = [
  { value: '1', label: '企业基本户' },
  { value: '2', label: '微信商户号' },
  { value: '3', label: '备用金' }
]

// 状态定义
const loading = ref(false)
const dialogVisible = ref(false)
const dialogType = ref<'add' | 'edit'>('add')
const transactionFormRef = ref<FormInstance>()
const dateRange = ref<[Date, Date] | null>(null)

// 表单数据
const transactionForm = ref<Omit<Transaction, 'id'> & { id?: number }>({
  date: new Date(),
  type: 'expense',
  amount: 0,
  category: '',
  account: '',
  description: ''
})

// 表单验证规则
const rules = {
  type: [
    { required: true, message: '请选择交易类型', trigger: 'change' }
  ],
  date: [
    { required: true, message: '请选择交易日期', trigger: 'change' }
  ],
  amount: [
    { required: true, message: '请输入交易金额', trigger: 'blur' }
  ],
  category: [
    { required: true, message: '请选择交易类别', trigger: 'change' }
  ],
  account: [
    { required: true, message: '请选择账户', trigger: 'change' }
  ]
}

// 模拟数据
const transactions = ref<Transaction[]>([
  {
    id: 1,
    date: new Date('2024-04-01'),
    type: 'expense',
    amount: 5000,
    category: 'office',
    account: '企业基本户',
    description: '购买办公用品'
  },
  {
    id: 2,
    date: new Date('2024-04-05'),
    type: 'income',
    amount: 100000,
    category: 'investment',
    account: '企业基本户',
    description: '投资收益'
  },
  {
    id: 3,
    date: new Date('2024-04-10'),
    type: 'expense',
    amount: 30000,
    category: 'salary_expense',
    account: '企业基本户',
    description: '发放员工工资'
  }
])

// 格式化日期
const formatDate = (date: Date) => {
  return new Date(date).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  })
}

// 处理日期变更
const handleDateChange = () => {
  // 这里应该调用查询API
  console.log('日期范围:', dateRange.value)
}

// 处理新增
const handleAdd = () => {
  dialogType.value = 'add'
  transactionForm.value = {
    date: new Date(),
    type: 'expense',
    amount: 0,
    category: '',
    account: '',
    description: ''
  }
  dialogVisible.value = true
}

// 处理编辑
const handleEdit = (row: Transaction) => {
  dialogType.value = 'edit'
  transactionForm.value = { ...row }
  dialogVisible.value = true
}

// 处理删除
const handleDelete = (row: Transaction) => {
  ElMessageBox.confirm(
    '确定要删除该交易记录吗？删除后将无法恢复。',
    '警告',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  )
    .then(() => {
      // 这里应该调用删除API
      const index = transactions.value.findIndex(item => item.id === row.id)
      if (index > -1) {
        transactions.value.splice(index, 1)
        ElMessage.success('删除成功')
      }
    })
    .catch(() => {
      ElMessage.info('已取消删除')
    })
}

// 处理表单提交
const handleSubmit = async () => {
  if (!transactionFormRef.value) return

  await transactionFormRef.value.validate((valid, fields) => {
    if (valid) {
      // 这里应该调用添加/更新API
      if (dialogType.value === 'add') {
        const newTransaction = {
          ...transactionForm.value,
          id: transactions.value.length + 1
        }
        transactions.value.push(newTransaction)
        ElMessage.success('添加成功')
      } else if (transactionForm.value.id) {
        const index = transactions.value.findIndex(item => item.id === transactionForm.value.id)
        if (index > -1) {
          transactions.value[index] = { ...transactionForm.value as Transaction }
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
.transaction-container {
  padding: 20px 0;
}

.toolbar {
  margin-bottom: 20px;
  display: flex;
  gap: 16px;
}

.date-picker {
  width: 300px;
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