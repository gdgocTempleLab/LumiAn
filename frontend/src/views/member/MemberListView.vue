<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import AppHeader from '@/components/layout/AppHeader.vue'
import PageTitleBar from '@/components/layout/PageTitleBar.vue'
import MemberSearchForm from '@/components/member/MemberSearchForm.vue'
import HouseholdTable from '@/components/member/HouseholdTable.vue'
import { useMemberStore } from '@/stores/member'
import type { Household } from '@/types'

const router = useRouter()
const memberStore = useMemberStore()
const searched = ref(false)

async function handleSearch(params: { searchMethod: string; searchText: string }) {
  await memberStore.searchHouseholds({
    searchMethod: params.searchMethod as 'phone' | 'name' | 'mobile',
    searchText: params.searchText,
  })
  searched.value = true
}

function handleEdit(household: Household) {
  memberStore.currentHousehold = household
  router.push('/member/edit')
}

function handleDelete(household: Household) {
  memberStore.currentHousehold = household
  router.push('/member/delete')
}
</script>

<template>
  <div class="member-list-page">
    <AppHeader compact />
    <PageTitleBar title="戶口列表" :show-save="false" :show-cancel="false" />

    <main class="list-content">
      <MemberSearchForm @search="handleSearch" />

      <div v-if="searched">
        <p class="result-hint">
          查詢結果（請選擇欲編輯之戶口，共 {{ memberStore.totalCount }} 筆）
        </p>
        <HouseholdTable
          :data="memberStore.households"
          :loading="memberStore.loading"
          :show-actions="true"
          @edit="handleEdit"
          @delete="handleDelete"
        />
      </div>
    </main>
  </div>
</template>

<style scoped lang="scss">
.member-list-page {
  min-height: 100vh;
  background: $temple-bg-cream;
}

.list-content {
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
