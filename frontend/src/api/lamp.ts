import apiClient from './client'
import type {
  LampRecord,
  HouseholdLampSummary,
  LampRosterEntry,
  LampStripEntry,
  LampQueryParams,
  CreateLampPayload,
  UpdateLampPayload,
  RosterQueryParams,
  StripQueryParams,
  ExportParams,
  PaginatedResponse,
  ApiResponse,
} from '@/types'

export function queryLamps(params: LampQueryParams) {
  return apiClient.get<PaginatedResponse<LampRecord>>('/lamps', { params })
}

export function getHouseholdLamps(householdId: number, year?: number) {
  return apiClient.get<ApiResponse<HouseholdLampSummary>>(`/lamps/household/${householdId}`, {
    params: { year },
  })
}

export function createLampRecord(data: CreateLampPayload) {
  return apiClient.post<ApiResponse<LampRecord>>('/lamps', data)
}

export function updateLampRecord(id: number, data: UpdateLampPayload) {
  return apiClient.put<ApiResponse<LampRecord>>(`/lamps/${id}`, data)
}

export function getLampHistory(householdId: number) {
  return apiClient.get<ApiResponse<LampRecord[]>>(`/lamps/history/${householdId}`)
}

export function getLampRoster(params: RosterQueryParams) {
  return apiClient.get<PaginatedResponse<LampRosterEntry>>('/lamps/roster', { params })
}

export function getLampStrips(params: StripQueryParams) {
  return apiClient.get<ApiResponse<LampStripEntry[]>>('/lamps/strips', { params })
}

export function exportLampRoster(params: ExportParams) {
  return apiClient.get('/lamps/export', { params, responseType: 'blob' })
}
