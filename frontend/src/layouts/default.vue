<template>
  <el-container class="layout-container">
    <!-- 侧边栏 -->
    <el-aside :width="isCollapse ? '64px' : '240px'" class="aside">
      <div class="logo">
        <img src="@/assets/logo.png" alt="Logo" />
        <span>ERP系统</span>
      </div>
      <el-menu
        :default-active="activeMenu"
        class="el-menu-vertical"
        :router="true"
        :collapse="isCollapse"
        background-color="#1f2d3d"
        text-color="#fff"
        active-text-color="#409EFF"
      >
        <el-menu-item index="/dashboard">
          <el-icon><Monitor /></el-icon>
          <template #title>仪表盘</template>
        </el-menu-item>

        <el-menu-item index="/products">
          <el-icon><Goods /></el-icon>
          <template #title>产品管理</template>
        </el-menu-item>

        <el-menu-item index="/inventory">
          <el-icon><Box /></el-icon>
          <template #title>库存管理</template>
        </el-menu-item>

        <el-menu-item index="/orders">
          <el-icon><List /></el-icon>
          <template #title>订单管理</template>
        </el-menu-item>

        <el-menu-item index="/suppliers">
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
      </el-menu>
    </el-aside>

    <!-- 主要内容区 -->
    <el-container>
      <!-- 顶部导航栏 -->
      <el-header class="header" height="60px">
        <div class="header-left">
          <el-button link @click="toggleSidebar">
            <el-icon><Fold v-if="!isCollapse" /><Expand v-else /></el-icon>
          </el-button>
          <el-breadcrumb separator="/">
            <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item>{{ currentRoute }}</el-breadcrumb-item>
          </el-breadcrumb>
        </div>
        <div class="header-right">
          <el-dropdown>
            <span class="user-info">
              {{ username }}
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
      </el-header>

      <!-- 内容区 -->
      <el-main class="main">
        <router-view></router-view>
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import {
  Monitor,
  Goods,
  Box,
  List,
  Connection,
  Money,
  Fold,
  Expand,
  CaretBottom,
} from '@element-plus/icons-vue';

const route = useRoute();
const router = useRouter();
const isCollapse = ref(false);
const username = ref('Admin'); // 这里应该从用户状态获取

// 当前激活的菜单项
const activeMenu = computed(() => route.path);

// 当前路由名称
const currentRoute = computed(() => route.meta.title || '');

// 切换侧边栏
const toggleSidebar = () => {
  isCollapse.value = !isCollapse.value;
};

// 处理个人信息
const handleProfile = () => {
  // 实现个人信息页面跳转
  console.log('跳转到个人信息页面');
};

// 处理退出登录
const handleLogout = () => {
  localStorage.removeItem('token');
  router.push('/login');
};
</script>

<style scoped>
.layout-container {
  height: 100vh;
  width: 100vw;
}

.aside {
  background-color: #1f2d3d;
  color: #fff;
  transition: width 0.3s;
  overflow: hidden;
}

.logo {
  height: 60px;
  display: flex;
  align-items: center;
  padding: 0 20px;
  background-color: #1a2634;
  border-bottom: 1px solid #283445;
}

.logo img {
  width: 32px;
  height: 32px;
  margin-right: 12px;
}

.logo span {
  font-size: 20px;
  font-weight: bold;
  color: #fff;
  white-space: nowrap;
}

.header {
  background-color: #fff;
  border-bottom: 1px solid #dcdfe6;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  position: relative;
  z-index: 999;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 20px;
}

.header-right {
  display: flex;
  align-items: center;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

.main {
  background-color: #f0f2f5;
  padding: 20px;
  height: calc(100vh - 60px);
  overflow-y: auto;
}

:deep(.el-menu) {
  border-right: none;
}

:deep(.el-menu-item) {
  border-left: 3px solid transparent;
}

:deep(.el-menu-item.is-active) {
  background-color: #1a2634 !important;
  border-left: 3px solid #409EFF;
  color: #409EFF !important;
}

:deep(.el-menu-item:hover), :deep(.el-sub-menu__title:hover) {
  background-color: #283445 !important;
}

:deep(.el-menu--collapse) {
  width: 64px;
}

:deep(.el-sub-menu__title) {
  border-left: 3px solid transparent;
}

:deep(.el-menu-item .el-icon), :deep(.el-sub-menu .el-icon) {
  color: #909399;
  margin-right: 16px;
  width: 24px;
  text-align: center;
}

:deep(.el-menu-item.is-active .el-icon) {
  color: #409EFF;
}

:deep(.el-menu-item:hover .el-icon), :deep(.el-sub-menu__title:hover .el-icon) {
  color: #fff;
}
</style> 