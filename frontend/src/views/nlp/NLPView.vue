<template>
  <div class="nlp-container">
    <el-card class="main-card">
      <template #header>
        <div class="card-header">
          <h2>智能数据库操作</h2>
          <el-tag type="success">AI 驱动</el-tag>
        </div>
      </template>

      <div class="content-area">
        <!-- 左侧区域：输入框和历史记录 -->
        <div class="left-section">
          <!-- 输入区域 -->
          <div class="input-section">
            <el-input
              v-model="userInput"
              type="textarea"
              :rows="6"
              placeholder="请输入您的指令，例如：
- 客户A订购500台高性能电脑，配置为Intel i9处理器，32GB内存，2TB硬盘，RTX4090显卡，交付日期2024-06-30
- 查询所有订单状态
- 生成本月销售报表"
            />
            <div class="button-group">
              <el-button type="primary" :loading="loading" @click="processCommand">
                执行操作
              </el-button>
              <el-button link @click="clearInput">清除</el-button>
            </div>
          </div>

          <!-- 历史记录 -->
          <div class="history-section">
            <div class="history-header">
              <h3>历史记录</h3>
              <el-button link type="primary" @click="clearHistory">
                <el-icon><Delete /></el-icon>
                清空
              </el-button>
            </div>
            <div class="history-list">
              <el-timeline>
                <el-timeline-item
                  v-for="(item, index) in historyList"
                  :key="index"
                  :type="item.status === 'success' ? 'success' : 'danger'"
                  :timestamp="item.timestamp"
                >
                  <el-card class="history-item" @click="loadHistoryItem(item)">
                    <p class="history-text">{{ item.text }}</p>
                    <el-tag size="small" :type="item.status === 'success' ? 'success' : 'danger'">
                      {{ item.status === 'success' ? '成功' : '失败' }}
                    </el-tag>
                  </el-card>
                </el-timeline-item>
              </el-timeline>
            </div>
          </div>
        </div>

        <!-- 右侧结果显示区域 -->
        <div class="result-section">
          <h3>执行结果</h3>
          <div v-if="loading" class="loading-area">
            <el-progress type="circle" :percentage="percentage" />
            <p>正在处理中...</p>
          </div>
          <div v-else-if="result" class="result-area">
            <!-- 状态提示 -->
            <el-alert
              :title="result.status === 'success' ? '处理成功' : '处理失败'"
              :type="result.status === 'success' ? 'success' : 'error'"
              :description="result.message"
              show-icon
            />
            
            <div v-if="result.status === 'success'" class="result-details">
              <!-- 基本信息 -->
              <el-card class="info-card">
                <template #header>
                  <div class="card-header">
                    <h4>基本信息</h4>
                  </div>
                </template>
                <el-descriptions :column="1" border>
                  <el-descriptions-item label="请求类型" class="description-item">
                    <div class="scrollable-content">
                      {{ result.result.type }}
                    </div>
                  </el-descriptions-item>
                  <el-descriptions-item label="处理结果" class="description-item">
                    <div class="scrollable-content">
                      {{ result.result.content }}
                    </div>
                  </el-descriptions-item>
                </el-descriptions>
              </el-card>

              <!-- Agents处理过程 -->
              <div v-if="result.result.details?.agents_process" class="agents-process">
                <el-card v-for="(agent, agentName) in result.result.details.agents_process" 
                       :key="agentName" 
                       class="agent-card">
                  <template #header>
                    <div class="agent-header">
                      <el-icon><Connection /></el-icon>
                      <span>{{ formatAgentName(agentName) }}</span>
                      <el-tag size="small" type="success">已完成</el-tag>
                    </div>
                  </template>
                  <div class="agent-content">
                    <div class="agent-action">
                      <strong>执行动作：</strong>{{ agent.action }}
                    </div>
                    <div class="agent-details">
                      <el-collapse>
                        <el-collapse-item>
                          <template #title>
                            <div class="collapse-title">
                              <el-icon><Document /></el-icon>
                              <span>查看处理结果</span>
                            </div>
                          </template>
                          
                          <!-- Order Agent 结果展示 -->
                          <template v-if="agentName.toString() === 'order_agent'">
                            <el-descriptions :column="2" border>
                              <el-descriptions-item label="订单编号" :span="2">
                                {{ agent.details.order_no }}
                              </el-descriptions-item>
                              <el-descriptions-item label="客户" :span="2">
                                {{ agent.details.customer }}
                              </el-descriptions-item>
                              <el-descriptions-item label="订购数量">
                                {{ agent.details.quantity }}台
                              </el-descriptions-item>
                              <el-descriptions-item label="交付日期">
                                {{ agent.details.delivery_date }}
                              </el-descriptions-item>
                            </el-descriptions>
                          </template>

                          <!-- Planning Agent 结果展示 -->
                          <template v-if="agentName.toString() === 'planning_agent'">
                            <el-timeline>
                              <el-timeline-item
                                v-for="phase in agent.details.production_phases"
                                :key="phase.phase"
                                :type="phase.phase === '组装' ? 'primary' : 'success'"
                                :timestamp="`${phase.start_date} 至 ${phase.end_date}`"
                              >
                                <h4>{{ phase.phase }}阶段</h4>
                                <p>计划生产数量：{{ phase.quantity }}台</p>
                              </el-timeline-item>
                            </el-timeline>
                          </template>

                          <!-- Supply Chain Agent 结果展示 -->
                          <template v-if="agentName.toString() === 'supply_chain_agent'">
                            <el-table :data="agent.details.required_components" border stripe>
                              <el-table-column prop="item" label="组件名称" />
                              <el-table-column prop="quantity" label="数量">
                                <template #default="scope">
                                  {{ scope.row.quantity }}个
                                </template>
                              </el-table-column>
                              <el-table-column prop="estimated_cost" label="预计单价">
                                <template #default="scope">
                                  ¥{{ scope.row.estimated_cost.toLocaleString() }}
                                </template>
                              </el-table-column>
                              <el-table-column label="总价">
                                <template #default="scope">
                                  ¥{{ (scope.row.quantity * scope.row.estimated_cost).toLocaleString() }}
                                </template>
                              </el-table-column>
                            </el-table>
                          </template>

                          <!-- Finance Agent 结果展示 -->
                          <template v-if="agentName.toString() === 'finance_agent'">
                            <div class="finance-summary">
                              <el-row :gutter="20">
                                <el-col :span="12">
                                  <el-card shadow="hover">
                                    <template #header>
                                      <div class="card-header">
                                        <h5>成本构成</h5>
                                      </div>
                                    </template>
                                    <el-descriptions direction="vertical" :column="1" border>
                                      <el-descriptions-item label="材料成本">
                                        ¥{{ agent.details.cost_estimation.materials.toLocaleString() }}
                                      </el-descriptions-item>
                                      <el-descriptions-item label="人工成本">
                                        ¥{{ agent.details.cost_estimation.labor.toLocaleString() }}
                                      </el-descriptions-item>
                                      <el-descriptions-item label="管理费用">
                                        ¥{{ agent.details.cost_estimation.overhead.toLocaleString() }}
                                      </el-descriptions-item>
                                    </el-descriptions>
                                  </el-card>
                                </el-col>
                                <el-col :span="12">
                                  <el-card shadow="hover">
                                    <template #header>
                                      <div class="card-header">
                                        <h5>财务概要</h5>
                                      </div>
                                    </template>
                                    <el-descriptions direction="vertical" :column="1" border>
                                      <el-descriptions-item label="总成本">
                                        ¥{{ agent.details.total_cost.toLocaleString() }}
                                      </el-descriptions-item>
                                      <el-descriptions-item label="建议售价">
                                        ¥{{ agent.details.suggested_price.toLocaleString() }}
                                      </el-descriptions-item>
                                      <el-descriptions-item label="预计利润">
                                        <span class="profit-text">
                                          ¥{{ agent.details.estimated_profit.toLocaleString() }}
                                        </span>
                                      </el-descriptions-item>
                                    </el-descriptions>
                                  </el-card>
                                </el-col>
                              </el-row>
                            </div>
                          </template>
                        </el-collapse-item>
                      </el-collapse>
                    </div>
                  </div>
                </el-card>
              </div>

              <!-- 原始数据 -->
              <el-card class="raw-data-card">
                <template #header>
                  <div class="card-header">
                    <h4>原始数据</h4>
                  </div>
                </template>
                <el-collapse>
                  <el-collapse-item title="查看原始数据">
                    <pre>{{ JSON.stringify(result.result.details, null, 2) }}</pre>
                  </el-collapse-item>
                </el-collapse>
              </el-card>
            </div>
          </div>
          <div v-else class="empty-result">
            <el-empty description="请输入指令开始操作" />
          </div>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { Connection, Document, Delete } from '@element-plus/icons-vue'
