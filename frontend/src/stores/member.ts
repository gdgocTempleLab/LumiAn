import { defineStore } from 'pinia'
import { ref } from 'vue'
import * as memberApi from '@/api/member'
import type { Household, Member, HouseholdQueryParams } from '@/types'

// ─── 後端資料轉換 ─────────────────────────────────────────────

function adaptMember(m: Record<string, unknown>): Member {
  const bdStr = String(m.Gregorian_Birthday || '')
  const [y, mo, d] = bdStr.split('-').map(Number)
  return {
    id: m.Member_ID as number,
    householdId: m.Household_ID as number,
    name: String(m.name || ''),
    role: m.isHeadOfHousehold ? 'head' : 'member',
    birthday: {
      calendarType: 'solar',
      year: y || 0,
      month: mo || 0,
      day: d || 0,
    },
    createdAt: String(m.Profile_Creation_Time || ''),
    updatedAt: String(m.Profile_Update_Time || ''),
  }
}

function adaptHousehold(h: Record<string, unknown>): Household {
  const phone = String(h.phone || '')
  const dashIdx = phone.indexOf('-')
  const phoneAreaCode = dashIdx > -1 ? phone.substring(0, dashIdx) : ''
  const phoneNumber = dashIdx > -1 ? phone.substring(dashIdx + 1) : phone

  return {
    id: h.Household_ID as number,
    phoneAreaCode,
    phoneNumber,
    mobile: String(h.mobile || ''),
    registeredAddress: {
      countyCode: String(h.Postal_code || ''),
      countyName: '',
      districtCode: '',
      districtName: '',
      detail: String(h.Address || ''),
    },
    residenceAddress: {
      countyCode: String(h.Postal_code || ''),
      countyName: '',
      districtCode: '',
      districtName: '',
      detail: String(h.Address || ''),
    },
    sameAsRegistered: true,
    members: ((h.Members as unknown[]) || []).map((m) => adaptMember(m as Record<string, unknown>)),
    createdAt: '',
    updatedAt: '',
  }
}

// ─── Store ────────────────────────────────────────────────────

