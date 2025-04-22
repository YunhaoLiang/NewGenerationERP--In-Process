import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import router from '@/router'

export const useAuthStore = defineStore('auth', () => {
  // 状态
  const token = ref<string>(localStorage.getItem('token') || '')
  const userInfo = ref<any>(JSON.parse(localStorage.getItem('userInfo') || 'null'))

  // 计算属性
  const isAuthenticated = computed(() => !!token.value)
  const username = computed(() => userInfo.value?.username || '')

  // 登录
  async function login(username: string, password: string) {
    try {
      // 这里模拟登录，实际项目中需要调用后端API
      if (username === 'admin' && password === 'admin123') {
        const fakeToken = 'fake-token-' + Date.now()
        const fakeUserInfo = { username: 'admin', role: 'admin' }
        
        // 保存登录状态
        token.value = fakeToken
        userInfo.value = fakeUserInfo
        localStorage.setItem('token', fakeToken)
        localStorage.setItem('userInfo', JSON.stringify(fakeUserInfo))
        
        return true
      }
      return false
    } catch (error) {
      console.error('登录失败:', error)
      return false
    }
  }

  // 登出
  function logout() {
    token.value = ''
    userInfo.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('userInfo')
    router.push('/login')
  }

  return {
    token,
    userInfo,
    isAuthenticated,
    username,
    login,
    logout
  }
}) 