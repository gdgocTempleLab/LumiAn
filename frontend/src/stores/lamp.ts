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

export const useLampStore = defineStore('lamp', () => {
  const lampRecords = ref<LampRecord[]>([])
  const householdLamps = ref<HouseholdLampSummary | null>(null)
  const lampHistory = ref<LampRecord[]>([])
  const rosterData = ref<LampRosterEntry[]>([])
  const stripData = ref<LampStripEntry[]>([])
  const selectedYear = ref<number>(new Date().getFullYear())
  const loading = ref(false)
  const totalCount = ref(0)

  async function queryLamps(params: LampQueryParams) {
    loading.value = true
    try {
      const res = await lampApi.queryLamps(params)
      lampRecords.value = res.data.data
      totalCount.value = res.data.total
    } finally {
      loading.value = false
    }
  }

  async function loadHouseholdLamps(householdId: number) {
    loading.value = true
    try {
      const res = await lampApi.getHouseholdLamps(householdId, selectedYear.value)
      householdLamps.value = res.data.data
    } finally {
      loading.value = false
    }
  }

  async function saveLampRecord(id: number, data: UpdateLampPayload) {
    await lampApi.updateLampRecord(id, data)
  }

  async function createLamp(data: CreateLampPayload) {
    await lampApi.createLampRecord(data)
  }

  async function loadLampHistory(householdId: number) {
    const res = await lampApi.getLampHistory(householdId)
    lampHistory.value = res.data.data
  }

  async function loadRoster(params: RosterQueryParams) {
    loading.value = true
    try {
      const res = await lampApi.getLampRoster(params)
      rosterData.value = res.data.data
      totalCount.value = res.data.total
    } finally {
      loading.value = false
    }
  }

  async function loadStrips(params: StripQueryParams) {
    loading.value = true
    try {
      const res = await lampApi.getLampStrips(params)
      stripData.value = res.data.data
    } finally {
      loading.value = false
    }
  }

  async function exportRoster(params: ExportParams): Promise<Blob> {
    const res = await lampApi.exportLampRoster(params)
    return res.data as Blob
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
  }
})
