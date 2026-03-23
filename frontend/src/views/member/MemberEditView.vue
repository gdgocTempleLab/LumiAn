<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Phone, Iphone, Location, Calendar, Plus, Minus } from '@element-plus/icons-vue'
import AppHeader from '@/components/layout/AppHeader.vue'
import PageTitleBar from '@/components/layout/PageTitleBar.vue'
import MemberSearchForm from '@/components/member/MemberSearchForm.vue'
import HouseholdTable from '@/components/member/HouseholdTable.vue'
import { useMemberStore } from '@/stores/member'
import type { Household, CalendarType, MemberRole } from '@/types'

const router = useRouter()
const memberStore = useMemberStore()
const searched = ref(false)
const editing = ref(false)

const emptyAddress = {
  countyCode: '', countyName: '', districtCode: '',
  districtName: '', villageName: '', detail: '',
}

const householdData = reactive({
  phoneAreaCode: '',
  phoneNumber: '',
  mobile: '',
  sameAsRegistered: false,
  registeredAddress: { ...emptyAddress },
  residenceAddress: { ...emptyAddress },
})

const members = ref<Array<{
  name: string
  role: MemberRole
  birthday: { calendarType: CalendarType; year: number | undefined; month: number | undefined; day: number | undefined }
}>>([])

let selectedId = 0

async function handleSearch(params: { searchMethod: string; searchText: string }) {
  await memberStore.searchHouseholds({
    searchMethod: params.searchMethod as 'phone' | 'name' | 'mobile',
    searchText: params.searchText,
  })
  searched.value = true
  editing.value = false
}

function handleSelect(household: Household) {
  selectedId = household.id
  householdData.phoneAreaCode = household.phoneAreaCode
  householdData.phoneNumber = household.phoneNumber
  householdData.mobile = household.mobile
  householdData.sameAsRegistered = household.sameAsRegistered
  householdData.registeredAddress = { ...household.registeredAddress }
  householdData.residenceAddress = { ...household.residenceAddress }

  members.value = household.members.map((m) => ({
    name: m.name,
    role: m.role,
    birthday: {
      calendarType: m.birthday.calendarType,
      year: m.birthday.year,
      month: m.birthday.month,
      day: m.birthday.day,
    },
  }))

  editing.value = true
}

function handleCancel() {
  editing.value = false
}

function addMember() {
  members.value.push({
    name: '',
    role: 'member',
    birthday: {
      calendarType: 'solar',
      year: undefined,
      month: undefined,
      day: undefined,
    },
  })
}

function removeMember() {
  if (members.value.length > 1) {
    members.value.pop()
  }
}

function getDisplayPhone() {
  if (householdData.phoneAreaCode && householdData.phoneNumber) {
    return `${householdData.phoneAreaCode}-${householdData.phoneNumber}`
  }
  return '-'
}

function getDisplayAddress() {
  const addr = householdData.registeredAddress
  return `${addr.countyName}${addr.districtName}${addr.villageName || ''}${addr.detail}`
}

function getDisplayBirthday(member: typeof members.value[0], type: 'solar' | 'lunar') {
  const b = member.birthday
  if (b.calendarType === type && b.year && b.month && b.day) {
    return `${b.year}/${String(b.month).padStart(2, '0')}/${String(b.day).padStart(2, '0')}`
  }
  return ''
}

function getRoleLabel(role: MemberRole) {
  return role === 'head' ? '戶長' : '戶員'
}

async function handleSave() {
  try {
    await memberStore.updateHousehold(selectedId, {
      phoneAreaCode: householdData.phoneAreaCode,
      phoneNumber: householdData.phoneNumber,
      mobile: householdData.mobile,
      sameAsRegistered: householdData.sameAsRegistered,
      registeredAddress: {
        countyCode: householdData.registeredAddress.countyCode,
        districtCode: householdData.registeredAddress.districtCode,
        detail: householdData.registeredAddress.detail,
      },
      residenceAddress: {
        countyCode: householdData.residenceAddress.countyCode,
        districtCode: householdData.residenceAddress.districtCode,
        detail: householdData.residenceAddress.detail,
      },
      members: members.value
        .filter((m) => m.name)
        .map((m) => ({
          name: m.name,
          role: m.role,
          birthday: {
            calendarType: m.birthday.calendarType,
            year: m.birthday.year || 2000,
            month: m.birthday.month || 1,
            day: m.birthday.day || 1,
          },
        })),
    })
    ElMessage.success('更新成功')
    router.push('/')
  } catch {
    ElMessage.error('更新失敗')
  }
}
</script>