import { nlpService } from '@/services/nlp'
import type { NLPResponse } from '@/services/nlp'

const userInput = ref('')
const loading = ref(false)
const percentage = ref(0)
const result = ref<NLPResponse | null>(null)

// 历史记录
interface HistoryItem {
  text: string
  status: string
  timestamp: string
  result: NLPResponse
}

const historyList = ref<HistoryItem[]>([])

// 加载历史记录项
const loadHistoryItem = (item: HistoryItem) => {
  userInput.value = item.text
  result.value = item.result
}

// 清空历史记录
const clearHistory = () => {
  historyList.value = []
}

// 处理命令
const processCommand = async () => {
  if (!userInput.value.trim()) {
    ElMessage.warning('请输入操作指令')
    return
  }

  loading.value = true
  percentage.value = 0
  result.value = null

  try {
    // 模拟进度
    const timer = setInterval(() => {
      if (percentage.value < 90) {
        percentage.value += 10
      }
    }, 200)

    const response = await nlpService.processText({
      text: userInput.value,
      requireAgents: true
    })

    clearInterval(timer)
    percentage.value = 100
    result.value = response

    // 添加到历史记录
    historyList.value.unshift({
      text: userInput.value,
      status: response.status,
      timestamp: new Date().toLocaleTimeString(),
      result: response
    })

    if (response.status === 'success') {
      ElMessage.success('执行成功')
    } else {
      ElMessage.error(response.message || '执行失败')
    }
  } catch (error: any) {
    console.error('执行出错:', error)
    ElMessage.error(error.message || '执行失败，请重试')
    result.value = {
      status: 'error',
      result: {
        type: '错误',
        content: error.message || '执行失败',
        details: {},
        processed_at: new Date().toISOString()
      },
      message: '执行失败，请重试',
      timestamp: new Date().toISOString()
    }
  } finally {
    loading.value = false
  }
}

