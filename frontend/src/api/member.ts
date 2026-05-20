import apiClient from './client'
import type { BackendResponse } from '@/types/api'

// BEL-003: 查詢信徒資料 → GET api/bel/search/
// 後端接受: searchMethod, searchText
export function queryHouseholds(params: {
  searchMethod?: string
  searchText?: string
}) {
  return apiClient.get<BackendResponse<{ HouseholdList: unknown[] }>>('/bel/search/', { params })
}

// BEL-002-1: 取得戶籍詳細資料 → GET api/bel/household/<householdId>/
export function getHouseholdDetail(householdId: string | number) {
  return apiClient.get<BackendResponse<{ Household: unknown }>>(`/bel/household/${householdId}/`)
}

// BEL-001-1: 建立戶籍資料 → POST api/bel/household/create/
// 必填: Household_ID, Postal_code, Address, phone
export function createHousehold(data: Record<string, unknown>) {
  return apiClient.post<BackendResponse>('/bel/household/create/', { Data: data })
}

// BEL-002-1: 更新戶籍基本資料 → PUT api/bel/household/update/
// 必填: Household_ID；選填: Postal_code, Address, phone
export function updateHousehold(data: Record<string, unknown>) {
  return apiClient.put<BackendResponse>('/bel/household/update/', { Data: data })
}

// BEL-002-3: 刪除戶籍資料 → DELETE api/bel/household/delete/
export function deleteHousehold(householdId: string | number) {
  return apiClient.delete<BackendResponse>('/bel/household/delete/', {
    data: { Data: { Household_ID: householdId } },
  })
}

// BEL-001-2: 新增戶員資料 → POST api/bel/member/create/
// 必填: Member_ID, Household_ID, name, Lunar_Birthday, Gregorian_Birthday
export function createMember(data: Record<string, unknown>) {
  return apiClient.post<BackendResponse>('/bel/member/create/', { Data: data })
}

// BEL-002-2: 更新戶員資料 → PUT api/bel/member/update/
// 必填: Member_ID, Household_ID；選填: name, Lunar_Birthday, Gregorian_Birthday, isHeadOfHousehold
export function updateMember(data: Record<string, unknown>) {
  return apiClient.put<BackendResponse>('/bel/member/update/', { Data: data })
}

// BEL-002-4: 刪除戶員資料 → DELETE api/bel/member/delete/
export function deleteMember(memberId: string | number, householdId: string | number) {
  return apiClient.delete<BackendResponse>('/bel/member/delete/', {
    data: { Data: { Member_ID: memberId, Household_ID: householdId } },
  })
}
