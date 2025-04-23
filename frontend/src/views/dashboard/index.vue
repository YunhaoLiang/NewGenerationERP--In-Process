<template>
  <div class="dashboard-container">
    <!-- 数据概览卡片 -->
    <el-row :gutter="20">
      <el-col :span="6" v-for="(item, index) in statisticsData" :key="index">
        <el-card class="statistics-card" :body-style="{ padding: '20px' }">
          <div class="statistics-content">
            <div class="icon-wrapper" :class="item.type">
              <el-icon><component :is="item.icon" /></el-icon>
            </div>
            <div class="statistics-info">
              <div class="label">{{ item.label }}</div>
              <div class="value">{{ item.value }}</div>
              <div class="trend" :class="{ 'up': item.trend > 0, 'down': item.trend < 0 }">
                <span>{{ item.trend > 0 ? '+' : '' }}{{ item.trend }}%</span>
                <span class="trend-text">较上月</span>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 图表区域 -->
    <el-row :gutter="20" class="chart-row">
      <el-col :span="16">
        <el-card class="chart-card">
          <div class="chart-header">
            <h3>销售趋势分析</h3>
            <el-radio-group v-model="timeRange" size="small">
              <el-radio-button label="week">本周</el-radio-button>
              <el-radio-button label="month">本月</el-radio-button>
              <el-radio-button label="year">全年</el-radio-button>
            </el-radio-group>
          </div>
          <div ref="salesChartRef" class="chart-container"></div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card class="chart-card">
          <div class="chart-header">
            <h3>库存分布</h3>
          </div>
          <div ref="stockChartRef" class="chart-container"></div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 最新订单和任务 -->
    <el-row :gutter="20" class="bottom-row">
      <el-col :span="14">
        <el-card class="table-card">
          <template #header>
            <div class="card-header">
              <span>最新订单</span>
              <el-button type="primary" link>查看全部</el-button>
            </div>
          </template>
          <el-table :data="latestOrders" style="width: 100%" size="large">
            <el-table-column prop="id" label="订单编号" width="180" />
            <el-table-column prop="customer" label="客户名称" width="120" />
            <el-table-column prop="amount" label="订单金额" width="120">
              <template #default="{ row }">
                <span class="amount">¥{{ row.amount }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="status" label="状态" width="100">
              <template #default="{ row }">
                <el-tag :type="row.statusType" size="small">{{ row.status }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="date" label="创建时间" />
          </el-table>
        </el-card>
      </el-col>
      <el-col :span="10">
        <el-card class="task-card">
          <template #header>
            <div class="card-header">
              <span>待办任务</span>
              <el-button type="primary" link>添加任务</el-button>
            </div>
          </template>
          <el-timeline>
            <el-timeline-item
              v-for="(task, index) in tasks"
              :key="index"
              :type="task.type"
              :timestamp="task.time"
            >
              {{ task.content }}
            </el-timeline-item>
          </el-timeline>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import * as echarts from 'echarts'
import {
  TrendCharts,
  Goods,
  Money,
  ShoppingCart
} from '@element-plus/icons-vue'

// 统计数据
const statisticsData = ref([
  {
    label: '总销售额',
    value: '¥ 126,560',
    trend: 12.5,
    icon: Money,
    type: 'success'
  },
  {
    label: '订单总量',
    value: '1,280',
    trend: -2.5,
    icon: ShoppingCart,
    type: 'warning'
  },
  {
    label: '商品总数',
    value: '3,680',
    trend: 8.2,
    icon: Goods,
    type: 'primary'
  },
  {
    label: '日活用户',
    value: '368',
    trend: 15.8,
    icon: TrendCharts,
    type: 'danger'
  }
])

// 时间范围选择
const timeRange = ref('month')

// 图表相关
const salesChartRef = ref<HTMLElement | null>(null)
const stockChartRef = ref<HTMLElement | null>(null)
let salesChart: echarts.ECharts | null = null
let stockChart: echarts.ECharts | null = null

// 初始化销售趋势图表
const initSalesChart = () => {
  if (!salesChartRef.value) return
  salesChart = echarts.init(salesChartRef.value)
  
  const option = {
    tooltip: {
      trigger: 'axis'
    },
    legend: {
      data: ['销售额', '订单量']
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
    },
    yAxis: {
      type: 'value'
    },
    series: [
      {
        name: '销售额',
        type: 'line',
        smooth: true,
        data: [820, 932, 901, 934, 1290, 1330, 1320],
        areaStyle: {
          opacity: 0.1
        },
        itemStyle: {
          color: '#409EFF'
        }
      },
      {
        name: '订单量',
        type: 'line',
        smooth: true,
        data: [320, 332, 301, 334, 390, 330, 320],
        areaStyle: {
          opacity: 0.1
        },
        itemStyle: {
          color: '#67C23A'
        }
      }
    ]
  }
  
  salesChart.setOption(option)
}

// 初始化库存分布图表
const initStockChart = () => {
  if (!stockChartRef.value) return
  stockChart = echarts.init(stockChartRef.value)
  
  const option = {
    tooltip: {
      trigger: 'item'
    },
    legend: {
      orient: 'vertical',
      left: 'left'
    },
    series: [
      {
        name: '库存分布',
        type: 'pie',
        radius: ['50%', '70%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 10,
          borderColor: '#fff',
          borderWidth: 2
        },
        label: {
          show: false,
          position: 'center'
        },
        emphasis: {
          label: {
            show: true,
            fontSize: '20',
            fontWeight: 'bold'
          }
        },
        labelLine: {
          show: false
        },
        data: [
          { value: 1048, name: '电子产品' },
          { value: 735, name: '服装' },
          { value: 580, name: '食品' },
          { value: 484, name: '家具' },
          { value: 300, name: '其他' }
        ]
      }
    ]
  }
  
  stockChart.setOption(option)
}

// 最新订单数据
const latestOrders = ref([
  {
    id: 'DD20240318001',
    customer: '张三',
    amount: '12,399.00',
    status: '已完成',
    statusType: 'success',
    date: '2024-03-18 10:00:00'
  },
  {
    id: 'DD20240318002',
    customer: '李四',
    amount: '5,999.00',
    status: '处理中',
    statusType: 'warning',
    date: '2024-03-18 09:30:00'
  },
  {
    id: 'DD20240318003',
    customer: '王五',
    amount: '3,999.00',
    status: '待付款',
    statusType: 'info',
    date: '2024-03-18 09:00:00'
  }
])

// 待办任务数据
const tasks = ref([
  {
    content: '新品上架审核',
    time: '09:00',
    type: 'primary'
  },
  {
    content: '供应商会议',
    time: '10:30',
    type: 'success'
  },
  {
    content: '库存盘点',
    time: '14:00',
    type: 'warning'
  },
  {
    content: '月度报告准备',
    time: '16:30',
    type: 'danger'
  }
])

// 监听窗口大小变化
const handleResize = () => {
  salesChart?.resize()
  stockChart?.resize()
}

onMounted(() => {
  initSalesChart()
  initStockChart()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  salesChart?.dispose()
  stockChart?.dispose()
})
</script>

<style scoped>
.dashboard-container {
  padding: 20px;
  background-color: #f5f7fa;
  min-height: 100vh;
}

.statistics-card {
  margin-bottom: 20px;
  border-radius: 8px;
  transition: all 0.3s;
}

.statistics-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.statistics-content {
  display: flex;
  align-items: center;
}

.icon-wrapper {
  width: 48px;
  height: 48px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 16px;
}

.icon-wrapper :deep(.el-icon) {
  font-size: 24px;
  color: #fff;
}

.icon-wrapper.success {
  background-color: #67C23A;
}

.icon-wrapper.warning {
  background-color: #E6A23C;
}

.icon-wrapper.primary {
  background-color: #409EFF;
}

.icon-wrapper.danger {
  background-color: #F56C6C;
}

.statistics-info {
  flex: 1;
}

.statistics-info .label {
  font-size: 14px;
  color: #606266;
  margin-bottom: 8px;
}

.statistics-info .value {
  font-size: 24px;
  font-weight: bold;
  color: #303133;
  margin-bottom: 8px;
}

.statistics-info .trend {
  font-size: 12px;
}

.trend.up {
  color: #67C23A;
}

.trend.down {
  color: #F56C6C;
}

.trend-text {
  color: #909399;
  margin-left: 4px;
}

.chart-row {
  margin-bottom: 20px;
}

.chart-card {
  height: 100%;
  border-radius: 8px;
}

.chart-header {
  padding: 16px 20px;
  border-bottom: 1px solid #EBEEF5;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chart-header h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 500;
}

.chart-container {
  height: 350px;
  padding: 20px;
}

.bottom-row {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.table-card :deep(.el-table) {
  margin: -10px 0;
}

.amount {
  font-family: monospace;
  color: #606266;
}

.task-card {
  height: 100%;
}

:deep(.el-timeline) {
  padding: 10px 20px;
}

:deep(.el-timeline-item__content) {
  font-size: 14px;
}

:deep(.el-timeline-item__timestamp) {
  font-size: 12px;
}
</style>