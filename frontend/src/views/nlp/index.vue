<template>
  <div class="nlp-container">
    <div class="tech-background">
      <div class="tech-grid"></div>
      <div class="tech-glow"></div>
    </div>
    <el-card class="nlp-card">
      <template #header>
        <div class="card-header">
          <div class="title-section">
            <el-icon class="tech-icon"><ChatLineRound /></el-icon>
            <span class="title-text">自然语言处理</span>
          </div>
          <div class="header-actions">
            <el-button type="primary" link @click="clearHistory">
              <el-icon><Delete /></el-icon>
              <span>清空历史</span>
            </el-button>
          </div>
        </div>
      </template>
      <div class="chat-container">
        <div class="chat-messages" ref="chatMessagesRef">
          <div v-for="(message, index) in messages" :key="index" 
               :class="['message', message.type]">
            <div class="message-content">
              <div class="message-header">
                <el-icon v-if="message.type === 'user'" class="user-icon"><User /></el-icon>
                <el-icon v-else-if="message.type === 'system'" class="system-icon"><Cpu /></el-icon>
                <el-icon v-else class="error-icon"><Warning /></el-icon>
                <span class="message-type">{{ getMessageTypeText(message.type) }}</span>
                <span class="message-time">{{ message.time }}</span>
              </div>
              <div class="message-text">{{ message.text }}</div>
            </div>
          </div>
        </div>
        <div class="chat-input">
          <el-input
            v-model="userInput"
            placeholder="请输入自然语言指令，例如：查询上个月的销售数据"
            @keyup.enter="processInput"
            class="tech-input"
          >
            <template #prefix>
              <el-icon><Edit /></el-icon>
            </template>
            <template #append>
              <el-button type="primary" @click="processInput" class="tech-button">
                <el-icon><Position /></el-icon>
                <span>发送</span>
              </el-button>
            </template>
          </el-input>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, nextTick } from 'vue'
import {
  ChatLineRound,
  User,
  Cpu,
  Warning,
  Edit,
  Position,
  Delete
} from '@element-plus/icons-vue'

const messages = ref<Array<{type: string, text: string, time: string}>>([])
const userInput = ref('')
const chatMessagesRef = ref<HTMLElement | null>(null)

const getMessageTypeText = (type: string) => {
  const typeMap: Record<string, string> = {
    'user': '用户',
    'system': '系统',
    'error': '错误'
  }
  return typeMap[type] || ''
}

const processInput = async () => {
  if (!userInput.value.trim()) return
  
  // 添加用户消息
  const userMessage = {
    type: 'user',
    text: userInput.value,
    time: new Date().toLocaleTimeString()
  }
  messages.value.push(userMessage)
  
  // 清空输入
  const input = userInput.value
  userInput.value = ''
  
  // 滚动到底部
  nextTick(() => {
    if (chatMessagesRef.value) {
      chatMessagesRef.value.scrollTop = chatMessagesRef.value.scrollHeight
    }
  })
  
  try {
    // 调用后端API处理自然语言
    const response = await fetch('/api/process_nlp', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        text: input
      })
    })
    
    const result = await response.json()
    
    // 添加系统回复
    const systemMessage = {
      type: 'system',
      text: result.message || '指令已处理完成',
      time: new Date().toLocaleTimeString()
    }
    messages.value.push(systemMessage)
    
  } catch (error) {
    // 添加错误消息
    const errorMessage = {
      type: 'error',
      text: '处理指令时出错，请稍后重试',
      time: new Date().toLocaleTimeString()
    }
    messages.value.push(errorMessage)
  }
}

const clearHistory = () => {
  messages.value = []
}
</script>

<style scoped>
.nlp-container {
  padding: 24px;
  height: 100%;
  position: relative;
  overflow: hidden;
}

.tech-background {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
  z-index: 0;
}

.tech-grid {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image: 
    linear-gradient(rgba(255, 255, 255, 0.05) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.05) 1px, transparent 1px);
  background-size: 20px 20px;
  opacity: 0.3;
}

.tech-glow {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 200px;
  height: 200px;
  background: radial-gradient(circle, rgba(0, 150, 255, 0.2) 0%, transparent 70%);
  transform: translate(-50%, -50%);
  animation: pulse 4s ease-in-out infinite;
}

@keyframes pulse {
  0% { opacity: 0.3; }
  50% { opacity: 0.6; }
  100% { opacity: 0.3; }
}

.nlp-card {
  height: 100%;
  display: flex;
  flex-direction: column;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  position: relative;
  z-index: 1;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
}

.title-section {
  display: flex;
  align-items: center;
  gap: 12px;
}

.tech-icon {
  font-size: 24px;
  color: #1890ff;
  animation: float 3s ease-in-out infinite;
}

@keyframes float {
  0% { transform: translateY(0); }
  50% { transform: translateY(-5px); }
  100% { transform: translateY(0); }
}

.title-text {
  font-size: 18px;
  font-weight: 600;
  background: linear-gradient(90deg, #1890ff, #722ed1);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.header-actions {
  display: flex;
  gap: 8px;
}

.chat-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 0;
  padding: 16px;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.message {
  display: flex;
  animation: fadeIn 0.3s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.message.user {
  justify-content: flex-end;
}

.message.system {
  justify-content: flex-start;
}

.message.error {
  justify-content: flex-start;
}

.message-content {
  max-width: 80%;
  padding: 16px;
  border-radius: 12px;
  position: relative;
  overflow: hidden;
}

.message-content::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(45deg, transparent, rgba(255, 255, 255, 0.1), transparent);
  transform: translateX(-100%);
  animation: shine 3s infinite;
}

@keyframes shine {
  100% { transform: translateX(100%); }
}

.message-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.message-type {
  font-size: 12px;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.message-time {
  font-size: 12px;
  opacity: 0.7;
  margin-left: auto;
}

.user-icon, .system-icon, .error-icon {
  font-size: 16px;
}

.message.user .message-content {
  background: linear-gradient(135deg, #1890ff, #096dd9);
  color: white;
}

.message.system .message-content {
  background: linear-gradient(135deg, #f0f2f5, #e6e8eb);
  color: #1f2937;
}

.message.error .message-content {
  background: linear-gradient(135deg, #fff2f0, #ffccc7);
  color: #ff4d4f;
}

.message-text {
  word-break: break-word;
  line-height: 1.6;
}

.chat-input {
  padding: 16px;
  background: rgba(255, 255, 255, 0.8);
  border-top: 1px solid rgba(0, 0, 0, 0.1);
}

.tech-input {
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  transition: all 0.3s;
}

.tech-input:hover, .tech-input:focus {
  border-color: #1890ff;
  box-shadow: 0 0 0 2px rgba(24, 144, 255, 0.2);
}

.tech-button {
  display: flex;
  align-items: center;
  gap: 8px;
  background: linear-gradient(135deg, #1890ff, #096dd9);
  border: none;
  transition: all 0.3s;
}

.tech-button:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(24, 144, 255, 0.3);
}

:deep(.el-card__header) {
  padding: 0;
}

:deep(.el-input__wrapper) {
  box-shadow: none;
}

:deep(.el-input-group__append) {
  padding: 0;
  border: none;
}
</style> 