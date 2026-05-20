import apiClient from './client'
import type { BackendResponse } from '@/types/api'

// DON-001-01: 檢查捐贈信息（名字 + 生日是否為既有信徒）→ POST api/don/check/
export function checkDonationBeliever(believerName: string, gregorianBirthday: string) {
  return apiClient.post<BackendResponse<{
    Exists: boolean
    Believer?: {
      Member_ID: string
      Believer_Name: string
      Gregorian_Birthday: string
      Household_ID: string
    }
  }>>('/don/check/', {
    Data: {
      Believer_Name: believerName,
      Gregorian_Birthday: gregorianBirthday,
    },
  })
}

// DON-001-02: 新增捐贈紀錄 → POST api/don/create/
export function createDonationRecord(data: {
  Believer_Name: string
  Gregorian_Birthday: string
  Donation_Amount: number
  Donation_Date: string
}) {
  return apiClient.post<BackendResponse>('/don/create/', { Data: data })
}
