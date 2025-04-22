<template>
  <div class="login-page">
    <div class="login-box">
      <div class="login-left">
        <div class="welcome-text">
          <h2>欢迎使用</h2>
          <h1>新一代ERP系统</h1>
          <p>提升效率 · 智能管理 · 数据驱动</p>
        </div>
      </div>
      <div class="login-right">
        <div class="login-form-container">
          <h2>账号登录</h2>
          <el-form
            ref="loginFormRef"
            :model="loginForm"
            :rules="loginRules"
            @keyup.enter="handleLogin"
          >
            <el-form-item prop="username">
              <el-input
                v-model="loginForm.username"
                placeholder="请输入用户名"
                :prefix-icon="User"
              />
            </el-form-item>
            <el-form-item prop="password">
              <el-input
                v-model="loginForm.password"
                type="password"
                placeholder="请输入密码"
                :prefix-icon="Lock"
                show-password
              />
            </el-form-item>
            <div class="remember-forgot">
              <el-checkbox v-model="rememberMe">记住我</el-checkbox>
              <a href="#" class="forgot-link">忘记密码？</a>
            </div>
            <el-button
              type="primary"
              :loading="loading"
              class="submit-btn"
              @click="handleLogin"
            >
              登录
            </el-button>
          </el-form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Lock } from '@element-plus/icons-vue'
import type { FormInstance } from 'element-plus'

const router = useRouter()
const loginFormRef = ref<FormInstance>()
const loading = ref(false)
const rememberMe = ref(false)

const loginForm = ref({
  username: '',
  password: ''
})

const loginRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, message: '用户名长度不能小于3位', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能小于6位', trigger: 'blur' }
  ]
}

const handleLogin = async () => {
  if (!loginFormRef.value) return
  
  await loginFormRef.value.validate(async (valid: boolean) => {
    if (valid) {
      try {
        loading.value = true
        const response = await fetch('http://localhost:3000/api/auth/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(loginForm.value)
        })

        const data = await response.json()

        if (!response.ok) {
          throw new Error(data.message || '登录失败')
        }

        localStorage.setItem('token', data.access_token)
        if (rememberMe.value) {
          localStorage.setItem('username', loginForm.value.username)
        }
        ElMessage.success('登录成功')
        router.push('/main/dashboard')
      } catch (error: any) {
        ElMessage.error(error.message || '登录失败')
      } finally {
        loading.value = false
      }
    }
  })
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  width: 100vw;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #001529;
  background-image: 
    radial-gradient(circle at 50% 50%, rgba(24, 144, 255, 0.1) 0%, transparent 80%),
    linear-gradient(135deg, rgba(0, 21, 41, 0.9) 0%, rgba(0, 21, 41, 0.8) 100%);
  overflow: hidden;
  position: fixed;
  top: 0;
  left: 0;
}

.login-box {
  width: 1000px;
  height: 600px;
  display: flex;
  border-radius: 12px;
  overflow: hidden;
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.login-left {
  flex: 1;
  background: rgba(24, 144, 255, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px;
  color: white;
  position: relative;
  overflow: hidden;
}

.login-left::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(24, 144, 255, 0.2), rgba(9, 109, 217, 0.2));
  z-index: 1;
}

.welcome-text {
  text-align: center;
  position: relative;
  z-index: 2;
}

.welcome-text h1 {
  font-size: 36px;
  font-weight: 600;
  margin: 20px 0;
  background: linear-gradient(to right, #40a9ff, #1890ff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.welcome-text h2 {
  font-size: 24px;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 10px;
}

.welcome-text p {
  font-size: 16px;
  color: rgba(255, 255, 255, 0.7);
}

.login-right {
  flex: 1;
  background: rgba(0, 0, 0, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px;
}

.login-form-container {
  width: 320px;
}

.login-form-container h2 {
  font-size: 24px;
  color: #fff;
  margin-bottom: 30px;
  text-align: center;
}

.remember-forgot {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 20px 0;
}

.forgot-link {
  color: #1890ff;
  text-decoration: none;
  font-size: 14px;
  opacity: 0.8;
  transition: opacity 0.3s;
}

.forgot-link:hover {
  opacity: 1;
}

.submit-btn {
  width: 100%;
  height: 40px;
  font-size: 16px;
  background: #1890ff;
  border: none;
  transition: all 0.3s;
}

.submit-btn:hover {
  background: #40a9ff;
  transform: translateY(-1px);
}

.submit-btn:active {
  background: #096dd9;
  transform: translateY(0);
}

:deep(.el-input__wrapper) {
  background: rgba(255, 255, 255, 0.04) !important;
  box-shadow: 0 0 0 1px rgba(255, 255, 255, 0.1) !important;
  border-radius: 4px;
}

:deep(.el-input__wrapper:hover) {
  box-shadow: 0 0 0 1px #1890ff !important;
}

:deep(.el-input__wrapper.is-focus) {
  box-shadow: 0 0 0 1px #1890ff !important;
  border-color: #1890ff;
}

:deep(.el-input__inner) {
  color: #fff !important;
  height: 24px;
}

:deep(.el-input__inner::placeholder) {
  color: rgba(255, 255, 255, 0.3);
}

:deep(.el-checkbox__label) {
  color: rgba(255, 255, 255, 0.8);
}

:deep(.el-checkbox__input.is-checked .el-checkbox__inner) {
  background-color: #1890ff;
  border-color: #1890ff;
}

:deep(.el-form-item__error) {
  color: #ff4d4f;
}

:deep(.el-input__prefix-inner) {
  color: rgba(255, 255, 255, 0.45);
}
</style> 