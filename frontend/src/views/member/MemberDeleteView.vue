<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import AppHeader from '@/components/layout/AppHeader.vue'
import PageTitleBar from '@/components/layout/PageTitleBar.vue'
import MemberSearchForm from '@/components/member/MemberSearchForm.vue'
import HouseholdTable from '@/components/member/HouseholdTable.vue'
import ConfirmDialog from '@/components/common/ConfirmDialog.vue'
import { useMemberStore } from '@/stores/member'
import type { Household } from '@/types'

const router = useRouter()
const memberStore = useMemberStore()
const searched = ref(false)
const confirmVisible = ref(false)
const selectedHousehold = ref<Household | null>(null)

async function handleSearch(params: { searchMethod: string; searchText: string }) {
  await memberStore.searchHouseholds({
    searchMethod: params.searchMethod as 'phone' | 'name' | 'mobile',
    searchText: params.searchText,
  })
  searched.value = true
}

function handleSelect(household: Household) {
  selectedHousehold.value = household
  confirmVisible.value = true
}

async function handleConfirmDelete() {
  if (!selectedHousehold.value) return

  try {
    await memberStore.removeHousehold(selectedHousehold.value.id)
    ElMessage.success('刪除成功')
    confirmVisible.value = false
    selectedHousehold.value = null
  } catch {
    ElMessage.error('刪除失敗')
  }
}
</script>

<template>
  <div class="member-delete-page">
    <AppHeader compact />
    <PageTitleBar title="刪除信徒資料" :show-save="false" :show-cancel="false" />

    <main class="delete-content">
      <MemberSearchForm @search="handleSearch" />

      <div v-if="searched">
        <p class="result-hint">
          查詢結果（請選擇欲刪除之戶口，共 {{ memberStore.totalCount }} 筆）
        </p>
        <HouseholdTable
          :data="memberStore.households"
          :loading="memberStore.loading"
          @select="handleSelect"
        />
      </div>
    </main>

    <ConfirmDialog
      v-model:visible="confirmVisible"
      title="確認刪除"
      :message="`確定要刪除戶長「${selectedHousehold?.members.find(m => m.role === 'head')?.name || ''}」的戶口資料嗎？此操作無法復原。`"
      :loading="memberStore.loading"
      @confirm="handleConfirmDelete"
    />
  </div>
</template>

<style scoped lang="scss">
.member-delete-page {
  min-height: 100vh;
  background: $temple-bg-cream;
}

.delete-content {
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
