<template>
  <div class="dashboard-container">
    <el-row :gutter="20">
      <el-col :span="6">
        <el-card class="data-card">
          <template #header>
            <div class="card-header">
              <span>总销售额</span>
              <el-tag type="success">月</el-tag>
            </div>
          </template>
          <div class="card-content">
            <div class="main-value">¥ 126,560</div>
            <div class="sub-value">
              <span class="trend up">
                <el-icon><ArrowUp /></el-icon>
                12%
              </span>
              较上月
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card class="data-card">
          <template #header>
            <div class="card-header">
              <span>订单数</span>
              <el-tag type="warning">周</el-tag>
            </div>
          </template>
          <div class="card-content">
            <div class="main-value">1,234</div>
            <div class="sub-value">
              <span class="trend up">
                <el-icon><ArrowUp /></el-icon>
                8%
              </span>
              较上周
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card class="data-card">
          <template #header>
            <div class="card-header">
              <span>新增用户</span>
              <el-tag type="info">日</el-tag>
            </div>
          </template>
          <div class="card-content">
            <div class="main-value">128</div>
            <div class="sub-value">
              <span class="trend down">
                <el-icon><ArrowDown /></el-icon>
                3%
              </span>
              较昨日
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card class="data-card">
          <template #header>
            <div class="card-header">
              <span>库存预警</span>
              <el-tag type="danger">实时</el-tag>
            </div>
          </template>
          <div class="card-content">
            <div class="main-value">12</div>
            <div class="sub-value">
              <span>待处理</span>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="chart-row">
      <el-col :span="16">
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <span>销售趋势</span>
              <el-radio-group v-model="timeRange" size="small">
                <el-radio-button label="week">周</el-radio-button>
                <el-radio-button label="month">月</el-radio-button>
                <el-radio-button label="year">年</el-radio-button>
              </el-radio-group>
            </div>
          </template>
          <div class="chart-placeholder">
            图表区域
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="8">
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <span>品类占比</span>
            </div>
          </template>
          <div class="chart-placeholder">
            饼图区域
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="table-row">
      <el-col :span="24">
        <el-card class="table-card">
          <template #header>
            <div class="card-header">
              <span>最新订单</span>
              <el-button type="primary" link>查看更多</el-button>
            </div>
          </template>
          <el-table :data="latestOrders" style="width: 100%">
            <el-table-column prop="id" label="订单号" width="180" />
            <el-table-column prop="customer" label="客户" width="180" />
            <el-table-column prop="amount" label="金额" width="180" />
            <el-table-column prop="status" label="状态">
              <template #default="{ row }">
                <el-tag :type="row.statusType">{{ row.status }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="date" label="下单时间" />
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ArrowUp, ArrowDown } from '@element-plus/icons-vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const timeRange = ref('month')

const latestOrders = [
  {
    id: 'DD20240301001',
    customer: '张三',
    amount: '¥3,450',
    status: '已完成',
    statusType: 'success',
    date: '2024-03-01 14:23'
  },
  {
    id: 'DD20240301002',
    customer: '李四',
    amount: '¥2,180',
    status: '处理中',
    statusType: 'warning',
    date: '2024-03-01 15:45'
  },
  {
    id: 'DD20240301003',
    customer: '王五',
    amount: '¥5,920',
    status: '待支付',
    statusType: 'info',
    date: '2024-03-01 16:30'
  }
]
</script>

<style scoped>
.dashboard-container {
  padding: 20px;
}

.data-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-content {
  text-align: center;
  padding: 20px 0;
}

.main-value {
  font-size: 28px;
  font-weight: bold;
  color: var(--primary-text);
  margin-bottom: 10px;
}

.sub-value {
  font-size: 14px;
  color: #666;
}

.trend {
  display: inline-flex;
  align-items: center;
  margin-right: 8px;
}

.trend.up {
  color: #67c23a;
}

.trend.down {
  color: #f56c6c;
}

.chart-row {
  margin-bottom: 20px;
}

.chart-card {
  height: 400px;
}

.chart-placeholder {
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  color: #999;
  font-size: 14px;
  background: #f5f7fa;
  border-radius: 4px;
}

.table-row {
  margin-bottom: 20px;
}

:deep(.el-card__header) {
  padding: 15px 20px;
  border-bottom: 1px solid var(--border-color);
}
</style> 