<template>
  <div class="member-edit-page">
    <AppHeader compact />
    <PageTitleBar
      title="信徒資料"
      :show-save="true"
      :show-cancel="true"
      :save-disabled="!editing"
      :cancel-disabled="!editing"
      :cancel-go-back="false"
      :loading="memberStore.loading"
      @save="handleSave"
      @cancel="handleCancel"
    />

    <main class="edit-content">
      <MemberSearchForm @search="handleSearch" />

      <div v-if="searched" class="result-card">
        <h3 class="card-title">查詢結果（請選擇欲編輯之戶口）</h3>
        <HouseholdTable
          :data="memberStore.households"
          :loading="memberStore.loading"
          @select="handleSelect"
        />
      </div>

      <div v-if="editing" class="household-data-card">
        <div class="card-header-row">
          <h3 class="card-title">戶口資料</h3>
          <div class="card-actions">
            <el-button class="add-member-btn" @click="addMember">
              <el-icon><Plus /></el-icon> 新增戶員
            </el-button>
            <el-button class="remove-member-btn" @click="removeMember">
              <el-icon><Minus /></el-icon> 刪除戶員
            </el-button>
          </div>
        </div>

        <el-table :data="[householdData]" class="info-table">
          <el-table-column min-width="180">
            <template #header>
              <span class="column-header"><el-icon><Phone /></el-icon> 電話（市話）</span>
            </template>
            <template #default>
              {{ getDisplayPhone() }}
            </template>
          </el-table-column>
          <el-table-column min-width="160">
            <template #header>
              <span class="column-header"><el-icon><Iphone /></el-icon> 電話（手機）</span>
            </template>
            <template #default>
              {{ householdData.mobile || '-' }}
            </template>
          </el-table-column>
          <el-table-column min-width="300">
            <template #header>
              <span class="column-header"><el-icon><Location /></el-icon> 地址</span>
            </template>
            <template #default>
              {{ getDisplayAddress() }}
            </template>
          </el-table-column>
        </el-table>

        <el-table :data="members" class="info-table members-table">
          <el-table-column min-width="120">
            <template #header>
              <span class="column-header"><el-icon><User /></el-icon> 姓名</span>
            </template>
            <template #default="{ row }">
              {{ row.name || '-' }}
            </template>
          </el-table-column>
          <el-table-column min-width="100">
            <template #header>
              <span class="column-header"><el-icon><User /></el-icon> 身份</span>
            </template>
            <template #default="{ row }">
              {{ getRoleLabel(row.role) }}
            </template>
          </el-table-column>
          <el-table-column min-width="160">
            <template #header>
              <span class="column-header"><el-icon><Calendar /></el-icon> 國曆誕辰</span>
            </template>
            <template #default="{ row }">
              {{ getDisplayBirthday(row, 'solar') }}
            </template>
          </el-table-column>
          <el-table-column min-width="160">
            <template #header>
              <span class="column-header"><el-icon><Calendar /></el-icon> 農曆誕辰</span>
            </template>
            <template #default="{ row }">
              {{ getDisplayBirthday(row, 'lunar') }}
            </template>
          </el-table-column>
        </el-table>
      </div>
    </main>
  </div>
</template>

<style scoped lang="scss">
.member-edit-page {
  min-height: 100vh;
  background: $temple-bg-cream;
}

.edit-content {
  max-width: 1000px;
  margin: 0 auto;
  padding: 32px 40px;
}

.result-card {
  background: white;
  border: 1px solid $temple-border-light;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
}

.card-title {
  font-size: 16px;
  font-weight: bold;
  color: $temple-text-dark;
  margin-bottom: 16px;
}

.household-data-card {
  background: white;
  border: 1px solid $temple-border-light;
  border-radius: 8px;
  padding: 20px;
}

.card-header-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.card-actions {
  display: flex;
  gap: 8px;
}

.add-member-btn {
  color: $temple-gold-primary;
  border: 1px solid $temple-gold-primary;
  background: transparent;
  border-radius: 20px;

  &:hover,
  &:focus {
    color: $temple-gold-dark;
    border-color: $temple-gold-dark;
    background: transparent;
  }
}

.remove-member-btn {
  color: #F56C6C;
  border: 1px solid #F56C6C;
  background: transparent;
  border-radius: 20px;

  &:hover,
  &:focus {
    color: #e04040;
    border-color: #e04040;
    background: transparent;
  }
}

.info-table {
  margin-bottom: 0;

  :deep(.el-table__header th) {
    background: #fafafa;
    font-weight: normal;
    color: $temple-text-dark;
  }
}

.members-table {
  margin-top: 16px;
}

.column-header {
  display: inline-flex;
  align-items: center;
  gap: 4px;
}
</style>
