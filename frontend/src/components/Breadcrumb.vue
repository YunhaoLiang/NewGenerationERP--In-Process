<template>
  <el-breadcrumb separator="/">
    <el-breadcrumb-item v-for="item in breadcrumbs" :key="item.path" :to="item.path">
      {{ item.title }}
    </el-breadcrumb-item>
  </el-breadcrumb>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

const breadcrumbs = computed(() => {
  return route.matched
    .filter(item => item.meta?.title)
    .map(item => ({
      title: item.meta.title,
      path: item.path
    }))
})
</script>

<style scoped>
.el-breadcrumb {
  line-height: 1;
}
</style> 