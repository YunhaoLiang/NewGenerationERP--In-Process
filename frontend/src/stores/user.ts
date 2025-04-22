import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { UserInfo } from '@/types/user'
import { login as apiLogin } from '@/api/auth'

export const useUserStore = defineStore('user', () => {
  const token = ref('')
  const userInfo = ref<UserInfo | null>(null)
  const avatar = ref('/default-avatar.png') // 默认头像

  const login = async (username: string, password: string) => {
    try {
      const { data } = await apiLogin(username, password)
      token.value = data.token
      userInfo.value = data.user
      return true
    } catch (error) {
      console.error('Login failed:', error)
      return false
    }
  }

  const logout = async () => {
    token.value = ''
    userInfo.value = null
  }

  const username = computed(() => userInfo.value?.username || '')

  return {
    token,
    userInfo,
    username,
    avatar,
    login,
    logout
  }
}) 