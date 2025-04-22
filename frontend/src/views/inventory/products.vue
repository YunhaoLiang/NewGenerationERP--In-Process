<template>
  <div class="products-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <div class="header-left">
            <el-input
              v-model="searchQuery"
              placeholder="搜索产品"
              style="width: 200px"
              clearable
              @clear="handleSearch"
              @keyup.enter="handleSearch"
            >
              <template #prefix>
                <el-icon><Search /></el-icon>
              </template>
            </el-input>
            <el-select v-model="filterCategory" placeholder="产品类别" clearable @change="handleSearch">
              <el-option
                v-for="category in categories"
                :key="category.value"
                :label="category.label"
                :value="category.value"
              />
            </el-select>
          </div>
          <el-button type="primary" @click="handleAdd">新增产品</el-button>
        </div>
      </template>
      
      <el-table :data="products" style="width: 100%">
        <el-table-column prop="productCode" label="产品编码" width="120" />
        <el-table-column prop="name" label="产品名称" width="200" />
        <el-table-column prop="category" label="类别" width="120">
          <template #default="{ row }">
            <el-tag>{{ row.category }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="price" label="价格" width="120" />
        <el-table-column prop="stock" label="库存" width="120" />
        <el-table-column prop="unit" label="单位" width="80" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.status === '在售' ? 'success' : 'info'">
              {{ row.status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link @click="handleEdit(row)">编辑</el-button>
            <el-button type="success" link @click="handleStock(row)">库存</el-button>
            <el-button type="danger" link @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :total="total"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>

    <!-- 新增/编辑产品对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogType === 'add' ? '新增产品' : '编辑产品'"
      width="500px"
    >
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="100px"
      >
        <el-form-item label="产品编码" prop="productCode">
          <el-input v-model="form.productCode" :disabled="dialogType === 'edit'" />
        </el-form-item>
        <el-form-item label="产品名称" prop="name">
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="产品类别" prop="category">
          <el-select v-model="form.category" style="width: 100%">
            <el-option
              v-for="category in categories"
              :key="category.value"
              :label="category.label"
              :value="category.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="价格" prop="price">
          <el-input-number v-model="form.price" :precision="2" :step="0.01" style="width: 100%" />
        </el-form-item>
        <el-form-item label="单位" prop="unit">
          <el-input v-model="form.unit" />
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-select v-model="form.status" style="width: 100%">
            <el-option label="在售" value="在售" />
            <el-option label="下架" value="下架" />
          </el-select>
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input
            v-model="form.description"
            type="textarea"
            :rows="3"
            placeholder="请输入产品描述"
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

    <!-- 库存调整对话框 -->
    <el-dialog
      v-model="stockDialogVisible"
      title="库存调整"
      width="400px"
    >
      <el-form
        ref="stockFormRef"
        :model="stockForm"
        :rules="stockRules"
        label-width="100px"
      >
        <el-form-item label="当前库存">
          <span>{{ selectedProduct?.stock || 0 }}</span>
        </el-form-item>
        <el-form-item label="调整类型" prop="type">
          <el-select v-model="stockForm.type" style="width: 100%">
            <el-option label="入库" value="in" />
            <el-option label="出库" value="out" />
          </el-select>
        </el-form-item>
        <el-form-item label="调整数量" prop="quantity">
          <el-input-number v-model="stockForm.quantity" :min="1" style="width: 100%" />
        </el-form-item>
        <el-form-item label="备注" prop="remark">
          <el-input
            v-model="stockForm.remark"
            type="textarea"
            :rows="2"
            placeholder="请输入备注"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="stockDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleStockSubmit">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { Search } from '@element-plus/icons-vue'
import type { FormInstance } from 'element-plus'
import { ElMessage, ElMessageBox } from 'element-plus'
import axios from 'axios'

// 分页相关
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(100)

// 搜索和筛选
const searchQuery = ref('')
const filterCategory = ref('')

// 产品列表数据
const products = ref([])

// 加载产品列表
const loadProducts = async () => {
  try {
    const response = await axios.get('/api/products', {
      params: {
        page: currentPage.value,
        pageSize: pageSize.value,
        category: filterCategory.value,
        search: searchQuery.value
      }
    })
    products.value = response.data.items
    total.value = response.data.total
  } catch (error) {
    ElMessage.error('获取产品列表失败')
    console.error('Load products error:', error)
  }
}

// 产品类别
const categories = [
  { label: '笔记本电脑', value: '笔记本电脑' },
  { label: '台式电脑', value: '台式电脑' },
  { label: '显示器', value: '显示器' },
  { label: '配件', value: '配件' }
]

// 新增/编辑对话框
const dialogVisible = ref(false)
const dialogType = ref<'add' | 'edit'>('add')
const formRef = ref<FormInstance>()
const form = reactive({
  id: '',
  productCode: '',
  name: '',
  category: '',
  price: 0,
  unit: '',
  status: '在售',
  description: ''
})

const rules = {
  productCode: [
    { required: true, message: '请输入产品编码', trigger: 'blur' }
  ],
  name: [
    { required: true, message: '请输入产品名称', trigger: 'blur' }
  ],
  category: [
    { required: true, message: '请选择产品类别', trigger: 'change' }
  ],
  price: [
    { required: true, message: '请输入价格', trigger: 'blur' }
  ],
  unit: [
    { required: true, message: '请输入单位', trigger: 'blur' }
  ]
}

// 库存调整对话框
const stockDialogVisible = ref(false)
const stockFormRef = ref<FormInstance>()
const selectedProduct = ref<any>(null)
const stockForm = reactive({
  type: 'in',
  quantity: 1,
  remark: ''
})

const stockRules = {
  type: [
    { required: true, message: '请选择调整类型', trigger: 'change' }
  ],
  quantity: [
    { required: true, message: '请输入调整数量', trigger: 'blur' }
  ]
}

// 搜索和筛选方法
const handleSearch = () => {
  currentPage.value = 1
  loadProducts()
}

const handleSizeChange = (val: number) => {
  pageSize.value = val
  loadProducts()
}

const handleCurrentChange = (val: number) => {
  currentPage.value = val
  loadProducts()
}

// 产品相关方法
const handleAdd = () => {
  dialogType.value = 'add'
  form.productCode = ''
  form.name = ''
  form.category = ''
  form.price = 0
  form.unit = ''
  form.status = '在售'
  form.description = ''
  dialogVisible.value = true
}

const handleEdit = (row: any) => {
  dialogType.value = 'edit'
  Object.assign(form, {
    id: row.id,
    productCode: row.code,
    name: row.name,
    category: row.category,
    price: row.price,
    unit: row.unit,
    status: row.status === 'active' ? '在售' : '下架',
    description: row.description
  })
  dialogVisible.value = true
}

const handleDelete = async (row: any) => {
  try {
    await ElMessageBox.confirm('确定要删除该产品吗？', '提示', {
      type: 'warning'
    })
    
    await axios.delete(`/api/products/${row.id}`)
    ElMessage.success('删除成功')
    loadProducts()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
      console.error('Delete product error:', error)
    }
  }
}

const handleSubmit = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid) => {
    if (valid) {
      try {
        const data = {
          code: form.productCode,
          name: form.name,
          category: form.category,
          price: Number(form.price),
          unit: form.unit,
          status: form.status === '在售' ? 'active' : 'inactive',
          description: form.description
        }

        if (dialogType.value === 'add') {
          await axios.post('/api/products', data)
          ElMessage.success('创建成功')
        } else {
          await axios.put(`/api/products/${form.id}`, data)
          ElMessage.success('更新成功')
        }

        dialogVisible.value = false
        loadProducts()
      } catch (error) {
        ElMessage.error(dialogType.value === 'add' ? '创建失败' : '更新失败')
        console.error('Submit product error:', error)
      }
    }
  })
}

// 库存相关方法
const handleStock = (row: any) => {
  selectedProduct.value = row
  stockForm.type = 'in'
  stockForm.quantity = 1
  stockForm.remark = ''
  stockDialogVisible.value = true
}

const handleStockSubmit = async () => {
  if (!stockFormRef.value) return
  
  await stockFormRef.value.validate((valid) => {
    if (valid) {
      // TODO: 实现库存调整逻辑
      stockDialogVisible.value = false
    }
  })
}

// 初始加载
onMounted(() => {
  loadProducts()
})
</script>

<style scoped>
.products-container {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-left {
  display: flex;
  gap: 10px;
}

.pagination {
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