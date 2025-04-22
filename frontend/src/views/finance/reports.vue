<template>
  <div class="reports-container">
    <!-- 报表类型选择 -->
    <el-card class="filter-card">
      <el-form :inline="true" :model="filterForm">
        <el-form-item label="报表类型">
          <el-select v-model="filterForm.reportType">
            <el-option label="资产负债表" value="balance" />
            <el-option label="利润表" value="income" />
            <el-option label="现金流量表" value="cashflow" />
          </el-select>
        </el-form-item>
        <el-form-item label="日期范围">
          <el-date-picker
            v-model="filterForm.dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            value-format="YYYY-MM-DD"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleGenerate">生成报表</el-button>
          <el-button type="success" @click="handleExport">导出报表</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 资产负债表 -->
    <el-card v-if="filterForm.reportType === 'balance'" class="report-card">
      <template #header>
        <div class="card-header">
          <span>资产负债表</span>
          <span>{{ formatDateRange }}</span>
        </div>
      </template>
      
      <el-row :gutter="20">
        <el-col :span="12">
          <h3>资产</h3>
          <el-table :data="balanceSheet.assets" :show-header="false">
            <el-table-column prop="name" label="项目" />
            <el-table-column prop="amount" label="金额" align="right" />
          </el-table>
          <div class="total-row">
            <span>资产总计</span>
            <span>{{ balanceSheet.totalAssets }}</span>
          </div>
        </el-col>
        <el-col :span="12">
          <h3>负债和所有者权益</h3>
          <el-table :data="balanceSheet.liabilities" :show-header="false">
            <el-table-column prop="name" label="项目" />
            <el-table-column prop="amount" label="金额" align="right" />
          </el-table>
          <div class="total-row">
            <span>负债和所有者权益总计</span>
            <span>{{ balanceSheet.totalLiabilities }}</span>
          </div>
        </el-col>
      </el-row>
    </el-card>

    <!-- 利润表 -->
    <el-card v-if="filterForm.reportType === 'income'" class="report-card">
      <template #header>
        <div class="card-header">
          <span>利润表</span>
          <span>{{ formatDateRange }}</span>
        </div>
      </template>
      
      <el-table :data="incomeStatement" :show-header="false">
        <el-table-column prop="name" label="项目" />
        <el-table-column prop="amount" label="金额" align="right" />
      </el-table>
      <div class="total-row">
        <span>净利润</span>
        <span>{{ incomeStatement[incomeStatement.length - 1].amount }}</span>
      </div>
    </el-card>

    <!-- 现金流量表 -->
    <el-card v-if="filterForm.reportType === 'cashflow'" class="report-card">
      <template #header>
        <div class="card-header">
          <span>现金流量表</span>
          <span>{{ formatDateRange }}</span>
        </div>
      </template>
      
      <el-table :data="cashflowStatement" :show-header="false">
        <el-table-column prop="name" label="项目" />
        <el-table-column prop="amount" label="金额" align="right" />
      </el-table>
      <div class="total-row">
        <span>现金及现金等价物净增加额</span>
        <span>{{ cashflowStatement[cashflowStatement.length - 1].amount }}</span>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue'

const filterForm = reactive({
  reportType: 'balance',
  dateRange: []
})

const formatDateRange = computed(() => {
  if (!filterForm.dateRange || filterForm.dateRange.length !== 2) return ''
  return `${filterForm.dateRange[0]} 至 ${filterForm.dateRange[1]}`
})

// 示例数据
const balanceSheet = reactive({
  assets: [
    { name: '流动资产', amount: '1,234,567.89' },
    { name: '固定资产', amount: '2,345,678.90' },
    { name: '无形资产', amount: '345,678.90' }
  ],
  totalAssets: '3,925,925.69',
  liabilities: [
    { name: '流动负债', amount: '987,654.32' },
    { name: '非流动负债', amount: '1,234,567.89' },
    { name: '所有者权益', amount: '1,703,703.48' }
  ],
  totalLiabilities: '3,925,925.69'
})

const incomeStatement = ref([
  { name: '营业收入', amount: '2,345,678.90' },
  { name: '营业成本', amount: '1,234,567.89' },
  { name: '营业利润', amount: '1,111,111.01' },
  { name: '利润总额', amount: '1,000,000.00' },
  { name: '净利润', amount: '800,000.00' }
])

const cashflowStatement = ref([
  { name: '经营活动现金流量净额', amount: '500,000.00' },
  { name: '投资活动现金流量净额', amount: '-300,000.00' },
  { name: '筹资活动现金流量净额', amount: '200,000.00' },
  { name: '现金及现金等价物净增加额', amount: '400,000.00' }
])

const handleGenerate = () => {
  // TODO: 实现报表生成逻辑
}

const handleExport = () => {
  // TODO: 实现报表导出逻辑
}
</script>

<style scoped>
.reports-container {
  padding: 20px;
}

.filter-card {
  margin-bottom: 20px;
}

.report-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

h3 {
  margin: 0 0 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid #ebeef5;
}

.total-row {
  display: flex;
  justify-content: space-between;
  padding: 10px;
  font-weight: bold;
  border-top: 1px solid #ebeef5;
  margin-top: 10px;
}
</style> 