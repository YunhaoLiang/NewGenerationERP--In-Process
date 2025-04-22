<template>
  <div class="nlp-container">
    <el-card class="input-card">
      <template #header>
        <div class="card-header">
          <span>自然语言处理</span>
          <el-tag type="success">AI 助手</el-tag>
        </div>
      </template>
      
      <div class="input-section">
        <el-input
          v-model="userInput"
          type="textarea"
          :rows="4"
          placeholder="请输入您的问题或描述，例如：'帮我分析最近一周的销售趋势'"
          :disabled="loading"
        />
        
        <div class="button-group">
          <el-button
            type="primary"
            :loading="loading"
            @click="handleAnalyze"
          >
            分析
          </el-button>
          <el-button @click="clearInput">清空</el-button>
        </div>
      </div>
    </el-card>

    <el-card v-if="result" class="result-card">
      <template #header>
        <div class="card-header">
          <span>分析结果</span>
          <el-button type="primary" link @click="handleExport">导出报告</el-button>
        </div>
      </template>
      
      <div class="result-content">
        <div v-if="result.summary" class="summary-section">
          <h3>摘要</h3>
          <p>{{ result.summary }}</p>
        </div>

        <div v-if="result.chart" class="chart-section">
          <h3>数据可视化</h3>
          <div class="chart-placeholder">
            图表区域
          </div>
        </div>

        <div v-if="result.details" class="details-section">
          <h3>详细分析</h3>
          <el-collapse>
            <el-collapse-item
              v-for="(detail, index) in result.details"
              :key="index"
              :title="detail.title"
            >
              <p>{{ detail.content }}</p>
            </el-collapse-item>
          </el-collapse>
        </div>

        <div v-if="result.suggestions" class="suggestions-section">
          <h3>建议</h3>
          <el-timeline>
            <el-timeline-item
              v-for="(suggestion, index) in result.suggestions"
              :key="index"
              :type="suggestion.type"
            >
              {{ suggestion.content }}
            </el-timeline-item>
          </el-timeline>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage } from 'element-plus'

const userInput = ref('')
const loading = ref(false)
const result = ref<any>(null)

// 模拟 AI 分析过程
const handleAnalyze = async () => {
  if (!userInput.value.trim()) {
    ElMessage.warning('请输入需要分析的内容')
    return
  }

  loading.value = true
  try {
    // 这里应该调用后端 API 进行实际的分析
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    // 模拟返回结果
    result.value = {
      summary: '根据分析，最近一周的销售情况整体呈上升趋势，环比增长15%。主要增长来自电子产品类别，其中智能手机销量增长最为显著。',
      details: [
        {
          title: '销售趋势分析',
          content: '周环比增长15%，日均销售额达到¥12,680，较上周提升¥1,650。'
        },
        {
          title: '品类分布',
          content: '电子产品占比45%，服装占比30%，食品占比15%，其他占比10%。'
        },
        {
          title: '客户分析',
          content: '新客户占比23%，复购率达到68%，客单价较上周提升12%。'
        }
      ],
      suggestions: [
        {
          type: 'success',
          content: '建议增加电子产品的库存，特别是热销机型。'
        },
        {
          type: 'warning',
          content: '服装类商品库存较高，建议适当促销清理。'
        },
        {
          type: 'info',
          content: '可以考虑针对高复购率客户推出会员专享活动。'
        }
      ]
    }
  } catch (error) {
    ElMessage.error('分析失败，请重试')
  } finally {
    loading.value = false
  }
}

const clearInput = () => {
  userInput.value = ''
  result.value = null
}

const handleExport = () => {
  ElMessage.success('报告已导出')
}
</script>

<style scoped>
.nlp-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.input-section {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.button-group {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
}

.result-content {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.result-content h3 {
  margin: 0 0 16px;
  color: #1f2f3d;
  font-weight: 500;
}

.chart-section {
  min-height: 300px;
}

.chart-placeholder {
  height: 300px;
  background: #f5f7fa;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #909399;
}

.details-section {
  border-top: 1px solid #ebeef5;
  padding-top: 20px;
}

.suggestions-section {
  border-top: 1px solid #ebeef5;
  padding-top: 20px;
}

:deep(.el-collapse-item__header) {
  font-weight: 500;
}

:deep(.el-timeline-item__node--success) {
  background-color: #67c23a;
}

:deep(.el-timeline-item__node--warning) {
  background-color: #e6a23c;
}

:deep(.el-timeline-item__node--info) {
  background-color: #909399;
}
</style> 