export const useMemberStore = defineStore('member', () => {
  const households = ref<Household[]>([])
  const currentHousehold = ref<Household | null>(null)
  const loading = ref(false)
  const totalCount = ref(0)

  // BEL-003: 查詢信徒資料
  async function searchHouseholds(params: HouseholdQueryParams) {
    loading.value = true
    try {
      const backendParams: Record<string, string> = {}
      if (params.searchMethod) {
        backendParams.searchMethod = params.searchMethod
      }
      if (params.searchText) {
        backendParams.searchText = params.searchText
      }

      const res = await memberApi.queryHouseholds(backendParams)
      const raw = (res.data.Data?.HouseholdList ?? []) as Record<string, unknown>[]
      households.value = raw.map(adaptHousehold)
      totalCount.value = households.value.length
    } finally {
      loading.value = false
    }
  }

  // 從已載入清單中找到指定戶口（後端無單筆查詢端點）
  async function loadHousehold(id: number | string) {
    const found = households.value.find((h) => String(h.id) === String(id))
    if (found) {
      currentHousehold.value = found
      return found
    }

    loading.value = true
    try {
      const res = await memberApi.getHouseholdDetail(id)
      const raw = res.data.Data?.Household as Record<string, unknown> | undefined
      if (!raw) return null

      const household = adaptHousehold(raw)
      currentHousehold.value = household
      return household
    } finally {
      loading.value = false
    }
  }

  // BEL-001-1 + BEL-001-2: 建立戶籍 + 戶員
  // 前端傳入 camelCase；轉換為後端 PascalCase
  async function createHousehold(data: Record<string, unknown>) {
    loading.value = true
    try {
      const phone = `${data.phoneAreaCode || ''}-${data.phoneNumber || ''}`
      const regAddr = (data.registeredAddress as Record<string, unknown>) || {}

      // 自動產生 Household_ID（以手機 + 時間戳）
      const mobile = String(data.mobile || '').replace(/\D/g, '')
      const householdId = `H${mobile || Date.now()}`

      await memberApi.createHousehold({
        Household_ID: householdId,
        Postal_code: regAddr.countyCode || '',
        Address: `${regAddr.countyName || ''}${regAddr.districtName || ''}${regAddr.detail || ''}`,
        phone,
        mobile: String(data.mobile || ''),
      })

      // 建立戶員
      const members = (data.members as unknown[]) || []
      for (let i = 0; i < members.length; i++) {
        const m = members[i] as Record<string, unknown>
        const bd = (m.birthday as Record<string, unknown>) || {}
        const memberId = `${householdId}M${i + 1}`
        const bdStr = `${bd.year || 2000}-${String(bd.month || 1).padStart(2, '0')}-${String(bd.day || 1).padStart(2, '0')}`
        await memberApi.createMember({
          Member_ID: memberId,
          Household_ID: householdId,
          name: m.name,
          Lunar_Birthday: bdStr,
          Gregorian_Birthday: bdStr,
          isHeadOfHousehold: m.role === 'head',
        })
      }
    } finally {
      loading.value = false
    }
  }

  // BEL-002-1: 更新戶籍基本資料
  async function updateHousehold(id: number | string, data: Record<string, unknown>) {
    loading.value = true
    try {
      const phone = data.phoneAreaCode && data.phoneNumber
        ? `${data.phoneAreaCode}-${data.phoneNumber}`
        : undefined
      const regAddr = (data.registeredAddress as Record<string, unknown>) || {}

      await memberApi.updateHousehold({
        Household_ID: id,
        ...(phone ? { phone } : {}),
        ...(data.mobile !== undefined ? { mobile: data.mobile } : {}),
        ...(regAddr.countyCode ? { Postal_code: regAddr.countyCode } : {}),
        ...(regAddr.detail ? {
          Address: `${regAddr.countyName || ''}${regAddr.districtName || ''}${regAddr.detail}`,
        } : {}),
      })
    } finally {
      loading.value = false
    }
  }

  // BEL-002-3: 刪除戶籍
  async function removeHousehold(id: number | string) {
    loading.value = true
    try {
      await memberApi.deleteHousehold(id)
      households.value = households.value.filter((h) => String(h.id) !== String(id))
      if (String(currentHousehold.value?.id) === String(id)) {
        currentHousehold.value = null
      }
    } finally {
      loading.value = false
    }
  }

  // BEL-001-2: 新增戶員到現有戶籍
  async function addMemberToHousehold(householdId: number | string, data: Record<string, unknown>) {
    const bd = (data.birthday as Record<string, unknown>) || {}
    const bdStr = `${bd.year || 2000}-${String(bd.month || 1).padStart(2, '0')}-${String(bd.day || 1).padStart(2, '0')}`
    const memberId = `${householdId}M${Date.now()}`
    await memberApi.createMember({
      Member_ID: memberId,
      Household_ID: householdId,
      name: data.name,
      Lunar_Birthday: bdStr,
      Gregorian_Birthday: bdStr,
      isHeadOfHousehold: data.role === 'head',
    })
  }

  // BEL-002-2: 更新戶員資料
  async function updateMember(memberId: number | string, householdId: number | string, data: Record<string, unknown>) {
    const bd = (data.birthday as Record<string, unknown>) || {}
    const bdStr = bd.year
      ? `${bd.year}-${String(bd.month || 1).padStart(2, '0')}-${String(bd.day || 1).padStart(2, '0')}`
      : undefined

    await memberApi.updateMember({
      Member_ID: memberId,
      Household_ID: householdId,
      ...(data.name ? { name: data.name } : {}),
      ...(bdStr ? { Gregorian_Birthday: bdStr, Lunar_Birthday: bdStr } : {}),
      ...(data.role !== undefined ? { isHeadOfHousehold: data.role === 'head' } : {}),
    })
  }

  // BEL-002-4: 刪除戶員
  async function removeMember(memberId: number | string, householdId: number | string) {
    await memberApi.deleteMember(memberId, householdId)
  }

  function clearCurrent() {
    currentHousehold.value = null
  }

  return {
    households,
    currentHousehold,
    loading,
    totalCount,
    searchHouseholds,
    loadHousehold,
    createHousehold,
    updateHousehold,
    removeHousehold,
    addMemberToHousehold,
    updateMember,
    removeMember,
    clearCurrent,
  }
})
