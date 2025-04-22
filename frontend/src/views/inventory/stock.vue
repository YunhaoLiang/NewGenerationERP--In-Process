<template>
  <div class="stock-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>库存管理</span>
          <div class="header-buttons">
            <el-button type="primary" @click="handleIn">入库</el-button>
            <el-button type="success" @click="handleOut">出库</el-button>
          </div>
        </div>
      </template>

      <!-- 搜索栏 -->
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="产品名称">
          <el-input v-model="searchForm.name" placeholder="请输入产品名称" clearable />
        </el-form-item>
        <el-form-item label="仓库">
          <el-select v-model="searchForm.warehouse" placeholder="请选择" clearable>
            <el-option label="主仓库" value="main" />
            <el-option label="分仓库" value="branch" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="resetSearch">重置</el-button>
        </el-form-item>
      </el-form>
      
      <el-table :data="stockList" style="width: 100%">
        <el-table-column prop="productNo" label="产品编号" width="180" />
        <el-table-column prop="name" label="产品名称" />
        <el-table-column prop="warehouse" label="仓库" width="120">
          <template #default="{ row }">
            <el-tag :type="row.warehouse === 'main' ? 'success' : 'warning'">
              {{ row.warehouse === 'main' ? '主仓库' : '分仓库' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="quantity" label="数量" width="120" />
        <el-table-column prop="unit" label="单位" width="80" />
        <el-table-column prop="updateTime" label="更新时间" width="180" />
        <el-table-column label="操作" width="200">
          <template #default="{ row }">
            <el-button type="primary" link @click="handleAdjust(row)">调整库存</el-button>
            <el-button type="info" link @click="handleHistory(row)">查看记录</el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          :total="total"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>

    <!-- 入库对话框 -->
    <el-dialog
      v-model="inDialogVisible"
      title="产品入库"
      width="500px"
    >
      <el-form
        ref="inFormRef"
        :model="inForm"
        :rules="inRules"
        label-width="100px"
      >
        <el-form-item label="产品" prop="product">
          <el-select v-model="inForm.product" style="width: 100%">
            <el-option
              v-for="item in products"
              :key="item.productNo"
              :label="item.name"
              :value="item.productNo"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="仓库" prop="warehouse">
          <el-select v-model="inForm.warehouse" style="width: 100%">
            <el-option label="主仓库" value="main" />
            <el-option label="分仓库" value="branch" />
          </el-select>
        </el-form-item>
        <el-form-item label="数量" prop="quantity">
          <el-input-number v-model="inForm.quantity" :min="1" style="width: 100%" />
        </el-form-item>
        <el-form-item label="备注" prop="remark">
          <el-input v-model="inForm.remark" type="textarea" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="inDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleInSubmit">确定</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 出库对话框 -->
    <el-dialog
      v-model="outDialogVisible"
      title="产品出库"
      width="500px"
    >
      <el-form
        ref="outFormRef"
        :model="outForm"
        :rules="outRules"
        label-width="100px"
      >
        <el-form-item label="产品" prop="product">
          <el-select v-model="outForm.product" style="width: 100%">
            <el-option
              v-for="item in products"
              :key="item.productNo"
              :label="item.name"
              :value="item.productNo"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="仓库" prop="warehouse">
          <el-select v-model="outForm.warehouse" style="width: 100%">
            <el-option label="主仓库" value="main" />
            <el-option label="分仓库" value="branch" />
          </el-select>
        </el-form-item>
        <el-form-item label="数量" prop="quantity">
          <el-input-number v-model="outForm.quantity" :min="1" style="width: 100%" />
        </el-form-item>
        <el-form-item label="备注" prop="remark">
          <el-input v-model="outForm.remark" type="textarea" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="outDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleOutSubmit">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import type { FormInstance } from 'element-plus'

const stockList = ref([
  {
    productNo: 'P001',
    name: 'ThinkPad X1 Carbon',
    warehouse: 'main',
    quantity: 100,
    unit: '台',
    updateTime: '2024-03-15 10:00:00'
  },
  {
    productNo: 'P002',
    name: 'iPhone 15 Pro',
    warehouse: 'branch',
    quantity: 200,
    unit: '台',
    updateTime: '2024-03-15 11:00:00'
  }
])

const products = ref([
  {
    productNo: 'P001',
    name: 'ThinkPad X1 Carbon'
  },
  {
    productNo: 'P002',
    name: 'iPhone 15 Pro'
  }
])

const searchForm = reactive({
  name: '',
  warehouse: ''
})

const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(100)

const inDialogVisible = ref(false)
const outDialogVisible = ref(false)
const inFormRef = ref<FormInstance>()
const outFormRef = ref<FormInstance>()

const inForm = reactive({
  product: '',
  warehouse: '',
  quantity: 1,
  remark: ''
})

const outForm = reactive({
  product: '',
  warehouse: '',
  quantity: 1,
  remark: ''
})

const inRules = {
  product: [
    { required: true, message: '请选择产品', trigger: 'change' }
  ],
  warehouse: [
    { required: true, message: '请选择仓库', trigger: 'change' }
  ],
  quantity: [
    { required: true, message: '请输入数量', trigger: 'blur' }
  ]
}

const outRules = {
  product: [
    { required: true, message: '请选择产品', trigger: 'change' }
  ],
  warehouse: [
    { required: true, message: '请选择仓库', trigger: 'change' }
  ],
  quantity: [
    { required: true, message: '请输入数量', trigger: 'blur' }
  ]
}

const handleSearch = () => {
  // TODO: 实现搜索逻辑
  console.log('搜索条件：', searchForm)
}

const resetSearch = () => {
  searchForm.name = ''
  searchForm.warehouse = ''
}

const handleSizeChange = (val: number) => {
  pageSize.value = val
  // TODO: 重新加载数据
}

const handleCurrentChange = (val: number) => {
  currentPage.value = val
  // TODO: 重新加载数据
}

const handleIn = () => {
  inDialogVisible.value = true
  inForm.product = ''
  inForm.warehouse = ''
  inForm.quantity = 1
  inForm.remark = ''
}

const handleOut = () => {
  outDialogVisible.value = true
  outForm.product = ''
  outForm.warehouse = ''
  outForm.quantity = 1
  outForm.remark = ''
}

const handleAdjust = (row: any) => {
  ElMessage.info('调整库存功能待实现')
}

const handleHistory = (row: any) => {
  ElMessage.info('查看记录功能待实现')
}

const handleInSubmit = async () => {
  if (!inFormRef.value) return
  
  await inFormRef.value.validate((valid) => {
    if (valid) {
      ElMessage.success('入库成功')
      inDialogVisible.value = false
    }
  })
}

const handleOutSubmit = async () => {
  if (!outFormRef.value) return
  
  await outFormRef.value.validate((valid) => {
    if (valid) {
      ElMessage.success('出库成功')
      outDialogVisible.value = false
    }
  })
}
</script>

<style scoped>
.stock-container {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-buttons {
  display: flex;
  gap: 10px;
}

.search-form {
  margin-bottom: 20px;
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