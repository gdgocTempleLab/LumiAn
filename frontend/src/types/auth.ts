export interface User {
  id: number
  account: string
  name: string
  role: 'admin' | 'user'
}

export interface LoginRequest {
  account: string
  password: string
}

export interface LoginResponse {
  Status: string
  Data: {
    AccessToken: string
  }
}

export interface AccountInfo {
  Id: number
  Account: string
  Role: string
  Email: string
  Account_Status: string
  Account_Creation_Time: string
  Account_Update_Time: string
}

export interface ChangePasswordRequest {
  currentPassword: string
  newPassword: string
}
