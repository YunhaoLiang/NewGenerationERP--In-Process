<template>
  <div class="dashboard-container">
    <!-- 数据概览卡片 -->
    <el-row :gutter="24">
      <el-col :span="6">
        <el-card shadow="hover" class="data-card">
          <template #header>
            <div class="card-header">
              <span>总销售额</span>
              <el-tag type="success">月</el-tag>
            </div>
          </template>
          <div class="card-content">
            <div class="amount">¥ 126,560</div>
            <div class="trend">
              <span>周同比</span>
              <span class="up">
                <el-icon><CaretTop /></el-icon>
                12%
              </span>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="data-card">
          <template #header>
            <div class="card-header">
              <span>订单数量</span>
              <el-tag type="warning">月</el-tag>
            </div>
          </template>
          <div class="card-content">
            <div class="amount">8,846</div>
            <div class="trend">
              <span>周同比</span>
              <span class="down">
                <el-icon><CaretBottom /></el-icon>
                2%
              </span>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="data-card">
          <template #header>
            <div class="card-header">
              <span>库存价值</span>
              <el-tag type="info">当前</el-tag>
            </div>
          </template>
          <div class="card-content">
            <div class="amount">¥ 1,234,567</div>
            <div class="trend">
              <span>库存周转率</span>
              <span class="up">
                <el-icon><CaretTop /></el-icon>
                8.5%
              </span>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="data-card">
          <template #header>
            <div class="card-header">
              <span>供应商数量</span>
              <el-tag type="danger">当前</el-tag>
            </div>
          </template>
          <div class="card-content">
            <div class="amount">128</div>
            <div class="trend">
              <span>活跃供应商</span>
              <span class="up">
                <el-icon><CaretTop /></el-icon>
                85%
              </span>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 图表区域 -->
    <el-row :gutter="24" class="chart-row">
      <el-col :span="16">
        <el-card shadow="hover">
          <template #header>
            <div class="card-header">
              <span>销售趋势</span>
              <el-radio-group v-model="salesTimeRange" size="small" @change="updateSalesChart">
                <el-radio-button label="week">周</el-radio-button>
                <el-radio-button label="month">月</el-radio-button>
                <el-radio-button label="year">年</el-radio-button>
              </el-radio-group>
            </div>
          </template>
          <div class="chart-container" ref="salesChartRef"></div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="hover">
          <template #header>
            <div class="card-header">
              <span>库存分布</span>
            </div>
          </template>
          <div class="chart-container" ref="inventoryChartRef"></div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 最近订单 -->
    <el-card shadow="hover" class="recent-orders">
      <template #header>
        <div class="card-header">
          <span>最近订单</span>
          <el-button type="primary" link>查看全部</el-button>
        </div>
      </template>
      <el-table :data="recentOrders" style="width: 100%">
        <el-table-column prop="orderNo" label="订单号" width="180" />
        <el-table-column prop="customer" label="客户" width="120" />
        <el-table-column prop="amount" label="金额" width="120" />
        <el-table-column prop="status" label="状态" width="120">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">
              {{ row.status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="createTime" label="创建时间" />
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import { CaretTop, CaretBottom } from '@element-plus/icons-vue'
import * as echarts from 'echarts'

const salesTimeRange = ref('month')
const salesChartRef = ref<HTMLElement | null>(null)
const inventoryChartRef = ref<HTMLElement | null>(null)
let salesChart: echarts.ECharts | null = null
let inventoryChart: echarts.ECharts | null = null

// 模拟数据
const mockSalesData = {
  week: {
    dates: ['周一', '周二', '周三', '周四', '周五', '周六', '周日', '下周一', '下周二', '下周三', '下周四', '下周五', '下周六', '下周日'],
    sales: [30, 40, 35, 50, 49, 60, 70],
    orders: [20, 30, 25, 40, 35, 45, 55],
    predictedSales: [null, null, null, null, null, null, null, 75, 78, 82, 85, 88, 90, 92],
    predictedOrders: [null, null, null, null, null, null, null, 60, 62, 65, 68, 70, 72, 75]
  },
  month: {
    dates: Array.from({ length: 37 }, (_, i) => `${i + 1}日`),
    sales: Array.from({ length: 30 }, () => Math.floor(Math.random() * 100) + 20),
    orders: Array.from({ length: 30 }, () => Math.floor(Math.random() * 80) + 10),
    predictedSales: [...Array(7).fill(null), ...Array(7).fill(0).map(() => Math.floor(Math.random() * 100) + 20)],
    predictedOrders: [...Array(7).fill(null), ...Array(7).fill(0).map(() => Math.floor(Math.random() * 80) + 10)]
  },
  year: {
    dates: ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月', '1月', '2月', '3月'],
    sales: Array.from({ length: 12 }, () => Math.floor(Math.random() * 1000) + 200),
    orders: Array.from({ length: 12 }, () => Math.floor(Math.random() * 800) + 100),
    predictedSales: [...Array(3).fill(null), ...Array(3).fill(0).map(() => Math.floor(Math.random() * 1000) + 200)],
    predictedOrders: [...Array(3).fill(null), ...Array(3).fill(0).map(() => Math.floor(Math.random() * 800) + 100)]
  }
}

const initSalesChart = () => {
  if (!salesChartRef.value) return
  
  salesChart = echarts.init(salesChartRef.value)
  updateSalesChart()
}

const updateSalesChart = () => {
  if (!salesChart) return

  const data = mockSalesData[salesTimeRange.value as keyof typeof mockSalesData]
  
  const option = {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      }
    },
    legend: {
      data: ['销售额', '订单量', '预测销售额', '预测订单量'],
      top: 10,
      right: 10
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: data.dates,
      axisLine: {
        lineStyle: {
          color: '#666'
        }
      },
      axisLabel: {
        color: '#666'
      }
    },
    yAxis: [
      {
        type: 'value',
        name: '销售额',
        axisLine: {
          show: true,
          lineStyle: {
            color: '#666'
          }
        },
        axisLabel: {
          color: '#666',
          formatter: '{value} 元'
        }
      },
      {
        type: 'value',
        name: '订单量',
        axisLine: {
          show: true,
          lineStyle: {
            color: '#666'
          }
        },
        axisLabel: {
          color: '#666',
          formatter: '{value} 单'
        }
      }
    ],
    series: [
      {
        name: '销售额',
        type: 'bar',
        data: data.sales,
        itemStyle: {
          color: '#1890ff'
        }
      },
      {
        name: '订单量',
        type: 'line',
        yAxisIndex: 1,
        data: data.orders,
        itemStyle: {
          color: '#52c41a'
        },
        lineStyle: {
          width: 2
        },
        symbol: 'circle',
        symbolSize: 8
      },
      {
        name: '预测销售额',
        type: 'line',
        data: data.predictedSales,
        itemStyle: {
          color: '#1890ff'
        },
        lineStyle: {
          type: 'dashed',
          width: 2
        },
        symbol: 'none'
      },
      {
        name: '预测订单量',
        type: 'line',
        yAxisIndex: 1,
        data: data.predictedOrders,
        itemStyle: {
          color: '#52c41a'
        },
        lineStyle: {
          type: 'dashed',
          width: 2
        },
        symbol: 'none'
      }
    ]
  }

  salesChart.setOption(option)
}

