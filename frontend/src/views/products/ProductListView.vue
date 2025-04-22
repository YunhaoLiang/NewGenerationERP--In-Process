<template>
  <div class="product-list-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>产品管理</span>
          <el-button type="primary" @click="handleAdd">新增产品</el-button>
        </div>
      </template>

      <!-- 搜索栏 -->
      <div class="search-bar">
        <el-input
          v-model="searchQuery"
          placeholder="搜索产品名称"
          class="search-input"
          clearable
          @clear="handleSearch"
          @input="handleSearch"
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
        <el-select
          v-model="categoryFilter"
          placeholder="产品类别"
          clearable
          class="filter-select"
          @change="handleSearch"
        >
          <el-option
            v-for="item in categories"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          />
        </el-select>
      </div>

      <!-- 产品表格 -->
      <el-table
        :data="filteredProducts"
        style="width: 100%"
        v-loading="loading"
      >
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="产品名称" />
        <el-table-column prop="category" label="类别" />
        <el-table-column prop="price" label="价格">
          <template #default="{ row }">
            ¥{{ row.price.toFixed(2) }}
          </template>
        </el-table-column>
        <el-table-column prop="stock" label="库存" />
        <el-table-column prop="status" label="状态">
          <template #default="{ row }">
            <el-tag :type="getStatusTagType(row.status)">
              {{ row.status === 'active' ? '在售' : '停售' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200">
          <template #default="{ row }">
            <el-button
              type="primary"
              link
              @click="handleEdit(row)"
            >
              编辑
            </el-button>
            <el-button
              type="danger"
              link
              @click="handleDelete(row)"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="total"
          layout="total, sizes, prev, pager, next"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>

    <!-- 产品表单对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogType === 'add' ? '新增产品' : '编辑产品'"
      width="500px"
    >
      <el-form
        ref="productFormRef"
        :model="productForm"
        :rules="productRules"
        label-width="80px"
      >
        <el-form-item label="产品名称" prop="name">
          <el-input v-model="productForm.name" />
        </el-form-item>
        <el-form-item label="类别" prop="category">
          <el-select v-model="productForm.category" placeholder="请选择类别">
            <el-option
              v-for="item in categories"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="价格" prop="price">
          <el-input-number
            v-model="productForm.price"
            :precision="2"
            :step="0.1"
            :min="0"
          />
        </el-form-item>
        <el-form-item label="库存" prop="stock">
          <el-input-number
            v-model="productForm.stock"
            :min="0"
            :step="1"
          />
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-radio-group v-model="productForm.status">
            <el-radio value="active">在售</el-radio>
            <el-radio value="inactive">停售</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input
            v-model="productForm.description"
            type="textarea"
            :rows="3"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit">
            确定
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { FormInstance } from 'element-plus'
import { Search } from '@element-plus/icons-vue'

interface Product {
  id: number
  name: string
  category: string
  price: number
  stock: number
  status: 'active' | 'inactive'
  description: string
}

// 搜索相关
const searchQuery = ref('')
const categoryFilter = ref('')
const categories = [
  { label: '电子产品', value: 'electronics' },
  { label: '办公用品', value: 'office' },
  { label: '家具', value: 'furniture' }
]

const filteredProducts = computed(() => {
  let result = products.value
  if (searchQuery.value) {
    result = result.filter(product =>
      product.name.toLowerCase().includes(searchQuery.value.toLowerCase())
    )
  }
  if (categoryFilter.value) {
    result = result.filter(product => product.category === categoryFilter.value)
  }
  return result
})

// 分页相关
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)

// 产品数据
const products = ref<Product[]>([
  {
    id: 1,
    name: '笔记本电脑',
    category: 'electronics',
    price: 5999.00,
    stock: 100,
    status: 'active',
    description: '高性能笔记本电脑'
  },
  {
    id: 2,
    name: '办公椅',
    category: 'furniture',
    price: 299.00,
    stock: 50,
    status: 'active',
    description: '舒适办公椅'
  }
])

// 加载状态
const loading = ref(false)

// 对话框相关
const dialogVisible = ref(false)
const dialogType = ref<'add' | 'edit'>('add')
const productFormRef = ref<FormInstance>()
const productForm = ref({
  id: 0,
  name: '',
  category: '',
  price: 0,
  stock: 0,
  status: 'active',
  description: ''
})

// 表单验证规则
const productRules = {
  name: [
    { required: true, message: '请输入产品名称', trigger: 'blur' }
  ],
  category: [
    { required: true, message: '请选择产品类别', trigger: 'change' }
  ],
  price: [
    { required: true, message: '请输入产品价格', trigger: 'blur' }
  ],
  stock: [
    { required: true, message: '请输入库存数量', trigger: 'blur' }
  ],
  status: [
    { required: true, message: '请选择产品状态', trigger: 'change' }
  ]
}

// 获取状态标签类型
const getStatusTagType = (status: string) => {
  return status === 'active' ? 'success' : 'info'
}

// 搜索处理
const handleSearch = () => {
  currentPage.value = 1
}

// 分页处理
const handleSizeChange = (val: number) => {
  pageSize.value = val
  currentPage.value = 1
}

const handleCurrentChange = (val: number) => {
  currentPage.value = val
}

// 新增产品
const handleAdd = () => {
  dialogType.value = 'add'
  productForm.value = {
    id: 0,
    name: '',
    category: '',
    price: 0,
    stock: 0,
    status: 'active',
    description: ''
  }
  dialogVisible.value = true
}

// 编辑产品
const handleEdit = (row: Product) => {
  dialogType.value = 'edit'
  productForm.value = { ...row }
  dialogVisible.value = true
}

// 删除产品
const handleDelete = (row: Product) => {
  ElMessageBox.confirm(
    `确定要删除产品 ${row.name} 吗？`,
    '警告',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(() => {
    // TODO: 调用删除API
    ElMessage.success('删除成功')
  }).catch(() => {})
}

// 提交表单
const handleSubmit = async () => {
  if (!productFormRef.value) return
  
  try {
    await productFormRef.value.validate()
    // TODO: 调用新增/编辑API
    ElMessage.success(dialogType.value === 'add' ? '新增成功' : '编辑成功')
    dialogVisible.value = false
  } catch (error) {
    console.error('表单验证失败:', error)
  }
}
</script>

<style scoped>
.product-list-container {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.search-bar {
  margin-bottom: 20px;
  display: flex;
  gap: 16px;
}

.search-input {
  width: 300px;
}

.filter-select {
  width: 200px;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style> 