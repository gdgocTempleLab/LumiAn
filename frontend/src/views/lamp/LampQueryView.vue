<script setup lang="ts">
import { ref } from 'vue'
import AppHeader from '@/components/layout/AppHeader.vue'
import PageTitleBar from '@/components/layout/PageTitleBar.vue'
import LampSearchForm from '@/components/lamp/LampSearchForm.vue'
import LampRecordTable from '@/components/lamp/LampRecordTable.vue'
import LampHistoryDialog from '@/components/lamp/LampHistoryDialog.vue'
import HouseholdTable from '@/components/member/HouseholdTable.vue'
import { useMemberStore } from '@/stores/member'
import { useLampStore } from '@/stores/lamp'
import type { Household } from '@/types'

const memberStore = useMemberStore()
const lampStore = useLampStore()
const searched = ref(false)
const selectedHousehold = ref(false)
const historyVisible = ref(false)

async function handleSearch(params: { year: number; searchMethod: string; searchText: string }) {
  lampStore.selectedYear = params.year
  await memberStore.searchHouseholds({
    searchMethod: params.searchMethod as 'phone' | 'name' | 'mobile',
    searchText: params.searchText,
  })
  searched.value = true
  selectedHousehold.value = false
}

async function handleSelectHousehold(household: Household) {
  await lampStore.queryLamps({ householdId: household.id, year: lampStore.selectedYear })
  selectedHousehold.value = true
}

async function showHistory() {
  if (memberStore.currentHousehold) {
    await lampStore.loadLampHistory(memberStore.currentHousehold.id)
  }
  historyVisible.value = true
}
</script>

<template>
  <div class="lamp-query-page">
    <AppHeader compact />
    <PageTitleBar title="查詢點燈資訊" :show-save="false" :show-cancel="false" />

    <main class="query-content">
      <LampSearchForm @search="handleSearch" />

      <div v-if="searched && !selectedHousehold">
        <p class="result-hint">查詢結果（共 {{ memberStore.totalCount }} 筆）</p>
        <HouseholdTable
          :data="memberStore.households"
          :loading="memberStore.loading"
          @select="handleSelectHousehold"
        />
      </div>

      <div v-if="selectedHousehold">
        <div class="section-header">
          <h3>點燈紀錄</h3>
          <el-button text type="primary" @click="showHistory">查看歷史紀錄</el-button>
        </div>
        <LampRecordTable :data="lampStore.lampRecords" :loading="lampStore.loading" />
      </div>
    </main>

    <LampHistoryDialog
      v-model:visible="historyVisible"
      :records="lampStore.lampHistory"
    />
  </div>
</template>

<style scoped lang="scss">
.lamp-query-page {
  min-height: 100vh;
  background: $temple-bg-cream;
}

.query-content {
  max-width: 1000px;
  margin: 0 auto;
  padding: 32px 40px;
}

.result-hint {
  font-size: 14px;
  color: $temple-text-muted;
  margin-bottom: 12px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}
</style>
