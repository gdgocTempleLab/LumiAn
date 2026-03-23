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
  token: string
  user: User
}