const initInventoryChart = () => {
  if (!inventoryChartRef.value) return
  
  inventoryChart = echarts.init(inventoryChartRef.value)
  
  const option = {
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'vertical',
      right: 10,
      top: 'center',
      textStyle: {
        color: '#666'
      }
    },
    series: [
      {
        name: '库存分布',
        type: 'pie',
        radius: ['40%', '70%'],
        center: ['40%', '50%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 10,
          borderColor: '#fff',
          borderWidth: 2
        },
        label: {
          show: false
        },
        emphasis: {
          label: {
            show: true,
            fontSize: '16',
            fontWeight: 'bold'
          }
        },
        labelLine: {
          show: false
        },
        data: [
          { value: 1048, name: '原材料', itemStyle: { color: '#1890ff' } },
          { value: 735, name: '在产品', itemStyle: { color: '#52c41a' } },
          { value: 580, name: '产成品', itemStyle: { color: '#faad14' } },
          { value: 484, name: '低值易耗品', itemStyle: { color: '#f5222d' } },
          { value: 300, name: '其他', itemStyle: { color: '#722ed1' } }
        ]
      }
    ]
  }

  inventoryChart.setOption(option)
}

const handleResize = () => {
  salesChart?.resize()
  inventoryChart?.resize()
}

onMounted(() => {
  initSalesChart()
  initInventoryChart()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  salesChart?.dispose()
  inventoryChart?.dispose()
})

const recentOrders = ref([
  {
    orderNo: 'ORD20240315001',
    customer: '张三',
    amount: '¥ 12,800',
    status: '已完成',
    createTime: '2024-03-15 10:30:00'
  },
  {
    orderNo: 'ORD20240315002',
    customer: '李四',
    amount: '¥ 8,500',
    status: '处理中',
    createTime: '2024-03-15 11:20:00'
  },
  {
    orderNo: 'ORD20240315003',
    customer: '王五',
    amount: '¥ 15,200',
    status: '待付款',
    createTime: '2024-03-15 14:15:00'
  }
])

const getStatusType = (status: string) => {
  const statusMap: Record<string, string> = {
    '已完成': 'success',
    '处理中': 'warning',
    '待付款': 'danger'
  }
  return statusMap[status] || 'info'
}
</script>

<style scoped>
.dashboard-container {
  padding: 24px;
  min-height: calc(100vh - 64px);
  background-color: #f0f2f5;
}

.data-card {
  margin-bottom: 24px;
  transition: all 0.3s;
}

.data-card:hover {
  transform: translateY(-2px);
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

.amount {
  font-size: 30px;
  font-weight: bold;
  margin: 16px 0;
  color: #262626;
}

.trend {
  font-size: 14px;
  color: #8c8c8c;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 8px;
}

.trend .up {
  color: #52c41a;
  display: flex;
  align-items: center;
}

.trend .down {
  color: #ff4d4f;
  display: flex;
  align-items: center;
}

.chart-row {
  margin-bottom: 24px;
}

.chart-container {
  height: 400px;
  width: 100%;
}

.recent-orders {
  margin-top: 24px;
}

:deep(.el-card) {
  border-radius: 4px;
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.03);
  border: 1px solid #f0f0f0;
}

:deep(.el-card:hover) {
  box-shadow: 0 3px 6px -4px rgba(0, 0, 0, 0.12), 0 6px 16px 0 rgba(0, 0, 0, 0.08), 0 9px 28px 8px rgba(0, 0, 0, 0.05);
}

:deep(.el-table) {
  margin: 16px 0;
}
</style>