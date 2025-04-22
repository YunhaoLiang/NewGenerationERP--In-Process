<template>
  <div class="app-wrapper">
    <!-- 侧边栏 -->
    <div class="sidebar-container">
      <el-menu
        :default-active="route.path"
        class="el-menu-vertical"
        :collapse="isCollapse"
        background-color="#304156"
        text-color="#bfcbd9"
        active-text-color="#409EFF"
      >
        <el-menu-item index="/dashboard" @click="router.push('/dashboard')">
          <el-icon><Monitor /></el-icon>
          <template #title>仪表盘</template>
        </el-menu-item>

        <el-menu-item index="/inventory" @click="router.push('/inventory')">
          <el-icon><Box /></el-icon>
          <template #title>库存管理</template>
        </el-menu-item>

        <el-menu-item index="/products" @click="router.push('/products')">
          <el-icon><Goods /></el-icon>
          <template #title>产品管理</template>
        </el-menu-item>

        <el-menu-item index="/orders" @click="router.push('/orders')">
          <el-icon><List /></el-icon>
          <template #title>订单管理</template>
        </el-menu-item>

        <el-menu-item index="/suppliers" @click="router.push('/suppliers')">
          <el-icon><Connection /></el-icon>
          <template #title>供应商管理</template>
        </el-menu-item>

        <el-sub-menu index="/finance">
          <template #title>
            <el-icon><Money /></el-icon>
            <span>财务管理</span>
          </template>
          <el-menu-item index="/finance/accounts">账户管理</el-menu-item>
          <el-menu-item index="/finance/transactions">交易记录</el-menu-item>
          <el-menu-item index="/finance/budgets">预算管理</el-menu-item>
        </el-sub-menu>

        <el-menu-item index="/users" v-if="authStore.hasRole(['admin'])">
          <el-icon><User /></el-icon>
          <template #title>用户管理</template>
        </el-menu-item>
      </el-menu>
    </div>

    <!-- 主容器 -->
    <div class="main-container">
      <!-- 顶部栏 -->
      <div class="navbar">
        <div class="left">
          <el-button
            type="text"
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
  Fold
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
  // TODO: 实现个人信息页面
  console.log('个人信息')
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
  height: 100%;
  display: flex;
}

.sidebar-container {
  background-color: #304156;
  height: 100%;
  transition: width 0.3s;
  width: var(--sidebar-width, 210px);
}

.sidebar-container.is-collapse {
  width: 64px;
}

.main-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.navbar {
  height: 50px;
  background: #fff;
  box-shadow: 0 1px 4px rgba(0, 21, 41, 0.08);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 16px;
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
  padding: 0 12px;
  cursor: pointer;
  font-size: 20px;
}

.user-dropdown {
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 4px;
  color: #606266;
}

.app-main {
  flex: 1;
  overflow: auto;
  background-color: #f0f2f5;
  padding: 16px;
}

/* 路由过渡动画 */
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