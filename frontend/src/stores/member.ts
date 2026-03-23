import { defineStore } from 'pinia'
import { ref } from 'vue'
import * as memberApi from '@/api/member'
import type {
  Household,
  CreateHouseholdPayload,
  UpdateHouseholdPayload,
  CreateMemberPayload,
  UpdateMemberPayload,
  HouseholdQueryParams,
} from '@/types'

export const useMemberStore = defineStore('member', () => {
  const households = ref<Household[]>([])
  const currentHousehold = ref<Household | null>(null)
  const loading = ref(false)
  const totalCount = ref(0)

  async function searchHouseholds(params: HouseholdQueryParams) {
    loading.value = true
    try {
      const res = await memberApi.queryHouseholds(params)
      households.value = res.data.data
      totalCount.value = res.data.total
    } finally {
      loading.value = false
    }
  }

  async function loadHousehold(id: number) {
    loading.value = true
    try {
      const res = await memberApi.getHousehold(id)
      currentHousehold.value = res.data.data
    } finally {
      loading.value = false
    }
  }

  async function createHousehold(data: CreateHouseholdPayload) {
    loading.value = true
    try {
      await memberApi.createHousehold(data)
    } finally {
      loading.value = false
    }
  }

  async function updateHousehold(id: number, data: UpdateHouseholdPayload) {
    loading.value = true
    try {
      await memberApi.updateHousehold(id, data)
    } finally {
      loading.value = false
    }
  }

  async function removeHousehold(id: number) {
    loading.value = true
    try {
      await memberApi.deleteHousehold(id)
      households.value = households.value.filter((h) => h.id !== id)
    } finally {
      loading.value = false
    }
  }

  async function addMemberToHousehold(householdId: number, data: CreateMemberPayload) {
    await memberApi.addMember(householdId, data)
  }

  async function updateMember(id: number, data: UpdateMemberPayload) {
    await memberApi.updateMember(id, data)
  }

  async function removeMember(id: number) {
    await memberApi.deleteMember(id)
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
