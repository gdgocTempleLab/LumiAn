import apiClient from './client'
import type { BackendResponse } from '@/types/api'

// LGT-001: 查詢點燈紀錄 → GET api/light/search/
export function searchLightingRecords(params: {
  phone?: string
  head_name?: string
  year?: number
  is_paid?: boolean
}) {
  return apiClient.get<BackendResponse>('/light/search/', { params })
}

// LGT-002: 查詢指定信徒所有燈種狀態 → GET api/light/member-status/:member_id/
export function getMemberLightingStatus(memberId: string | number, year?: number) {
  return apiClient.get<BackendResponse>(`/light/member-status/${memberId}/`, {
    params: year ? { year } : undefined,
  })
}

// 建立點燈紀錄 → POST api/light/create/
export function createLightingRecord(data: Record<string, unknown>) {
  return apiClient.post<BackendResponse>('/light/create/', { Data: data })
}

// 編輯點燈紀錄 → PUT api/light/update/:lighting_record_id/
export function updateLightingRecord(recordId: string | number, data: Record<string, unknown>) {
  return apiClient.put<BackendResponse>(`/light/update/${recordId}/`, { Data: data })
}

// 刪除點燈紀錄 → DELETE api/light/delete/:lighting_record_id/
export function deleteLightingRecord(recordId: string | number, memberId: string | number) {
  return apiClient.delete<BackendResponse>(`/light/delete/${recordId}/`, {
    data: { Data: { Member_ID: memberId } },
  })
}

// 計算點燈費用 → POST api/light/calculate-fee/
export function calculateLightingFee(lightingRecordIds: (string | number)[]) {
  return apiClient.post<BackendResponse>('/light/calculate-fee/', {
    Data: { Lighting_Record_IDs: lightingRecordIds },
  })
}

// 建立繳費紀錄 → POST api/light/payment/create/
export function createLightingPayment(data: Record<string, unknown>) {
  return apiClient.post<BackendResponse>('/light/payment/create/', { Data: data })
}

// 匯出點燈清冊 → GET api/light/export-inventory/
export function exportLightingInventory(params: { year?: number; lamp_type?: string }) {
  return apiClient.get<BackendResponse>('/light/export-inventory/', { params })
}

// 燈條列印預覽 → GET api/light/print/preview/
export function getLightStripPreview(params: { year?: number; lamp_type?: string }) {
  return apiClient.get<BackendResponse>('/light/print/preview/', { params })
}

// 確認列印並更新狀態 → POST api/light/print/confirm/
export function confirmLightStripPrint(data: Record<string, unknown>) {
  return apiClient.post<BackendResponse>('/light/print/confirm/', { Data: data })
}
