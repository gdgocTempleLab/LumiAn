import { defineStore } from 'pinia'
import { ref } from 'vue'
import * as lampApi from '@/api/lamp'
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
} from '@/types'

// ─── 後端資料轉換 ─────────────────────────────────────────────

function adaptRecord(r: Record<string, unknown>): LampRecord {
  return {
    id: r.Lighting_Record_ID as number,
    householdId: r.Household_ID as number,
    memberId: r.Member_ID as number,
    memberName: String(r.Member_Name || ''),
    lampType: String(r.Lamp_Type || ''),
    year: Number(r.Year || 0),
    isPaid: Boolean(r.Is_Paid),
    amount: Number(r.Amount || 0),
    notes: String(r.Notes || ''),
    createdAt: String(r.Record_Creation_Time || ''),
    updatedAt: String(r.Record_Updated_Time || ''),
  }
}

function adaptRosterEntry(r: Record<string, unknown>): LampRosterEntry {
  return {
    memberName: String(r.Member_Name || r.member_name || ''),
    lampType: String(r.Lamp_Type || r.lamp_type || ''),
    year: Number(r.Year || r.year || 0),
    isPaid: Boolean(r.Is_Paid ?? r.is_paid),
    amount: Number(r.Amount || r.amount || 0),
    householdPhone: String(r.Phone || r.phone || ''),
  }
}

function adaptStripEntry(r: Record<string, unknown>): LampStripEntry {
  return {
    memberName: String(r.Member_Name || r.member_name || ''),
    lampType: String(r.Lamp_Type || r.lamp_type || ''),
    year: Number(r.Year || r.year || 0),
  }
}

// ─── Store ────────────────────────────────────────────────────

export const useLampStore = defineStore('lamp', () => {
  const lampRecords = ref<LampRecord[]>([])
  const householdLamps = ref<HouseholdLampSummary | null>(null)
  const lampHistory = ref<LampRecord[]>([])
  const rosterData = ref<LampRosterEntry[]>([])
  const stripData = ref<LampStripEntry[]>([])
  const selectedYear = ref<number>(new Date().getFullYear())
  const loading = ref(false)
  const totalCount = ref(0)

  // LGT-001: 查詢點燈紀錄（依條件）
  async function queryLamps(params: LampQueryParams) {
    loading.value = true
    try {
      const res = await lampApi.searchLightingRecords({
        year: params.year,
        phone: undefined,
      })
      const raw = (res.data.Data ?? []) as Record<string, unknown>[]
      lampRecords.value = raw.map(adaptRecord)
      totalCount.value = lampRecords.value.length
    } finally {
      loading.value = false
    }
  }

  // LGT-002: 取得指定戶口的所有燈種狀態
  // phone 參數用於過濾該戶口的紀錄（後端無單一戶口查詢端點）
  async function loadHouseholdLamps(householdId: number | string, phone?: string) {
    loading.value = true
    try {
      const res = await lampApi.searchLightingRecords({
        year: selectedYear.value,
        ...(phone ? { phone } : {}),
      })
      const raw = (res.data.Data ?? []) as Record<string, unknown>[]
      const all = raw.map(adaptRecord)

      const memberMap = new Map<number, { memberName: string; lamps: LampRecord[] }>()
      for (const r of all) {
        if (!memberMap.has(r.memberId)) {
          memberMap.set(r.memberId, { memberName: r.memberName, lamps: [] })
        }
        memberMap.get(r.memberId)!.lamps.push(r)
      }

      householdLamps.value = {
        householdId: householdId as number,
        phone: phone ?? '',
        mobile: '',
        members: Array.from(memberMap.entries()).map(([memberId, v]) => ({
          memberId,
          memberName: v.memberName,
          lamps: v.lamps,
        })),
      }
    } finally {
      loading.value = false
    }
  }

  // 更新點燈紀錄
  async function saveLampRecord(id: number | string, data: UpdateLampPayload) {
    await lampApi.updateLightingRecord(id, {
      ...(data.lampType !== undefined ? { Lamp_Type: data.lampType } : {}),
      ...(data.year !== undefined ? { Year: data.year } : {}),
      ...(data.amount !== undefined ? { Amount: data.amount } : {}),
      ...(data.isPaid !== undefined ? { Is_Paid: data.isPaid } : {}),
      ...(data.notes !== undefined ? { Notes: data.notes } : {}),
    })
  }

  // 建立點燈紀錄
  async function createLamp(data: CreateLampPayload) {
    await lampApi.createLightingRecord({
      Household_ID: data.householdId,
      Member_ID: data.memberId,
      Lamp_Type: data.lampType,
      Year: data.year,
      Amount: data.amount,
      Is_Paid: data.isPaid,
      Notes: data.notes ?? '',
    })
  }

  // 歷史紀錄（使用全域搜尋，依年份過濾）
  async function loadLampHistory(householdId: number | string) {
    try {
      const res = await lampApi.searchLightingRecords({})
      const raw = (res.data.Data ?? []) as Record<string, unknown>[]
      lampHistory.value = raw.map(adaptRecord)
    } catch {
      lampHistory.value = []
    }
  }

  // 清冊查詢（用於 LampRosterView / LampPrintFormView / LampExportView）
  async function loadRoster(params: RosterQueryParams) {
    loading.value = true
    try {
      const res = await lampApi.searchLightingRecords({
        year: params.year,
      })
      const raw = (res.data.Data ?? []) as Record<string, unknown>[]
      rosterData.value = raw.map(adaptRosterEntry)
      totalCount.value = rosterData.value.length
    } finally {
      loading.value = false
    }
  }

  // 燈條預覽（用於 LampStripView / LampPrintStripView）
  async function loadStrips(params: StripQueryParams) {
    loading.value = true
    try {
      const res = await lampApi.getLightStripPreview({
        year: params.year,
        lamp_type: params.lampType,
      })
      const raw = (res.data.Data ?? []) as Record<string, unknown>[]
      stripData.value = raw.map(adaptStripEntry)
    } finally {
      loading.value = false
    }
  }

  // 匯出清冊（用於 LampExportView）
  async function exportRoster(params: ExportParams): Promise<Blob> {
    const res = await lampApi.exportLightingInventory({
      year: params.year,
      lamp_type: params.lampType,
    })
    return res.data as unknown as Blob
  }

  // 刪除點燈紀錄
  async function deleteLamp(recordId: number | string, memberId: number | string) {
    await lampApi.deleteLightingRecord(recordId, memberId)
    lampRecords.value = lampRecords.value.filter((r) => String(r.id) !== String(recordId))
  }

  // 計算費用
  async function calculateFee(recordIds: (number | string)[]) {
    const res = await lampApi.calculateLightingFee(recordIds)
    return res.data.Data
  }

  // 建立繳費紀錄
  async function createPayment(data: Record<string, unknown>) {
    await lampApi.createLightingPayment(data)
  }

  // 確認列印
  async function confirmPrint(data: Record<string, unknown>) {
    await lampApi.confirmLightStripPrint(data)
  }

  return {
    lampRecords,
    householdLamps,
    lampHistory,
    rosterData,
    stripData,
    selectedYear,
    loading,
    totalCount,
    queryLamps,
    loadHouseholdLamps,
    saveLampRecord,
    createLamp,
    loadLampHistory,
    loadRoster,
    loadStrips,
    exportRoster,
    deleteLamp,
    calculateFee,
    createPayment,
    confirmPrint,
  }
})
