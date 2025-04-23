<template>
  <div class="dashboard-charts">
    <el-row :gutter="20" class="chart-row">
      <el-col :span="16">
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <span class="title">销售趋势</span>
              <el-radio-group v-model="timeRange" size="small" @change="handleTimeRangeChange">
                <el-radio-button label="week">周</el-radio-button>
                <el-radio-button label="month">月</el-radio-button>
                <el-radio-button label="year">年</el-radio-button>
              </el-radio-group>
            </div>
          </template>
          <div ref="salesTrendChart" class="chart-container"></div>
        </el-card>
      </el-col>
      
      <el-col :span="8">
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <span class="title">品类占比</span>
            </div>
          </template>
          <div ref="categoryChart" class="chart-container"></div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { defineComponent, onMounted, ref } from 'vue'
import * as echarts from 'echarts'

export default defineComponent({
  name: 'DashboardCharts',
  setup() {
    const salesTrendChart = ref(null)
    const categoryChart = ref(null)
    const timeRange = ref('month')

    // 模拟不同时间范围的数据
    const mockData = {
      week: {
        labels: ['周一', '周二', '周三', '周四', '周五', '周六', '周日'],
        values: [68000, 92000, 85000, 78000, 110000, 120000, 105000]
      },
      month: {
        labels: ['1月', '2月', '3月', '4月', '5月', '6月'],
        values: [150000, 180000, 230000, 210000, 260000, 290000]
      },
      year: {
        labels: ['2023Q1', '2023Q2', '2023Q3', '2023Q4', '2024Q1'],
        values: [680000, 720000, 850000, 920000, 1050000]
      }
    }

    // 模拟品类分布数据
    const mockCategoryData = [
      { name: '笔记本电脑', value: 320000 },
      { name: '台式电脑', value: 250000 },
      { name: '打印机', value: 180000 },
      { name: '显示器', value: 150000 },
      { name: '网络设备', value: 120000 }
    ]

    const handleTimeRangeChange = (value) => {
      initSalesTrendChart(value)
    }

    const initSalesTrendChart = (range = 'month') => {
      const chart = echarts.init(salesTrendChart.value)
      const data = mockData[range]
      
      const option = {
        title: {
          text: '销售趋势分析',
          left: 'center',
          top: '20px',
          textStyle: {
            fontSize: 16,
            fontWeight: 'normal'
          }
        },
        tooltip: {
          trigger: 'axis',
          formatter: '{b}<br />销售额: ¥{c}元',
          axisPointer: {
            type: 'shadow'
          }
        },
        grid: {
          top: '15%',
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          boundaryGap: true,
          data: data.labels,
          axisLabel: {
            rotate: 30,
            fontSize: 12
          }
        },
        yAxis: {
          type: 'value',
          name: '销售额 (元)',
          axisLabel: {
            formatter: (value) => {
              return (value / 10000).toFixed(0) + 'w'
            },
            fontSize: 12
          },
          splitLine: {
            lineStyle: {
              type: 'dashed'
            }
          }
        },
        series: [{
          name: '销售额',
          type: 'bar',
          barWidth: '40%',
          data: data.values,
          itemStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
              offset: 0,
              color: '#83bff6'
            }, {
              offset: 0.5,
              color: '#188df0'
            }, {
              offset: 1,
              color: '#188df0'
            }])
          },
          emphasis: {
            itemStyle: {
              color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                offset: 0,
                color: '#2378f7'
              }, {
                offset: 0.7,
                color: '#2378f7'
              }, {
                offset: 1,
                color: '#83bff6'
              }])
            }
          }
        }]
      }
      chart.setOption(option)
    }

    const initCategoryChart = () => {
      const chart = echarts.init(categoryChart.value)
      const option = {
        title: {
          text: '品类销售占比',
          left: 'center',
          top: '20px',
          textStyle: {
            fontSize: 16,
            fontWeight: 'normal'
          }
        },
        tooltip: {
          trigger: 'item',
          formatter: '{b}: ¥{c}元 ({d}%)'
        },
        legend: {
          orient: 'vertical',
          right: '5%',
          top: 'middle',
          itemWidth: 10,
          itemHeight: 10,
          formatter: (name) => {
            const item = mockCategoryData.find(i => i.name === name)
            return name + ': ' + (item.value / 10000).toFixed(0) + 'w'
          }
        },
        series: [{
          name: '品类销售额',
          type: 'pie',
          radius: ['45%', '70%'],
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
              fontSize: '18',
              fontWeight: 'bold',
              formatter: '{b}\n¥{c}元'
            }
          },
          labelLine: {
            show: false
          },
          data: mockCategoryData.map(item => ({
            ...item,
            itemStyle: {
              color: ['#409EFF', '#67C23A', '#E6A23C', '#F56C6C', '#909399'][mockCategoryData.indexOf(item)]
            }
          }))
        }]
      }
      chart.setOption(option)
    }

    onMounted(() => {
      initSalesTrendChart()
      initCategoryChart()

      // 处理窗口大小变化
      window.addEventListener('resize', () => {
        const salesChart = echarts.getInstanceByDom(salesTrendChart.value)
        const catChart = echarts.getInstanceByDom(categoryChart.value)
        salesChart?.resize()
        catChart?.resize()
      })
    })

    return {
      salesTrendChart,
      categoryChart,
      timeRange,
      handleTimeRangeChange
    }
  }
})
</script>

<style scoped>
.dashboard-charts {
  padding: 20px;
  min-height: calc(100vh - 84px);
  background-color: #f0f2f5;
}

.chart-row {
  margin-bottom: 20px;
}

.chart-card {
  height: calc(100vh - 124px);
  box-shadow: 0 1px 4px rgba(0,21,41,.08);
}

.chart-container {
  height: calc(100% - 60px);
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.title {
  font-size: 16px;
  font-weight: 500;
  color: #1f2f3d;
}

:deep(.el-card__header) {
  padding: 15px 20px;
  border-bottom: 1px solid #ebeef5;
}

:deep(.el-radio-button__inner) {
  padding: 5px 15px;
}
</style> 