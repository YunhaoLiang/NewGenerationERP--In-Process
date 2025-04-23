<template>
  <div class="dashboard">
    <h1>仪表盘</h1>
    <dashboard-charts />
  </div>
</template>

<script>
import { defineComponent } from 'vue'
import DashboardCharts from './DashboardCharts.vue'

export default defineComponent({
  name: 'Dashboard',
  components: {
    DashboardCharts
  }
})
</script>

<style scoped>
.dashboard {
  padding: 24px;
}

h1 {
  margin-bottom: 24px;
  color: rgba(0, 0, 0, 0.85);
  font-weight: 500;
  font-size: 24px;
}
</style> 