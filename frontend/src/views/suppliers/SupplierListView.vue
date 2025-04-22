<template>
  <div class="supplier-container">
    <el-card class="supplier-card">
      <template #header>
        <div class="card-header">
          <h3>供应商管理</h3>
          <el-button type="primary" @click="handleAdd">
            新增供应商
          </el-button>
        </div>
      </template>

      <!-- 搜索区域 -->
      <div class="search-area">
        <el-input
          v-model="searchQuery"
          placeholder="搜索供应商名称"
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

      <!-- 表格区域 -->
      <el-table :data="filteredSuppliers" style="width: 100%" v-loading="loading">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="供应商名称" />
        <el-table-column prop="contact" label="联系人" />
        <el-table-column prop="phone" label="联系电话" />
        <el-table-column prop="email" label="电子邮箱" />
        <el-table-column prop="address" label="地址" show-overflow-tooltip />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.status === 'active' ? 'success' : 'danger'">
              {{ row.status === 'active' ? '活跃' : '停用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button-group>
              <el-button type="primary" @click="handleEdit(row)" :icon="Edit">编辑</el-button>
              <el-button type="danger" @click="handleDelete(row)" :icon="Delete">删除</el-button>
            </el-button-group>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination-container">
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

    <!-- 供应商表单对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogType === 'add' ? '新增供应商' : '编辑供应商'"
      width="500px"
    >
      <el-form
        ref="supplierFormRef"
        :model="supplierForm"
        :rules="rules"
        label-width="100px"
      >
        <el-form-item label="供应商名称" prop="name">
          <el-input v-model="supplierForm.name" />
        </el-form-item>
        <el-form-item label="联系人" prop="contact">
          <el-input v-model="supplierForm.contact" />
        </el-form-item>
        <el-form-item label="联系电话" prop="phone">
          <el-input v-model="supplierForm.phone" />
        </el-form-item>
        <el-form-item label="电子邮箱" prop="email">
          <el-input v-model="supplierForm.email" />
        </el-form-item>
        <el-form-item label="地址" prop="address">
          <el-input v-model="supplierForm.address" type="textarea" />
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-select v-model="supplierForm.status" style="width: 100%">
            <el-option label="活跃" value="active" />
            <el-option label="停用" value="inactive" />
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
import { ref, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { FormInstance } from 'element-plus'
import { Search, Edit, Delete } from '@element-plus/icons-vue'

// 状态定义
const loading = ref(false)
const searchQuery = ref('')
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const dialogVisible = ref(false)
const dialogType = ref<'add' | 'edit'>('add')
const supplierFormRef = ref<FormInstance>()

// 表单数据
const supplierForm = ref({
  id: 0,
  name: '',
  contact: '',
  phone: '',
  email: '',
  address: '',
  status: 'active'
})

// 表单验证规则
const rules = {
  name: [
    { required: true, message: '请输入供应商名称', trigger: 'blur' },
    { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
  ],
  contact: [
    { required: true, message: '请输入联系人', trigger: 'blur' }
  ],
  phone: [
    { required: true, message: '请输入联系电话', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入电子邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
  ],
  status: [
    { required: true, message: '请选择状态', trigger: 'change' }
  ]
}

// 模拟数据
const suppliers = ref([
  {
    id: 1,
    name: '测试供应商1',
    contact: '张三',
    phone: '13800138000',
    email: 'test1@example.com',
    address: '北京市朝阳区xxx街道xxx号',
    status: 'active'
  },
  // 更多测试数据...
])

// 计算属性：过滤后的供应商列表
const filteredSuppliers = computed(() => {
  return suppliers.value.filter(supplier =>
    supplier.name.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})

// 处理搜索
const handleSearch = () => {
  currentPage.value = 1
}

// 处理分页
const handleSizeChange = (val: number) => {
  pageSize.value = val
  currentPage.value = 1
}

const handleCurrentChange = (val: number) => {
  currentPage.value = val
}

// 处理新增
const handleAdd = () => {
  dialogType.value = 'add'
  supplierForm.value = {
    id: 0,
    name: '',
    contact: '',
    phone: '',
    email: '',
    address: '',
    status: 'active'
  }
  dialogVisible.value = true
}

// 处理编辑
const handleEdit = (row: any) => {
  dialogType.value = 'edit'
  supplierForm.value = { ...row }
  dialogVisible.value = true
}

// 处理删除
const handleDelete = (row: any) => {
  ElMessageBox.confirm(
    '确定要删除该供应商吗？',
    '警告',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  )
    .then(() => {
      // 这里应该调用删除API
      const index = suppliers.value.findIndex(item => item.id === row.id)
      if (index > -1) {
        suppliers.value.splice(index, 1)
        ElMessage.success('删除成功')
      }
    })
    .catch(() => {
      ElMessage.info('已取消删除')
    })
}

// 处理表单提交
const handleSubmit = async () => {
  if (!supplierFormRef.value) return

  await supplierFormRef.value.validate((valid, fields) => {
    if (valid) {
      // 这里应该调用添加/更新API
      if (dialogType.value === 'add') {
        supplierForm.value.id = suppliers.value.length + 1
        suppliers.value.push({ ...supplierForm.value })
        ElMessage.success('添加成功')
      } else {
        const index = suppliers.value.findIndex(item => item.id === supplierForm.value.id)
        if (index > -1) {
          suppliers.value[index] = { ...supplierForm.value }
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
.supplier-container {
  padding: 20px;
}

.supplier-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.search-area {
  margin-bottom: 20px;
}

.search-input {
  width: 300px;
}

.pagination-container {
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