import apiClient from './client'
import type {
  Household,
  CreateHouseholdPayload,
  UpdateHouseholdPayload,
  CreateMemberPayload,
  UpdateMemberPayload,
  HouseholdQueryParams,
  PaginatedResponse,
  ApiResponse,
} from '@/types'

export function queryHouseholds(params: HouseholdQueryParams) {
  return apiClient.get<PaginatedResponse<Household>>('/households', { params })
}

export function getHousehold(id: number) {
  return apiClient.get<ApiResponse<Household>>(`/households/${id}`)
}

export function createHousehold(data: CreateHouseholdPayload) {
  return apiClient.post<ApiResponse<Household>>('/households', data)
}

export function updateHousehold(id: number, data: UpdateHouseholdPayload) {
  return apiClient.put<ApiResponse<Household>>(`/households/${id}`, data)
}

export function deleteHousehold(id: number) {
  return apiClient.delete<ApiResponse<null>>(`/households/${id}`)
}

export function addMember(householdId: number, data: CreateMemberPayload) {
  return apiClient.post<ApiResponse<null>>(`/households/${householdId}/members`, data)
}

export function updateMember(id: number, data: UpdateMemberPayload) {
  return apiClient.put<ApiResponse<null>>(`/members/${id}`, data)
}

export function deleteMember(id: number) {
  return apiClient.delete<ApiResponse<null>>(`/members/${id}`)
}
