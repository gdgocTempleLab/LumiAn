<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { Search } from '@element-plus/icons-vue'
import AppHeader from '@/components/layout/AppHeader.vue'
import PageTitleBar from '@/components/layout/PageTitleBar.vue'
import HouseholdTable from '@/components/member/HouseholdTable.vue'
import HouseholdLampInfoCard from '@/components/lamp/HouseholdLampInfoCard.vue'
import LampHistoryDialog from '@/components/lamp/LampHistoryDialog.vue'
import { useMemberStore } from '@/stores/member'
import { useLampStore } from '@/stores/lamp'
import type { Household } from '@/types'

const router = useRouter()
const memberStore = useMemberStore()
const lampStore = useLampStore()
const searched = ref(false)
const selectedHousehold = ref(false)
const historyVisible = ref(false)

const currentYear = new Date().getFullYear()
const year = ref(currentYear)
const years: number[] = []
for (let y = currentYear; y >= currentYear - 10; y--) years.push(y)

const form = reactive({ searchMethod: 'phone', searchText: '' })

const searchMethods = [
  { value: 'phone', label: '電話（市話）' },
  { value: 'mobile', label: '電話（手機）' },
  { value: 'name', label: '戶長姓名' },
]

const placeholders: Record<string, string> = {
  phone: '請輸入市話號碼',
  mobile: '請輸入手機號碼',
  name: '請輸入戶長姓名',
}

async function handleSearch() {
  lampStore.selectedYear = year.value
  await memberStore.searchHouseholds({
    searchMethod: form.searchMethod as 'phone' | 'name' | 'mobile',
    searchText: form.searchText,
  })
  searched.value = true
  selectedHousehold.value = false
}

async function handleSelect(household: Household) {
  lampStore.selectedYear = year.value
  await Promise.all([
    memberStore.loadHousehold(household.id),
    lampStore.loadHouseholdLamps(household.id),
  ])
  selectedHousehold.value = true
}

function handlePrint() {
  router.push('/lamp/print-form')
}

async function handleHistory() {
  if (memberStore.currentHousehold) {
    await lampStore.loadLampHistory(memberStore.currentHousehold.id)
  }
  historyVisible.value = true
}
</script>

<template>
  <div class="lamp-edit-list-page">
    <AppHeader compact />
    <PageTitleBar
      title="點燈紀錄"
      :show-save="true"
      :show-cancel="true"
      :save-disabled="true"
      :cancel-disabled="true"
    />

    <main class="list-content">
      <div class="search-card">
        <h3 class="card-title">選擇年份</h3>
        <el-select v-model="year" class="year-select">
          <el-option v-for="y in years" :key="y" :label="`${y}年`" :value="y" />
        </el-select>
      </div>

      <div class="search-card">
        <h3 class="card-title">查詢家庭資料</h3>
        <div class="search-method">
          <el-radio-group v-model="form.searchMethod">
            <el-radio
              v-for="m in searchMethods"
              :key="m.value"
              :value="m.value"
            >
              {{ m.label }}
            </el-radio>
          </el-radio-group>
        </div>
        <div class="search-input-row">
          <el-input
            v-model="form.searchText"
            :placeholder="placeholders[form.searchMethod]"
            class="search-input"
            @keyup.enter="handleSearch"
          />
          <el-button class="search-btn" @click="handleSearch">
            <el-icon><Search /></el-icon>
            查詢
          </el-button>
        </div>
      </div>

      <div v-if="searched" class="search-card">
        <h3 class="card-title">查詢結果（請選擇欲編輯之戶口）</h3>
        <HouseholdTable
          :data="memberStore.households"
          :loading="memberStore.loading"
          @select="handleSelect"
        />
      </div>

      <HouseholdLampInfoCard
        v-if="selectedHousehold && memberStore.currentHousehold && lampStore.householdLamps"
        :household="memberStore.currentHousehold"
        :household-lamps="lampStore.householdLamps"
        @print="handlePrint"
        @history="handleHistory"
      />
    </main>

    <LampHistoryDialog
      v-model:visible="historyVisible"
      :records="lampStore.lampHistory"
    />
  </div>
</template>

<style scoped lang="scss">
.lamp-edit-list-page {
  min-height: 100vh;
  background: $temple-bg-cream;
}

.list-content {
  max-width: 1000px;
  margin: 0 auto;
  padding: 32px 40px;
}

.search-card {
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

.year-select {
  width: 160px;
}

.search-method {
  margin-bottom: 12px;
}

.search-input-row {
  display: flex;
  gap: 8px;
}

.search-input {
  flex: 1;
}

.search-btn {
  background: $temple-gold-primary;
  color: white;
  border: none;
  border-radius: 8px;
  padding: 8px 16px;

  &:hover,
  &:focus {
    background: $temple-gold-dark;
    color: white;
  }
}
</style>
