<script setup lang="ts">
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import AppHeader from '@/components/layout/AppHeader.vue'
import PageTitleBar from '@/components/layout/PageTitleBar.vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

const form = reactive({
  currentPassword: '',
  newPassword: '',
  confirmPassword: '',
})

const formRef = ref()

const rules = {
  currentPassword: [{ required: true, message: '請輸入目前密碼', trigger: 'blur' }],
  newPassword: [
    { required: true, message: '請輸入新密碼', trigger: 'blur' },
    { min: 6, message: '密碼至少 6 個字元', trigger: 'blur' },
  ],
  confirmPassword: [
    { required: true, message: '請確認新密碼', trigger: 'blur' },
    {
      validator: (_rule: unknown, value: string, callback: (err?: Error) => void) => {
        if (value !== form.newPassword) {
          callback(new Error('兩次輸入的密碼不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur',
    },
  ],
}

async function handleSave() {
  try {
    await formRef.value?.validate()
  } catch {
    return
  }
  // Mock: 密碼變更成功
  ElMessage.success('密碼變更成功')
  form.currentPassword = ''
  form.newPassword = ''
  form.confirmPassword = ''
}
</script>

<template>
  <div class="account-manage-page">
    <AppHeader compact />
    <PageTitleBar title="帳號管理" :show-save="false" :show-cancel="false" />

    <main class="account-content">
      <div class="account-card">
        <div class="user-info">
          <h3>帳號資訊</h3>
          <p>帳號：{{ authStore.user?.account || 'admin' }}</p>
          <p>姓名：{{ authStore.user?.name || '管理員' }}</p>
          <p>角色：{{ authStore.user?.role === 'admin' ? '管理員' : '一般使用者' }}</p>
        </div>

        <el-divider />

        <h3 class="section-title">變更密碼</h3>
        <el-form
          ref="formRef"
          :model="form"
          :rules="rules"
          label-width="120px"
          class="password-form"
        >
          <el-form-item label="目前密碼" prop="currentPassword">
            <el-input v-model="form.currentPassword" type="password" show-password />
          </el-form-item>
          <el-form-item label="新密碼" prop="newPassword">
            <el-input v-model="form.newPassword" type="password" show-password />
          </el-form-item>
          <el-form-item label="確認新密碼" prop="confirmPassword">
            <el-input v-model="form.confirmPassword" type="password" show-password />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSave">儲存變更</el-button>
          </el-form-item>
        </el-form>
      </div>
    </main>
  </div>
</template>

<style scoped lang="scss">
.account-manage-page { min-height: 100vh; background: $temple-bg-cream; }
.account-content { max-width: 600px; margin: 0 auto; padding: 32px 40px; }

.account-card {
  background: white;
  border: 1px solid $temple-border-light;
  border-radius: 8px;
  padding: 32px;
}

.user-info {
  h3 { margin-bottom: 12px; }
  p { color: $temple-text-muted; margin-bottom: 4px; }
}

.section-title {
  margin-bottom: 20px;
}

.password-form {
  max-width: 400px;
}
</style>
