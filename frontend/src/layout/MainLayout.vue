<template>
  <div class="app-wrapper">
    <!-- 侧边栏 -->
    <div class="sidebar-container" :class="{ 'is-collapse': isCollapse }">
      <div class="logo">
        <img src="@/assets/logo.png" alt="Logo">
        <span v-show="!isCollapse">ERP 系统</span>
      </div>
      
      <el-menu
        :default-active="route.path"
        :collapse="isCollapse"
        class="sidebar-menu"
        background-color="#001529"
        text-color="#fff"
        active-text-color="#409EFF"
        router
      >
        <el-menu-item index="/main/dashboard">
          <el-icon><Monitor /></el-icon>
          <template #title>仪表盘</template>
        </el-menu-item>

        <el-menu-item index="/main/users">
          <el-icon><User /></el-icon>
          <template #title>用户管理</template>
        </el-menu-item>

        <el-menu-item index="/main/products">
          <el-icon><Goods /></el-icon>
          <template #title>产品管理</template>
        </el-menu-item>

        <el-menu-item index="/main/inventory">
          <el-icon><Box /></el-icon>
          <template #title>库存管理</template>
        </el-menu-item>

        <el-menu-item index="/main/orders">
          <el-icon><List /></el-icon>
          <template #title>订单管理</template>
        </el-menu-item>

        <el-menu-item index="/main/suppliers">
          <el-icon><Connection /></el-icon>
          <template #title>供应商管理</template>
        </el-menu-item>

        <el-menu-item index="/main/nlp">
          <el-icon><ChatDotRound /></el-icon>
          <template #title>自然语言处理</template>
        </el-menu-item>

        <el-sub-menu index="/main/finance">
          <template #title>
            <el-icon><Money /></el-icon>
            <span>财务管理</span>
          </template>
          <el-menu-item index="/main/finance/accounts">账户管理</el-menu-item>
          <el-menu-item index="/main/finance/transactions">交易记录</el-menu-item>
          <el-menu-item index="/main/finance/budgets">预算管理</el-menu-item>
        </el-sub-menu>
      </el-menu>
    </div>

    <!-- 主容器 -->
    <div class="main-container">
      <!-- 顶部栏 -->
      <div class="navbar">
        <div class="left">
          <el-button
            link
            @click="toggleSidebar"
            class="hamburger"
          >
            <el-icon>
              <component :is="isCollapse ? 'Expand' : 'Fold'" />
            </el-icon>
          </el-button>
          <breadcrumb />
        </div>
        <div class="right">
          <el-dropdown trigger="click">
            <span class="user-dropdown">
              {{ authStore.username }}
              <el-icon><CaretBottom /></el-icon>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click="handleProfile">个人信息</el-dropdown-item>
                <el-dropdown-item @click="handleLogout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </div>

      <!-- 内容区 -->
      <div class="app-main">
        <router-view v-slot="{ Component }">
          <transition name="fade-transform" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import {
  Monitor,
  Box,
  Goods,
  List,
  Connection,
  Money,
  User,
  CaretBottom,
  Expand,
  Fold,
  ChatDotRound
} from '@element-plus/icons-vue'
import { ElMessageBox } from 'element-plus'
import Breadcrumb from '@/components/Breadcrumb.vue'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()
const isCollapse = ref(false)

const toggleSidebar = () => {
  isCollapse.value = !isCollapse.value
}

const handleProfile = () => {
  router.push('/main/profile')
}

const handleLogout = () => {
  ElMessageBox.confirm('确定要退出登录吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    authStore.logout()
    router.push('/login')
  })
}
</script>

<style scoped>
.app-wrapper {
  position: relative;
  height: 100vh;
  width: 100%;
}

.sidebar-container {
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  width: 240px;
  background-color: #001529;
  transition: width 0.3s;
  z-index: 1001;
  overflow: hidden;
}

.sidebar-container.is-collapse {
  width: 64px;
}

.logo {
  height: 60px;
  padding: 10px;
  display: flex;
  align-items: center;
  background: #002140;
  overflow: hidden;
}

.logo img {
  width: 32px;
  height: 32px;
  margin-right: 12px;
}

.logo span {
  color: white;
  font-size: 20px;
  font-weight: 600;
  white-space: nowrap;
}

.sidebar-menu {
  border: none;
}

.main-container {
  position: relative;
  min-height: 100%;
  margin-left: 240px;
  transition: margin-left 0.3s;
  width: calc(100% - 240px);
  padding: 0;
  display: flex;
  flex-direction: column;
}

.sidebar-container.is-collapse + .main-container {
  margin-left: 64px;
  width: calc(100% - 64px);
}

.app-main {
  flex: 1;
  padding: 0;
  background: #f0f2f5;
  position: relative;
  overflow-x: auto;
  min-width: 800px;
}

.navbar {
  height: 60px;
  padding: 0 16px;
  background: white;
  box-shadow: 0 1px 4px rgba(0, 21, 41, 0.08);
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: relative;
  z-index: 1000;
}

.navbar .left {
  display: flex;
  align-items: center;
}

.navbar .right {
  display: flex;
  align-items: center;
}

.hamburger {
  padding: 0 15px;
  cursor: pointer;
  font-size: 20px;
}

.user-dropdown {
  cursor: pointer;
  display: flex;
  align-items: center;
  font-size: 14px;
  color: #666;
}

.user-dropdown .el-icon {
  margin-left: 4px;
}

/* 过渡动画 */
.fade-transform-enter-active,
.fade-transform-leave-active {
  transition: all 0.3s;
}

.fade-transform-enter-from {
  opacity: 0;
  transform: translateX(-30px);
}

.fade-transform-leave-to {
  opacity: 0;
  transform: translateX(30px);
}
</style> 