// 清除输入
const clearInput = () => {
  userInput.value = ''
  result.value = null
}

// 格式化Agent名称
const formatAgentName = (name: string) => {
  return name
    .split('_')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ')
}
</script>

<style scoped>
.nlp-container {
  padding: 20px;
  height: 100%;
  background: #f0f2f5;
}

.main-card {
  width: 95%;
  max-width: 2400px;
  margin: 0 auto;
  height: 100%;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 12px;
}

.card-header h2 {
  margin: 0;
}

.content-area {
  display: flex;
  gap: 30px;
  padding: 20px;
  height: calc(100% - 60px);
}

/* 左侧区域样式 */
.left-section {
  width: 500px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.input-section {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.history-section {
  flex: 1;
  background: #fff;
  border-radius: 4px;
  padding: 20px;
  overflow-y: auto;
}

.history-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.history-header h3 {
  margin: 0;
  font-size: 16px;
}

.history-list {
  height: calc(100% - 40px);
  overflow-y: auto;
}

.history-item {
  cursor: pointer;
  transition: all 0.3s;
}

.history-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 2px 12px 0 rgba(0,0,0,0.1);
}

.history-text {
  margin: 0 0 8px 0;
  font-size: 14px;
  color: #606266;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* 右侧区域样式 */
.result-section {
  flex: 1;
  background: #fff;
  border-radius: 4px;
  padding: 20px;
  overflow-y: auto;
}

.result-section h3 {
  margin-top: 0;
  margin-bottom: 20px;
}

.result-area {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.result-details {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.info-card,
.agent-card,
.raw-data-card {
  border: 1px solid #e4e7ed;
  border-radius: 4px;
  transition: all 0.3s;
}

.info-card:hover,
.agent-card:hover {
  box-shadow: 0 2px 12px 0 rgba(0,0,0,.1);
}

.agent-header {
  display: flex;
  align-items: center;
  gap: 8px;
}

.agent-header .el-icon {
  font-size: 18px;
  color: #409EFF;
}

.agent-content {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.agent-action {
  font-size: 14px;
  line-height: 1.6;
}

.agent-details pre {
  margin: 0;
  white-space: pre-wrap;
  word-wrap: break-word;
  background: #f8f9fa;
  padding: 12px;
  border-radius: 4px;
  font-size: 13px;
}

.empty-result {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 300px;
}

:deep(.el-card__header) {
  padding: 12px 16px;
  border-bottom: 1px solid #e4e7ed;
}

:deep(.el-descriptions__cell) {
  padding: 12px 16px;
}

.finance-summary {
  margin-top: 16px;
}

.finance-summary .el-card {
  margin-bottom: 16px;
}

.finance-summary h5 {
  margin: 0;
  font-size: 16px;
  color: #606266;
}

.profit-text {
  color: #67c23a;
  font-weight: bold;
}

:deep(.el-timeline-item__timestamp) {
  font-size: 13px;
  color: #909399;
}

:deep(.el-timeline-item__content h4) {
  margin: 0;
  font-size: 14px;
  color: #303133;
}

:deep(.el-timeline-item__content p) {
  margin: 4px 0 0;
  font-size: 13px;
  color: #606266;
}

.agent-card {
  margin-bottom: 16px;
}

.collapse-title {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #409EFF;
}

.collapse-title .el-icon {
  font-size: 16px;
}

:deep(.el-collapse-item__header) {
  font-size: 14px;
  color: #409EFF;
}

:deep(.el-collapse-item__content) {
  padding: 16px;
  background: #f8f9fa;
  border-radius: 4px;
}

/* 描述列表样式优化 */
:deep(.el-descriptions) {
  width: 100%;
}

:deep(.el-descriptions__cell) {
  padding: 16px 20px;
}

:deep(.el-descriptions__label) {
  width: 120px;
  text-align: right;
  font-weight: bold;
  background-color: #f5f7fa;
}

:deep(.el-descriptions__content) {
  min-width: 300px;
  word-break: break-all;
}

/* 卡片样式优化 */
.info-card {
  margin-bottom: 20px;
}

:deep(.el-card__header) {
  padding: 12px 20px;
  background-color: #f5f7fa;
}

:deep(.el-card__body) {
  padding: 20px;
}

/* 标题样式 */
.card-header h4 {
  margin: 0;
  font-size: 16px;
  color: #303133;
}

/* 基本信息卡片样式 */
.info-card {
  margin-bottom: 20px;
}

.info-card :deep(.el-descriptions__cell) {
  padding: 12px 16px;
}

.info-card :deep(.el-descriptions__label) {
  width: 100px;
  text-align: right;
  font-weight: bold;
  background-color: #f5f7fa;
  white-space: nowrap;
}

.info-card :deep(.el-descriptions__content) {
  min-width: 200px;
}

.description-item {
  width: 100%;
}

.scrollable-content {
  max-height: 100px;
  overflow-y: auto;
  padding: 4px;
  word-break: break-all;
  line-height: 1.5;
}

.scrollable-content::-webkit-scrollbar {
  width: 6px;
}

.scrollable-content::-webkit-scrollbar-thumb {
  background-color: #909399;
  border-radius: 3px;
}

.scrollable-content::-webkit-scrollbar-track {
  background-color: #f5f7fa;
  border-radius: 3px;
}
</style> 