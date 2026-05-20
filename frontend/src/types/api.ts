export interface ApiResponse<T> {
  success: boolean
  data: T
  message?: string
}

export interface PaginatedResponse<T> {
  success: boolean
  data: T[]
  total: number
  page: number
  pageSize: number
}

export interface BackendResponse<T = unknown> {
  Status: 'Success' | 'Error'
  Message?: string
  Data?: T
}
