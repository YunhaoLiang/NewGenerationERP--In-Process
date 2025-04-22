<script setup lang="ts">
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const authStore = useAuthStore()
</script>

<template>
  <div class="app-container">
    <router-view v-slot="{ Component }">
      <component :is="Component" />
    </router-view>
  </div>
</template>

<style>
:root {
  --primary-gradient: linear-gradient(135deg, #1a2980 0%, #26d0ce 100%);
  --secondary-gradient: linear-gradient(135deg, #141e30 0%, #243b55 100%);
  --card-bg: rgba(255, 255, 255, 0.95);
  --hover-color: rgba(38, 208, 206, 0.1);
  --menu-bg: #ffffff;
  --menu-dark-bg: #f5f7fa;
  --primary-text: #2c3e50;
  --border-color: #e4e7ed;
  --page-bg: #f5f7fa;
  --hover-bg: #f5f7fa;
  --primary-color: #1a2980;
}

html, body {
  margin: 0;
  padding: 0;
  height: 100vh;
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', '微软雅黑', Arial, sans-serif;
}

body {
  background: var(--primary-gradient);
}

.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* 全局卡片样式 */
.el-card {
  backdrop-filter: blur(10px);
  background: var(--card-bg) !important;
  border: none !important;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1) !important;
  transition: all 0.3s ease;
}

.el-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 25px rgba(0, 0, 0, 0.15) !important;
}

/* 表格样式优化 */
.el-table {
  background: transparent !important;
}

.el-table th {
  background: var(--secondary-gradient) !important;
  color: white !important;
}

.el-table tr:hover > td {
  background: var(--hover-color) !important;
}

/* 按钮样式优化 */
.el-button--primary {
  background: var(--primary-gradient) !important;
  border: none !important;
  transition: all 0.3s ease !important;
}

.el-button--primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(38, 208, 206, 0.3);
}

/* 输入框样式优化 */
.el-input__wrapper {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05) !important;
  transition: all 0.3s ease !important;
}

.el-input__wrapper:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1) !important;
}

/* 菜单样式优化 */
.el-menu {
  border: none !important;
  background: transparent !important;
}

.el-menu-item {
  transition: all 0.3s ease !important;
}

.el-menu-item:hover {
  background: var(--hover-color) !important;
  transform: translateX(5px);
}

.el-menu-item.is-active {
  background: var(--primary-gradient) !important;
  color: white !important;
}
</style>
