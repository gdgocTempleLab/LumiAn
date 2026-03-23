import apiClient from './client'
import type { LoginRequest, LoginResponse, User } from '@/types'

export function loginApi(data: LoginRequest) {
  return apiClient.post<LoginResponse>('/auth/login', data)
}

export function logoutApi() {
  return apiClient.post('/auth/logout')
}

export function getCurrentUser() {
  return apiClient.get<User>('/auth/me')
}
