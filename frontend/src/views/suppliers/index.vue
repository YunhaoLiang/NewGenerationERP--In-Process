<template>
  <div class="suppliers-container">
    <div class="header-actions">
      <el-button type="primary" @click="handleAdd">
        <el-icon><Plus /></el-icon>添加供应商
      </el-button>
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

    <el-table
      v-loading="loading"
      :data="suppliers"
      border
      style="width: 100%"
    >
      <el-table-column prop="supplier_id" label="ID" width="80" />
      <el-table-column prop="supplier_name" label="供应商名称" />
      <el-table-column prop="contact_person" label="联系人" />
      <el-table-column prop="phone" label="联系电话" />
      <el-table-column prop="email" label="电子邮箱" show-overflow-tooltip />
      <el-table-column prop="address" label="地址" show-overflow-tooltip />
      <el-table-column prop="created_at" label="创建时间" width="180">
        <template #default="{ row }">
          {{ formatDate(row.created_at) }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="200" fixed="right">
        <template #default="{ row }">
          <el-button-group>
            <el-button type="primary" @click="handleEdit(row)">编辑</el-button>
            <el-button type="danger" @click="handleDelete(row)">删除</el-button>
          </el-button-group>
        </template>
      </el-table-column>
    </el-table>

    <!-- 供应商表单对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑供应商' : '添加供应商'"
      width="500px"
    >
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="100px"
      >
        <el-form-item label="供应商名称" prop="supplier_name">
          <el-input v-model="form.supplier_name" />
        </el-form-item>
        <el-form-item label="联系人" prop="contact_person">
          <el-input v-model="form.contact_person" />
        </el-form-item>
        <el-form-item label="联系电话" prop="phone">
          <el-input v-model="form.phone" />
        </el-form-item>
        <el-form-item label="电子邮箱" prop="email">
          <el-input v-model="form.email" />
        </el-form-item>
        <el-form-item label="地址" prop="address">
          <el-input
            v-model="form.address"
            type="textarea"
            :rows="3"
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
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Search } from '@element-plus/icons-vue'
import type { FormInstance } from 'element-plus'
import type { Supplier } from '@/types/models'

// 状态
const loading = ref(false)
const suppliers = ref<Supplier[]>([])
const searchQuery = ref('')
const dialogVisible = ref(false)
const isEdit = ref(false)
const formRef = ref<FormInstance>()

// 表单数据
const form = ref({
  supplier_name: '',
  contact_person: '',
  phone: '',
  email: '',
  address: ''
})

// 表单验证规则
const rules = {
  supplier_name: [
    { required: true, message: '请输入供应商名称', trigger: 'blur' },
    { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
  ],
  contact_person: [
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
  address: [
    { required: true, message: '请输入地址', trigger: 'blur' }
  ]
}

// 格式化日期
const formatDate = (date: string) => {
  return new Date(date).toLocaleString()
}

// 获取供应商列表
const fetchSuppliers = async () => {
  try {
    loading.value = true
    // 这里应该调用供应商列表API
    // const response = await supplierApi.getSuppliers()
    // suppliers.value = response.data
    
    // 模拟数据
    suppliers.value = []
  } catch (error) {
    ElMessage.error('获取供应商列表失败')
  } finally {
    loading.value = false
  }
}

// 搜索处理
const handleSearch = () => {
  // 实现搜索逻辑
  console.log('搜索:', searchQuery.value)
}

// 添加供应商
const handleAdd = () => {
  isEdit.value = false
  form.value = {
    supplier_name: '',
    contact_person: '',
    phone: '',
    email: '',
    address: ''
  }
  dialogVisible.value = true
}

// 编辑供应商
const handleEdit = (row: Supplier) => {
  isEdit.value = true
  form.value = {
    supplier_name: row.supplier_name,
    contact_person: row.contact_person,
    phone: row.phone,
    email: row.email,
    address: row.address
  }
  dialogVisible.value = true
}

// 删除供应商
const handleDelete = async (row: Supplier) => {
  try {
    await ElMessageBox.confirm(
      '确定要删除该供应商吗？此操作不可恢复',
      '警告',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    // 这里应该调用删除API
    // await supplierApi.deleteSupplier(row.supplier_id)
    ElMessage.success('删除成功')
    await fetchSuppliers()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
    
    // 这里应该调用创建/更新API
    // if (isEdit.value) {
    //   await supplierApi.updateSupplier(currentId, form.value)
    // } else {
    //   await supplierApi.createSupplier(form.value)
    // }
    
    ElMessage.success(isEdit.value ? '更新成功' : '添加成功')
    dialogVisible.value = false
    await fetchSuppliers()
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

// 初始化
onMounted(() => {
  fetchSuppliers()
})
</script>

<style scoped>
.suppliers-container {
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