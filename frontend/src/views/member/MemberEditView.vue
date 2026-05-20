<script setup lang="ts">
import { computed, reactive, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Phone } from '@element-plus/icons-vue'
import AppHeader from '@/components/layout/AppHeader.vue'
import PageTitleBar from '@/components/layout/PageTitleBar.vue'
import HouseholdForm from '@/components/member/HouseholdForm.vue'
import MemberCardList from '@/components/member/MemberCardList.vue'
import { useMemberStore } from '@/stores/member'
import type { CalendarType, MemberRole } from '@/types'

type AddressForm = {
  countyCode: string
  countyName: string
  districtCode: string
  districtName: string
  villageName: string
  detail: string
}

type EditableMember = {
  memberId?: string
  name: string
  role: MemberRole
  birthday: {
    calendarType: CalendarType
    year: number | undefined
    month: number | undefined
    day: number | undefined
  }
}

const route = useRoute()
const router = useRouter()
const memberStore = useMemberStore()

const emptyAddress: AddressForm = {
  countyCode: '',
  countyName: '',
  districtCode: '',
  districtName: '',
  villageName: '',
  detail: '',
}

const householdId = ref('')
const pageReady = ref(false)

const householdData = reactive({
  phoneAreaCode: '',
  phoneNumber: '',
  mobile: '',
  sameAsRegistered: false,
  registeredAddress: { ...emptyAddress },
  residenceAddress: { ...emptyAddress },
})

const members = ref<EditableMember[]>([createEmptyMember()])
const originalMemberIds = ref<string[]>([])

function createEmptyMember(role: MemberRole = 'member', memberId = ''): EditableMember {
  return {
    memberId,
    name: '',
    role,
    birthday: {
      calendarType: 'solar',
      year: undefined,
      month: undefined,
      day: undefined,
    },
  }
}

function cloneAddress(source?: Partial<AddressForm> | null): AddressForm {
  return {
    countyCode: source?.countyCode || '',
    countyName: source?.countyName || '',
    districtCode: source?.districtCode || '',
    districtName: source?.districtName || '',
    villageName: source?.villageName || '',
    detail: source?.detail || '',
  }
}

function applyHouseholdData() {
  const current = memberStore.currentHousehold
  if (!current) return false

  householdId.value = String(current.id)
  householdData.phoneAreaCode = current.phoneAreaCode
  householdData.phoneNumber = current.phoneNumber
  householdData.mobile = current.mobile
  householdData.sameAsRegistered = current.sameAsRegistered
  householdData.registeredAddress = cloneAddress(current.registeredAddress)
  householdData.residenceAddress = cloneAddress(current.residenceAddress)

  const nextMembers = current.members.length > 0
    ? current.members.map((m) => ({
        memberId: String(m.id),
        name: m.name,
        role: m.role,
        birthday: {
          calendarType: m.birthday.calendarType,
          year: m.birthday.year,
          month: m.birthday.month,
          day: m.birthday.day,
        },
      }))
    : [createEmptyMember()]

  members.value = nextMembers
  originalMemberIds.value = current.members.map((m) => String(m.id))
  pageReady.value = true
  return true
}

async function loadHousehold() {
  pageReady.value = false

  const householdIdParam = Array.isArray(route.params.householdId)
    ? route.params.householdId[0]
    : route.params.householdId

  const targetId = householdIdParam || memberStore.currentHousehold?.id
  if (!targetId) {
    ElMessage.error('缺少戶口編號，無法載入編輯頁面')
    router.push({ name: 'MemberList' })
    return
  }

  const loaded = await memberStore.loadHousehold(targetId)
  if (!loaded) {
    ElMessage.error('找不到指定戶口資料')
    router.push({ name: 'MemberList' })
    return
  }

  applyHouseholdData()
}

watch(
  () => route.params.householdId,
  () => {
    void loadHousehold()
  },
  { immediate: true },
)

const headName = computed(() => members.value.find((m) => m.role === 'head')?.name || '-')

function getHouseholdAddressText() {
  const addr = householdData.registeredAddress
  return `${addr.countyName}${addr.districtName}${addr.villageName || ''}${addr.detail}` || '-'
}

