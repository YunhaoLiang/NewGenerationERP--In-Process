<template>
  <div class="dashboard-container">
    <!-- 顶部数据卡片 -->
    <el-row :gutter="20" class="data-cards">
      <el-col :span="6">
        <div class="data-card">
          <div class="card-header">
            <span class="label">总销售额</span>
            <span class="period">月</span>
          </div>
          <div class="card-value">¥ 126,560</div>
          <div class="card-trend">
            <span class="trend-value positive">↑12% 较上月</span>
          </div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="data-card">
          <div class="card-header">
            <span class="label">订单数</span>
            <span class="period">周</span>
          </div>
          <div class="card-value">1,234</div>
          <div class="card-trend">
            <span class="trend-value positive">↑8% 较上周</span>
          </div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="data-card">
          <div class="card-header">
            <span class="label">新增用户</span>
            <span class="period">日</span>
          </div>
          <div class="card-value">128</div>
          <div class="card-trend">
            <span class="trend-value negative">↓3% 较昨日</span>
          </div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="data-card">
          <div class="card-header">
            <span class="label">库存预警</span>
            <span class="period warning">实时</span>
          </div>
          <div class="card-value">12</div>
          <div class="card-trend">
            <span class="trend-label">待处理</span>
          </div>
        </div>
      </el-col>
    </el-row>

    <!-- 图表区域 -->
    <el-row :gutter="20" class="chart-section">
      <el-col :span="16">
        <div class="chart-card">
          <div class="chart-header">
            <div class="title">销售趋势</div>
            <div class="actions">
              <el-radio-group v-model="timeRange" size="small">
                <el-radio-button label="week">周</el-radio-button>
                <el-radio-button label="month">月</el-radio-button>
                <el-radio-button label="year">年</el-radio-button>
              </el-radio-group>
            </div>
          </div>
          <div ref="salesChart" class="chart-content"></div>
        </div>
      </el-col>
      <el-col :span="8">
        <div class="chart-card">
          <div class="chart-header">
            <div class="title">品类占比</div>
          </div>
          <div ref="categoryChart" class="chart-content"></div>
        </div>
      </el-col>
    </el-row>

    <!-- 最新订单 -->
    <div class="order-section">
      <div class="section-header">
        <span class="title">最新订单</span>
        <el-switch v-model="autoRefresh" active-text="自动刷新" />
      </div>
      <el-table :data="latestOrders" style="width: 100%">
        <el-table-column prop="orderNo" label="订单号" width="180" />
        <el-table-column prop="customer" label="客户" />
        <el-table-column prop="amount" label="金额">
          <template #default="scope">
            ¥{{ scope.row.amount.toLocaleString() }}
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态">
          <template #default="scope">
            <el-tag :type="scope.row.status === '已完成' ? 'success' : 'warning'">
              {{ scope.row.status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="createTime" label="下单时间" width="180" />
      </el-table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import * as echarts from 'echarts'

const timeRange = ref('month')
const autoRefresh = ref(true)
const salesChart = ref<HTMLElement | null>(null)
const categoryChart = ref<HTMLElement | null>(null)

// 模拟最新订单数据
const latestOrders = ref([
  {
    orderNo: 'DD20240301001',
    customer: '张三',
    amount: 3450,
    status: '已完成',
    createTime: '2024-03-01 14:23'
  },
  // 可以添加更多订单数据
])

// 初始化销售趋势图
const initSalesChart = () => {
  if (!salesChart.value) return
  const chart = echarts.init(salesChart.value)
  const option = {
    grid: {
      top: '10%',
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      }
    },
    xAxis: {
      type: 'category',
      data: ['周一', '周二', '周三', '周四', '周五', '周六', '周日'],
      axisLine: {
        lineStyle: {
          color: '#E5E9F2'
        }
      }
    },
    yAxis: {
      type: 'value',
      splitLine: {
        lineStyle: {
          type: 'dashed',
          color: '#E5E9F2'
        }
      }
    },
    series: [{
      data: [820, 932, 901, 934, 1290, 1330, 1320],
      type: 'line',
      smooth: true,
      symbolSize: 8,
      lineStyle: {
        width: 3,
        color: '#409EFF'
      },
      areaStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
          offset: 0,
          color: 'rgba(64,158,255,0.3)'
        }, {
          offset: 1,
          color: 'rgba(64,158,255,0.1)'
        }])
      }
    }]
  }
  chart.setOption(option)
}

// 初始化品类占比图
const initCategoryChart = () => {
  if (!categoryChart.value) return
  const chart = echarts.init(categoryChart.value)
  const option = {
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'vertical',
      right: 10,
      top: 'center'
    },
    series: [{
      type: 'pie',
      radius: ['50%', '70%'],
      avoidLabelOverlap: false,
      label: {
        show: false
      },
      emphasis: {
        label: {
          show: true,
          fontSize: '14',
          fontWeight: 'bold'
        }
      },
      data: [
        { value: 335, name: '笔记本' },
        { value: 310, name: '台式机' },
        { value: 234, name: '显示器' },
        { value: 135, name: '配件' },
        { value: 1548, name: '其他' }
      ]
    }]
  }
  chart.setOption(option)
}

// 处理窗口大小变化
const handleResize = () => {
  const salesChartInstance = echarts.getInstanceByDom(salesChart.value!)
  const categoryChartInstance = echarts.getInstanceByDom(categoryChart.value!)
  salesChartInstance?.resize()
  categoryChartInstance?.resize()
}

onMounted(() => {
  initSalesChart()
  initCategoryChart()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
})
</script>

<style scoped>
.dashboard-container {
  padding: 20px;
  background-color: #f5f7fa;
}

.data-cards {
  margin-bottom: 20px;
}

.data-card {
  background: #fff;
  border-radius: 4px;
  padding: 20px;
  box-shadow: 0 1px 4px rgba(0,21,41,.08);
}

.card-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
}

.label {
  color: #606266;
  font-size: 14px;
}

.period {
  font-size: 12px;
  padding: 2px 6px;
  background: #f0f2f5;
  border-radius: 2px;
}

.period.warning {
  color: #f56c6c;
  background: #fef0f0;
}

.card-value {
  font-size: 24px;
  font-weight: bold;
  color: #303133;
  margin: 8px 0;
}

.card-trend {
  font-size: 13px;
}

.trend-value {
  color: #606266;
}

.trend-value.positive {
  color: #67c23a;
}

.trend-value.negative {
  color: #f56c6c;
}

.chart-section {
  margin-bottom: 20px;
}

.chart-card {
  background: #fff;
  border-radius: 4px;
  padding: 20px;
  box-shadow: 0 1px 4px rgba(0,21,41,.08);
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.chart-header .title {
  font-size: 16px;
  font-weight: 500;
  color: #303133;
}

.chart-content {
  height: 350px;
}

.order-section {
  background: #fff;
  border-radius: 4px;
  padding: 20px;
  box-shadow: 0 1px 4px rgba(0,21,41,.08);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.section-header .title {
  font-size: 16px;
  font-weight: 500;
  color: #303133;
}

:deep(.el-table) {
  --el-table-border-color: #ebeef5;
  --el-table-header-bg-color: #f5f7fa;
}
</style> 