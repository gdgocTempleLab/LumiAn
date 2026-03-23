<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { ElMessage } from 'element-plus'
import templeBg from '@/assets/images/temple.jpg'
import logoPic from '@/assets/images/logo_pic.png'
import logoText from '@/assets/images/logo.png'
import logoWord from '@/assets/images/logo_word.png'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const form = reactive({
  account: '',
  password: '',
})

const formRef = ref()

const rules = {
  account: [{ required: true, message: '請輸入帳號', trigger: 'blur' }],
  password: [{ required: true, message: '請輸入密碼', trigger: 'blur' }],
}

async function handleLogin() {
  try {
    await formRef.value?.validate()
  } catch {
    return
  }

  try {
    await authStore.login(form.account, form.password)
    const redirect = (route.query.redirect as string) || '/'
    router.push(redirect)
  } catch {
    ElMessage.error('帳號或密碼錯誤')
  }
}
</script>

<template>
  <div class="login-page" :style="{ backgroundImage: `url(${templeBg})` }">
    <div class="login-overlay"></div>

    <div class="login-content">
      <div class="brand">
        <div class="brand-row">
          <img :src="logoPic" alt="八卦禪寺" class="brand-logo" />
          <img :src="logoText" alt="八卦禪寺" class="brand-title-img" />
        </div>
        <div class="brand-subtitle-row">
          <img :src="logoWord" alt="信徒管理系統" class="brand-subtitle-img" />
        </div>
      </div>

      <div class="login-card">
        <h2 class="login-title">登入</h2>

        <el-form
          ref="formRef"
          :model="form"
          :rules="rules"
          label-position="top"
          @submit.prevent="handleLogin"
        >
          <el-form-item label="帳號" prop="account">
            <el-input
              v-model="form.account"
              size="large"
            />
          </el-form-item>

          <el-form-item prop="password">
            <template #label>
              <div class="password-label">
                <span>密碼</span>
                <el-link type="primary" :underline="false" class="forgot-link">
                  忘記密碼？
                </el-link>
              </div>
            </template>
            <el-input
              v-model="form.password"
              type="password"
              size="large"
              show-password
              @keyup.enter="handleLogin"
            />
          </el-form-item>

          <el-form-item class="login-btn-item">
            <el-button
              type="primary"
              size="large"
              class="login-btn"
              :loading="authStore.loading"
              @click="handleLogin"
            >
              登入
            </el-button>
          </el-form-item>
        </el-form>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.login-page {
  position: relative;
  min-height: 100vh;
  background: center/cover no-repeat;
  background-color: #3a3a3a;
  overflow: hidden;
}

.login-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.35);
  z-index: 0;
}

.login-content {
  position: relative;
  z-index: 1;
  display: flex;
  justify-content: space-between;
  align-items: center;
  min-height: 100vh;
  padding: 60px 80px;
  max-width: 1400px;
  margin: 0 auto;
}

.brand {
  margin-left: 80px;
}

.brand-row {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: -55px;
}

.brand-logo {
  width: 45px;
  height: 45px;
  position: relative;
  top: -8px;
  left: 25px;
}

.brand-title-img {
  height: 112px;
}

.brand-subtitle-row {
  padding-left: 140px;
}

.brand-subtitle-img {
  height: 112px;
}

.login-card {
  width: 400px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
  padding: 40px;

  :deep(.el-form-item__label) {
    display: flex;
    width: 100%;
  }

  :deep(.el-input__wrapper) {
    border-radius: 8px;
  }
}

.login-title {
  font-size: 28px;
  font-weight: bold;
  color: $temple-text-dark;
  margin-bottom: 28px;
}

.password-label {
  display: flex;
  justify-content: space-between;
  width: 100%;
}

.forgot-link {
  font-size: 12px;
}

.login-btn-item {
  margin-bottom: 0;

  :deep(.el-form-item__content) {
    justify-content: flex-end;
  }
}

.login-btn {
  margin-top: 8px;
  padding: 10px 32px;
  border-radius: 8px;
  background-color: $temple-gold-primary !important;
  border-color: $temple-gold-primary !important;

  &:hover,
  &:focus {
    background-color: $temple-gold-dark !important;
    border-color: $temple-gold-dark !important;
  }
}

@media (max-width: 900px) {
  .login-content {
    flex-direction: column;
    justify-content: center;
    gap: 40px;
    padding: 40px 24px;
  }

  .brand {
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  .brand-subtitle-row {
    padding-left: 0;
  }

  .login-card {
    width: 100%;
    max-width: 400px;
  }
}
</style>
