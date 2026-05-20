import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { loginApi } from '@/api/auth'
import type { User } from '@/types'

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(localStorage.getItem('auth_token'))
  const user = ref<User | null>(null)
  const loading = ref(false)

  const isAuthenticated = computed(() => !!token.value)

  async function login(account: string, password: string) {
    loading.value = true
    try {
      const res = await loginApi(account, password)
      const accessToken = res.data.Data?.AccessToken
      if (!accessToken) throw new Error('登入失敗')
      token.value = accessToken
      localStorage.setItem('auth_token', accessToken)
    } finally {
      loading.value = false
    }
  }

  function logout() {
    clearAuth()
  }

  function clearAuth() {
    token.value = null
    user.value = null
    localStorage.removeItem('auth_token')
  }

  return { token, user, loading, isAuthenticated, login, logout, clearAuth }
})
