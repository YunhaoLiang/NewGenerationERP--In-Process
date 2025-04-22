<template>
  <div class="budget-container">
    <div class="toolbar">
      <el-button type="primary" @click="handleAdd">
        新增预算
      </el-button>
      <el-select v-model="currentYear" class="year-select" @change="handleYearChange">
        <el-option
          v-for="year in years"
          :key="year"
          :label="year + '年'"
          :value="year"
        ></el-option>
      </el-select>
    </div>

    <el-table :data="budgets" style="width: 100%" v-loading="loading">
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="category" label="类别">
        <template #default="{ row }: { row: Budget }">
          <el-tag>{{ categoryMap[row.category] }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="amount" label="预算金额">
        <template #default="{ row }: { row: Budget }">
          ¥ {{ row.amount.toFixed(2) }}
        </template>
      </el-table-column>
      <el-table-column prop="used" label="已使用">
        <template #default="{ row }: { row: Budget }">
          <span :class="{ 'text-red': row.used > row.amount }">
            ¥ {{ row.used.toFixed(2) }}
          </span>
        </template>
      </el-table-column>
      <el-table-column label="使用进度" width="200">
        <template #default="{ row }: { row: Budget }">
          <el-progress
            :percentage="Math.min(Math.round((row.used / row.amount) * 100), 100)"
            :status="row.used > row.amount ? 'exception' : ''"
          ></el-progress>
        </template>
      </el-table-column>
      <el-table-column prop="description" label="描述" show-overflow-tooltip />
      <el-table-column label="操作" width="200" fixed="right">
        <template #default="{ row }: { row: Budget }">
          <el-button-group>
            <el-button type="primary" @click="handleEdit(row)" :icon="Edit">编辑</el-button>
            <el-button type="danger" @click="handleDelete(row)" :icon="Delete">删除</el-button>
          </el-button-group>
        </template>
      </el-table-column>
    </el-table>

    <!-- 预算表单对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogType === 'add' ? '新增预算' : '编辑预算'"
      width="500px"
    >
      <el-form
        ref="budgetFormRef"
        :model="budgetForm"
        :rules="rules"
        label-width="100px"
      >
        <el-form-item label="预算类别" prop="category">
          <el-select v-model="budgetForm.category" style="width: 100%">
            <el-option
              v-for="(name, category) in categoryMap"
              :key="category"
              :label="name"
              :value="category"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="预算金额" prop="amount">
          <el-input-number
            v-model="budgetForm.amount"
            :precision="2"
            :step="1000"
            :min="0"
            style="width: 100%"
          ></el-input-number>
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input
            v-model="budgetForm.description"
            type="textarea"
            :rows="3"
            placeholder="请输入预算描述"
          ></el-input>
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
import { ref, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { FormInstance } from 'element-plus'
import { Edit, Delete } from '@element-plus/icons-vue'

interface Budget {
  id: number
  category: string
  amount: number
  used: number
  description: string
  year: number
}

// 预算类别
const categoryMap: Record<string, string> = {
  office: '办公用品',
  utility: '水电费',
  rent: '房租',
  salary: '工资支出',
  marketing: '市场营销',
  travel: '差旅费',
  other: '其他支出'
}

// 生成年份选项（前5年到后5年）
const currentYear = ref(new Date().getFullYear())
const years = computed(() => {
  const year = currentYear.value
  return Array.from({ length: 11 }, (_, i) => year - 5 + i)
})

// 状态定义
const loading = ref(false)
const dialogVisible = ref(false)
const dialogType = ref<'add' | 'edit'>('add')
const budgetFormRef = ref<FormInstance>()

// 表单数据
const budgetForm = ref<Omit<Budget, 'id' | 'used' | 'year'> & { id?: number }>({
  category: '',
  amount: 0,
  description: ''
})

// 表单验证规则
const rules = {
  category: [
    { required: true, message: '请选择预算类别', trigger: 'change' }
  ],
  amount: [
    { required: true, message: '请输入预算金额', trigger: 'blur' }
  ]
}

// 模拟数据
const budgets = ref<Budget[]>([
  {
    id: 1,
    category: 'office',
    amount: 50000,
    used: 30000,
    description: '办公用品预算',
    year: 2024
  },
  {
    id: 2,
    category: 'salary',
    amount: 1000000,
    used: 750000,
    description: '员工工资预算',
    year: 2024
  },
  {
    id: 3,
    category: 'marketing',
    amount: 200000,
    used: 220000,
    description: '市场营销预算',
    year: 2024
  }
])

// 处理年份变更
const handleYearChange = () => {
  // 这里应该调用查询API
  console.log('选择年份:', currentYear.value)
}

// 处理新增
const handleAdd = () => {
  dialogType.value = 'add'
  budgetForm.value = {
    category: '',
    amount: 0,
    description: ''
  }
  dialogVisible.value = true
}

// 处理编辑
const handleEdit = (row: Budget) => {
  dialogType.value = 'edit'
  budgetForm.value = {
    id: row.id,
    category: row.category,
    amount: row.amount,
    description: row.description
  }
  dialogVisible.value = true
}

// 处理删除
const handleDelete = (row: Budget) => {
  ElMessageBox.confirm(
    '确定要删除该预算吗？删除后将无法恢复。',
    '警告',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  )
    .then(() => {
      // 这里应该调用删除API
      const index = budgets.value.findIndex(item => item.id === row.id)
      if (index > -1) {
        budgets.value.splice(index, 1)
        ElMessage.success('删除成功')
      }
    })
    .catch(() => {
      ElMessage.info('已取消删除')
    })
}

// 处理表单提交
const handleSubmit = async () => {
  if (!budgetFormRef.value) return

  await budgetFormRef.value.validate((valid, fields) => {
    if (valid) {
      // 这里应该调用添加/更新API
      if (dialogType.value === 'add') {
        const newBudget: Budget = {
          ...budgetForm.value,
          id: budgets.value.length + 1,
          used: 0,
          year: currentYear.value
        }
        budgets.value.push(newBudget)
        ElMessage.success('添加成功')
      } else if (budgetForm.value.id) {
        const index = budgets.value.findIndex(item => item.id === budgetForm.value.id)
        if (index > -1) {
          budgets.value[index] = {
            ...budgets.value[index],
            ...budgetForm.value,
            year: currentYear.value
          }
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
.budget-container {
  padding: 20px 0;
}

.toolbar {
  margin-bottom: 20px;
  display: flex;
  gap: 16px;
}

.year-select {
  width: 120px;
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