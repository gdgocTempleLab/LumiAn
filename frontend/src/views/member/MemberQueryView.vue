<script setup lang="ts">
import { ref } from 'vue'
import AppHeader from '@/components/layout/AppHeader.vue'
import PageTitleBar from '@/components/layout/PageTitleBar.vue'
import MemberSearchForm from '@/components/member/MemberSearchForm.vue'
import HouseholdTable from '@/components/member/HouseholdTable.vue'
import { useMemberStore } from '@/stores/member'

const memberStore = useMemberStore()
const searched = ref(false)

async function handleSearch(params: { searchMethod: string; searchText: string }) {
  await memberStore.searchHouseholds({
    searchMethod: params.searchMethod as 'phone' | 'name' | 'mobile',
    searchText: params.searchText,
  })
  searched.value = true
}
</script>

<template>
  <div class="member-query-page">
    <AppHeader compact />
    <PageTitleBar title="查詢信徒資料" :show-save="false" :show-cancel="false" />

    <main class="query-content">
      <MemberSearchForm @search="handleSearch" />

      <div v-if="searched">
        <p class="result-hint">
          查詢結果（共 {{ memberStore.totalCount }} 筆）
        </p>
        <HouseholdTable
          :data="memberStore.households"
          :loading="memberStore.loading"
          :show-actions="false"
        />
      </div>
    </main>
  </div>
</template>

<style scoped lang="scss">
.member-query-page {
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
</style>