async function handleSave() {
  if (!householdId.value) return

  const submittedMembers = members.value.filter((member) => member.name.trim())
  if (submittedMembers.length === 0) {
    ElMessage.warning('請至少保留一位戶員資料')
    return
  }

  const hasInvalidMember = submittedMembers.some((member) => {
    const birthday = member.birthday
    return !member.name.trim() || !birthday.year || !birthday.month || !birthday.day
  })
  if (hasInvalidMember) {
    ElMessage.warning('請完整填寫所有戶員姓名與誕辰資料')
    return
  }

  try {
    await memberStore.updateHousehold(householdId.value, {
      phoneAreaCode: householdData.phoneAreaCode,
      phoneNumber: householdData.phoneNumber,
      mobile: householdData.mobile,
      sameAsRegistered: householdData.sameAsRegistered,
      registeredAddress: {
        countyCode: householdData.registeredAddress.countyCode,
        countyName: householdData.registeredAddress.countyName,
        districtCode: householdData.registeredAddress.districtCode,
        districtName: householdData.registeredAddress.districtName,
        villageName: householdData.registeredAddress.villageName,
        detail: householdData.registeredAddress.detail,
      },
      residenceAddress: {
        countyCode: householdData.residenceAddress.countyCode,
        countyName: householdData.residenceAddress.countyName,
        districtCode: householdData.residenceAddress.districtCode,
        districtName: householdData.residenceAddress.districtName,
        villageName: householdData.residenceAddress.villageName,
        detail: householdData.residenceAddress.detail,
      },
    })

    const currentIds = new Set(submittedMembers.map((member) => member.memberId).filter(Boolean) as string[])
    const removedIds = originalMemberIds.value.filter((id) => !currentIds.has(id))
    const nonHeads = submittedMembers.filter((member) => member.role !== 'head')
    const heads = submittedMembers.filter((member) => member.role === 'head')

    for (const memberId of removedIds) {
      await memberStore.removeMember(memberId, householdId.value)
    }

    const syncMember = async (member: EditableMember) => {
      const payload = {
        name: member.name,
        role: member.role,
        birthday: {
          calendarType: member.birthday.calendarType,
          year: member.birthday.year || 2000,
          month: member.birthday.month || 1,
          day: member.birthday.day || 1,
        },
      }

      if (member.memberId) {
        await memberStore.updateMember(member.memberId, householdId.value, payload)
      } else {
        await memberStore.addMemberToHousehold(householdId.value, payload)
      }
    }

    for (const member of nonHeads) {
      await syncMember(member)
    }
    for (const member of heads) {
      await syncMember(member)
    }

    await memberStore.loadHousehold(householdId.value)
    applyHouseholdData()
    ElMessage.success('更新成功')
  } catch {
    ElMessage.error('更新失敗')
  }
}

function handleCancel() {
  router.push({ name: 'MemberList' })
}
</script>

<template>
  <div class="member-edit-page">
    <AppHeader compact />
    <PageTitleBar
      title="編輯信徒資料"
      :show-save="true"
      :show-cancel="true"
      :save-disabled="!pageReady || memberStore.loading"
      :cancel-disabled="memberStore.loading"
      :cancel-go-back="false"
      :loading="memberStore.loading && !pageReady"
      @save="handleSave"
      @cancel="handleCancel"
    />

    <main class="edit-content">
      <section v-if="pageReady" class="summary-card">
        <div class="summary-item">
          <span class="summary-label">戶口編號</span>
          <strong>{{ householdId }}</strong>
        </div>
        <div class="summary-item">
          <span class="summary-label">戶長</span>
          <strong>{{ headName }}</strong>
        </div>
        <div class="summary-item">
          <span class="summary-label">戶員數</span>
          <strong>{{ members.length }}</strong>
        </div>
        <div class="summary-item summary-address">
          <span class="summary-label">地址</span>
          <strong>{{ getHouseholdAddressText() }}</strong>
        </div>
      </section>

      <section class="form-columns" v-loading="memberStore.loading && !pageReady">
        <div class="column-left">
          <div class="section-card">
            <div class="section-title-row">
              <h3 class="section-title"><el-icon><Phone /></el-icon> 戶籍資訊</h3>
              <span class="section-subtitle">可直接修改電話與地址</span>
            </div>
            <HouseholdForm v-model="householdData" />
          </div>
        </div>

        <div class="column-right">
          <div class="section-card">
            <div class="section-title-row">
              <h3 class="section-title"><el-icon><User /></el-icon> 戶員資料</h3>
              <span class="section-subtitle">可新增、刪除與修改戶長/戶員</span>
            </div>
            <MemberCardList v-model="members" />
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<style scoped lang="scss">
.member-edit-page {
  min-height: 100vh;
  background: $temple-bg-cream;
}

.edit-content {
  max-width: 1180px;
  margin: 0 auto;
  padding: 32px 40px 56px;
}

.summary-card,
.section-card {
  background: white;
  border: 1px solid $temple-border-light;
  border-radius: 12px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.03);
}

.summary-card {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 16px;
  padding: 18px 20px;
  margin-bottom: 20px;
}

.summary-item {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.summary-label,
.section-subtitle {
  font-size: 12px;
  color: $temple-text-muted;
}

.summary-address {
  grid-column: span 2;
}

.form-columns {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
  gap: 20px;
}

.section-card {
  padding: 20px;
}

.section-title-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 12px;
}

.section-title {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 16px;
  color: $temple-text-dark;
  margin: 0;
}

.column-left,
.column-right {
  min-width: 0;
}

@media (max-width: 960px) {
  .summary-card,
  .form-columns {
    grid-template-columns: 1fr;
  }

  .summary-address {
    grid-column: span 1;
  }
}
</style>
