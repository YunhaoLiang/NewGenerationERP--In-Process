<template>
  <div class="finance-container">
    <el-card class="finance-card">
      <template #header>
        <div class="card-header">
          <h3>财务管理</h3>
        </div>
      </template>

      <el-menu
        mode="horizontal"
        router
        :default-active="activeMenu"
        class="finance-menu"
      >
        <el-menu-item index="/finance/accounts">
          <el-icon><Wallet /></el-icon>
          账户管理
        </el-menu-item>
        <el-menu-item index="/finance/transactions">
          <el-icon><Money /></el-icon>
          交易记录
        </el-menu-item>
        <el-menu-item index="/finance/budgets">
          <el-icon><PieChart /></el-icon>
          预算管理
        </el-menu-item>
      </el-menu>

      <div class="finance-content">
        <router-view></router-view>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { Wallet, Money, PieChart } from '@element-plus/icons-vue'

const route = useRoute()
const activeMenu = computed(() => route.path)
</script>

<style scoped>
.finance-container {
  padding: 20px;
}

.finance-card {
  min-height: calc(100vh - 140px);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.finance-menu {
  margin-bottom: 20px;
  background-color: transparent;
}

.finance-content {
  padding: 20px 0;
}
</style> 