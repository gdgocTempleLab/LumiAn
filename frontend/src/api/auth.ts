import apiClient from './client'
import type { LoginResponse, AccountInfo } from '@/types'
import type { BackendResponse } from '@/types/api'

// SYS-001: 登入 → POST api/sys/login/
export function loginApi(account: string, password: string) {
  return apiClient.post<LoginResponse>('/sys/login/', {
    Data: { Account: account, Password: password },
  })
}

// SYS-002: 取得帳號列表 → GET api/sys/account/list/
export function getAccountListApi() {
  return apiClient.get<BackendResponse<{ AccountList: AccountInfo[] }>>('/sys/account/list/')
}

// SYS-003: 建立帳號 → POST api/sys/account/create/
export function createAccountApi(data: {
  Account: string
  Password: string
  Role: string
  Email: string
  Account_Status: string
}) {
  return apiClient.post<BackendResponse>('/sys/account/create/', { Data: data })
}

// SYS-004: 帳號詳情 → GET api/sys/account/detail/?id=...
export function getAccountDetailApi(id: number) {
  return apiClient.get<BackendResponse<AccountInfo>>('/sys/account/detail/', {
    params: { id },
  })
}

// SYS-005: 更新帳號 → PUT api/sys/account/update/
export function updateAccountApi(data: {
  Id: number
  Account?: string
  Role?: string
  Email?: string
  Account_Status?: string
}) {
  return apiClient.put<BackendResponse>('/sys/account/update/', { Data: data })
}

// SYS-006: 管理員重設密碼 → PUT api/sys/account/reset-password/
export function adminResetPasswordApi(id: number, newPassword: string) {
  return apiClient.put<BackendResponse>('/sys/account/reset-password/', {
    Data: { Id: id, New_Password: newPassword },
  })
}

// SYS-007: 更新個人資料 → PUT api/sys/profile/update/
export function updateProfileApi(data: { Account?: string; Email?: string }) {
  return apiClient.put<BackendResponse>('/sys/profile/update/', { Data: data })
}

// SYS-008: 修改密碼 → PUT api/sys/profile/change-password/
export function changePasswordApi(oldPassword: string, newPassword: string) {
  return apiClient.put<BackendResponse>('/sys/profile/change-password/', {
    Data: { Old_Password: oldPassword, New_Password: newPassword },
  })
}
