<template>
  <div class="budgets-container">
    <div class="header-actions">
      <el-button type="primary" @click="handleAdd">
        <el-icon><Plus /></el-icon>新建预算
      </el-button>
      <el-input
        v-model="searchQuery"
        placeholder="搜索部门"
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
      :data="budgets"
      border
      style="width: 100%"
    >
      <el-table-column prop="budget_id" label="ID" width="80" />
      <el-table-column prop="department" label="部门" />
      <el-table-column prop="category" label="类别" />
      <el-table-column prop="amount" label="预算金额">
        <template #default="{ row }">
          ¥{{ formatNumber(row.amount) }}
        </template>
      </el-table-column>
      <el-table-column prop="actual_amount" label="实际支出">
        <template #default="{ row }">
          ¥{{ formatNumber(row.actual_amount || 0) }}
        </template>
      </el-table-column>
      <el-table-column label="执行进度">
        <template #default="{ row }">
          <el-progress
            :percentage="calculateProgress(row.actual_amount, row.amount)"
            :status="getProgressStatus(row.actual_amount, row.amount)"
          />
        </template>
      </el-table-column>
      <el-table-column prop="status" label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="getStatusType(row.status)">
            {{ getStatusLabel(row.status) }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="200" fixed="right">
        <template #default="{ row }">
          <el-button-group>
            <el-button type="primary" @click="handleEdit(row)">编辑</el-button>
            <el-button
              type="warning"
              @click="handleAdjust(row)"
            >
              调整
            </el-button>
          </el-button-group>
        </template>
      </el-table-column>
    </el-table>

    <!-- 预算表单对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑预算' : '新建预算'"
      width="500px"
    >
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="100px"
      >
        <el-form-item label="部门" prop="department">
          <el-input v-model="form.department" />
        </el-form-item>
        <el-form-item label="类别" prop="category">
          <el-input v-model="form.category" />
        </el-form-item>
        <el-form-item label="预算金额" prop="amount">
          <el-input-number
            v-model="form.amount"
            :precision="2"
            :step="1000"
            :min="0"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="开始日期" prop="period_start">
          <el-date-picker
            v-model="form.period_start"
            type="date"
            placeholder="选择开始日期"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="结束日期" prop="period_end">
          <el-date-picker
            v-model="form.period_end"
            type="date"
            placeholder="选择结束日期"
            style="width: 100%"
          />
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

    <!-- 调整对话框 -->
    <el-dialog
      v-model="adjustDialogVisible"
      title="调整实际支出"
      width="400px"
    >
      <el-form
        ref="adjustFormRef"
        :model="adjustForm"
        :rules="adjustRules"
        label-width="100px"
      >
        <el-form-item label="实际支出" prop="actual_amount">
          <el-input-number
            v-model="adjustForm.actual_amount"
            :precision="2"
            :step="1000"
            :min="0"
            style="width: 100%"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="adjustDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleAdjustSubmit">
            确认
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus, Search } from '@element-plus/icons-vue'
import type { FormInstance } from 'element-plus'
import { financeApi } from '@/api/modules/finance'
import type { Budget } from '@/types/models'

// 状态
const loading = ref(false)
const budgets = ref<Budget[]>([])
const searchQuery = ref('')
const dialogVisible = ref(false)
const adjustDialogVisible = ref(false)
const isEdit = ref(false)
const formRef = ref<FormInstance>()
const adjustFormRef = ref<FormInstance>()
const currentBudget = ref<Budget | null>(null)

// 表单数据
interface BudgetForm {
  budget_id?: number
  department: string
  category: string
  amount: number
  period_start: string
  period_end: string
  status: string
}

const form = ref<BudgetForm>({
  department: '',
  category: '',
  amount: 0,
  period_start: '',
  period_end: '',
  status: 'active'
})

// 调整表单数据
const adjustForm = ref({
  actual_amount: 0
})

// 表单验证规则
const rules = {
  department: [
    { required: true, message: '请输入部门', trigger: 'blur' }
  ],
  category: [
    { required: true, message: '请输入类别', trigger: 'blur' }
  ],
  amount: [
    { required: true, message: '请输入预算金额', trigger: 'blur' }
  ],
  period_start: [
    { required: true, message: '请选择开始日期', trigger: 'change' }
  ],
  period_end: [
    { required: true, message: '请选择结束日期', trigger: 'change' }
  ]
}

// 调整表单验证规则
const adjustRules = {
  actual_amount: [
    { required: true, message: '请输入实际支出', trigger: 'blur' }
  ]
}

// 格式化数字
const formatNumber = (num: number) => {
  return num.toLocaleString('zh-CN')
}

// 计算预算执行进度
const calculateProgress = (actual: number = 0, total: number) => {
  return Math.round((actual / total) * 100)
}

// 获取进度条状态
const getProgressStatus = (actual: number = 0, total: number) => {
  const progress = (actual / total) * 100
  if (progress > 90) return 'warning'
  if (progress > 100) return 'exception'
  return 'success'
}

// 获取状态类型
const getStatusType = (status: string) => {
  const types: Record<string, string> = {
    active: 'success',
    completed: 'info',
    overbudget: 'danger'
  }
  return types[status] || 'info'
}

// 获取状态标签
const getStatusLabel = (status: string) => {
  const labels: Record<string, string> = {
    active: '执行中',
    completed: '已完成',
    overbudget: '超预算'
  }
  return labels[status] || status
}

// 获取预算列表
const fetchBudgets = async () => {
  try {
    loading.value = true
    const response = await financeApi.budgets.getBudgets()
    budgets.value = response.data
  } catch (error) {
    ElMessage.error('获取预算列表失败')
  } finally {
    loading.value = false
  }
}

// 搜索处理
const handleSearch = () => {
  // 实现搜索逻辑
  console.log('搜索:', searchQuery.value)
}

// 添加预算
const handleAdd = () => {
  isEdit.value = false
  form.value = {
    department: '',
    category: '',
    amount: 0,
    period_start: '',
    period_end: '',
    status: 'active'
  }
  dialogVisible.value = true
}

// 编辑预算
const handleEdit = (row: Budget) => {
  isEdit.value = true
  form.value = { ...row }
  dialogVisible.value = true
}

// 调整预算
const handleAdjust = (row: Budget) => {
  currentBudget.value = row
  adjustForm.value.actual_amount = row.actual_amount || 0
  adjustDialogVisible.value = true
}

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
    
    if (isEdit.value && form.value.budget_id) {
      await financeApi.budgets.updateBudget(form.value.budget_id, form.value)
      ElMessage.success('更新成功')
    } else {
      await financeApi.budgets.createBudget(form.value)
      ElMessage.success('添加成功')
    }
    
    dialogVisible.value = false
    await fetchBudgets()
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

// 提交调整
const handleAdjustSubmit = async () => {
  if (!adjustFormRef.value || !currentBudget.value) return
  
  try {
    await adjustFormRef.value.validate()
    
    await financeApi.budgets.updateActualAmount(
      currentBudget.value.budget_id,
      adjustForm.value.actual_amount
    )
    
    ElMessage.success('调整成功')
    adjustDialogVisible.value = false
    await fetchBudgets()
  } catch (error) {
    ElMessage.error('调整失败')
  }
}

// 初始化
onMounted(() => {
  fetchBudgets()
})
</script>

<style scoped>
.budgets-container {
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