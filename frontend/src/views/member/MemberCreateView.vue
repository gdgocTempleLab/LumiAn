<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import AppHeader from '@/components/layout/AppHeader.vue'
import PageTitleBar from '@/components/layout/PageTitleBar.vue'
import HouseholdForm from '@/components/member/HouseholdForm.vue'
import MemberCardList from '@/components/member/MemberCardList.vue'
import { useMemberStore } from '@/stores/member'
import type { CalendarType, MemberRole } from '@/types'

const router = useRouter()
const memberStore = useMemberStore()

const emptyAddress = {
  countyCode: '',
  countyName: '',
  districtCode: '',
  districtName: '',
  villageName: '',
  detail: '',
}

const householdData = reactive({
  phoneAreaCode: '',
  phoneNumber: '',
  mobile: '',
  sameAsRegistered: false,
  registeredAddress: { ...emptyAddress },
  residenceAddress: { ...emptyAddress },
})

const members = ref([
  {
    name: '',
    role: 'head' as MemberRole,
    birthday: {
      calendarType: 'solar' as CalendarType,
      year: undefined as number | undefined,
      month: undefined as number | undefined,
      day: undefined as number | undefined,
    },
  },
])

async function handleSave() {
  if (!members.value.some((m) => m.name)) {
    ElMessage.warning('請至少填寫一位戶員姓名')
    return
  }

  try {
    await memberStore.createHousehold({
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
    ElMessage.success('信徒資料建立成功')
    router.push('/')
  } catch {
    ElMessage.error('建立失敗，請稍後再試')
  }
}
</script>

<template>
  <div class="member-create-page">
    <AppHeader compact />
    <PageTitleBar
      title="建立信徒資料"
      @save="handleSave"
      :loading="memberStore.loading"
    />

    <main class="create-content">
      <div class="form-columns">
        <div class="column-left">
          <HouseholdForm v-model="householdData" />
        </div>

        <div class="column-right">
          <MemberCardList v-model="members" />
        </div>
      </div>
    </main>
  </div>
</template>

<style scoped lang="scss">
.member-create-page {
  min-height: 100vh;
  background: $temple-bg-cream;
}

.create-content {
  max-width: 1000px;
  margin: 0 auto;
  padding: 32px 40px;
}

.form-columns {
  display: flex;
  gap: 48px;
  justify-content: center;
}

.column-left {
  flex: 1;
}

.column-right {
  flex: 1;
  display: flex;
  justify-content: center;
}
</style>
