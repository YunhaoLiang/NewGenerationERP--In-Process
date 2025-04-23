<template>
  <div class="products-container">
    <div class="header-actions">
      <el-button type="primary" @click="handleAdd">
        <el-icon><Plus /></el-icon>添加产品
      </el-button>
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
    </div>

    <el-table
      v-loading="loading"
      :data="products"
      border
      style="width: 100%"
    >
      <el-table-column prop="product_id" label="ID" width="80" />
      <el-table-column prop="name" label="产品名称" />
      <el-table-column prop="price" label="单价">
        <template #default="{ row }">
          ¥{{ formatPrice(row.price) }}
        </template>
      </el-table-column>
      <el-table-column prop="stock" label="库存" width="100" />
      <el-table-column prop="category" label="类别" />
      <el-table-column prop="description" label="描述" show-overflow-tooltip />
      <el-table-column prop="updated_at" label="更新时间" width="180">
        <template #default="{ row }">
          {{ formatDate(row.updated_at) }}
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

    <!-- 产品表单对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑产品' : '添加产品'"
      width="500px"
    >
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="100px"
      >
        <el-form-item label="产品名称" prop="name">
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="单价" prop="price">
          <el-input-number
            v-model="form.price"
            :precision="2"
            :step="0.1"
            :min="0"
          />
        </el-form-item>
        <el-form-item label="库存" prop="stock">
          <el-input-number
            v-model="form.stock"
            :min="0"
          />
        </el-form-item>
        <el-form-item label="类别" prop="category">
          <el-input v-model="form.category" />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input
            v-model="form.description"
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
import { ref, onMounted } from 'vue';
import { ElMessage, ElMessageBox, type FormInstance } from 'element-plus';
import { Plus, Search } from '@element-plus/icons-vue';
import type { Product } from '@/types/models';
import * as productApi from '@/api/modules/products';

// 状态
const loading = ref(false);
const products = ref<Product[]>([]);
const searchQuery = ref('');
const dialogVisible = ref(false);
const isEdit = ref(false);
const formRef = ref<FormInstance>();

interface ProductForm {
  product_id?: number;
  name: string;
  price: number;
  stock: number;
  category: string;
  description: string;
}

// 表单数据
const form = ref<ProductForm>({
  name: '',
  price: 0,
  stock: 0,
  category: '',
  description: '',
});

// 表单验证规则
const rules = {
  name: [
    { required: true, message: '请输入产品名称', trigger: 'blur' },
    { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' },
  ],
  price: [
    { required: true, message: '请输入单价', trigger: 'blur' },
  ],
  stock: [
    { required: true, message: '请输入库存数量', trigger: 'blur' },
  ],
  category: [
    { required: true, message: '请输入类别', trigger: 'blur' },
  ],
};

// 格式化价格
const formatPrice = (price: number) => {
  return price.toFixed(2);
};

// 格式化日期
const formatDate = (date: string) => {
  return new Date(date).toLocaleString();
};

// 获取产品列表
const fetchProducts = async () => {
  try {
    loading.value = true;
    const response = await productApi.getProducts({ page: 1, limit: 10 });
    products.value = response.data.items;
  } catch (error) {
    ElMessage.error('获取产品列表失败');
  } finally {
    loading.value = false;
  }
};

// 搜索处理
const handleSearch = () => {
  // 实现搜索逻辑
  console.log('搜索:', searchQuery.value);
};

// 添加产品
const handleAdd = () => {
  isEdit.value = false;
  form.value = {
    name: '',
    price: 0,
    stock: 0,
    category: '',
    description: '',
  };
  dialogVisible.value = true;
};

// 编辑产品
const handleEdit = (row: Product) => {
  isEdit.value = true;
  form.value = {
    product_id: row.product_id,
    name: row.name,
    price: row.price,
    stock: row.stock,
    category: row.category,
    description: row.description,
  };
  dialogVisible.value = true;
};

// 删除产品
const handleDelete = async (row: Product) => {
  try {
    await ElMessageBox.confirm(
      '确定要删除该产品吗？此操作不可恢复',
      '警告',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
    );
    
    await productApi.deleteProduct(row.product_id);
    ElMessage.success('删除成功');
    await fetchProducts();
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败');
    }
  }
};

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return;
  
  try {
    await formRef.value.validate();
    
    if (isEdit.value && form.value.product_id) {
      await productApi.updateProduct(form.value.product_id, form.value);
      ElMessage.success('更新成功');
    } else {
      await productApi.createProduct(form.value);
      ElMessage.success('添加成功');
    }
    
    dialogVisible.value = false;
    await fetchProducts();
  } catch (error) {
    ElMessage.error('操作失败');
  }
};

// 初始化
onMounted(() => {
  fetchProducts();
});
</script>

<style scoped>
.products-container {
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