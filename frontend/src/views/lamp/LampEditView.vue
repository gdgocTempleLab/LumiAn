<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import AppHeader from '@/components/layout/AppHeader.vue'
import PageTitleBar from '@/components/layout/PageTitleBar.vue'
import LampEditForm from '@/components/lamp/LampEditForm.vue'
import LampHistoryDialog from '@/components/lamp/LampHistoryDialog.vue'
import { useLampStore } from '@/stores/lamp'
import type { LampRecord } from '@/types'

const route = useRoute()
const lampStore = useLampStore()
const historyVisible = ref(false)
const householdId = Number(route.params.householdId)

onMounted(async () => {
  await lampStore.loadHouseholdLamps(householdId)
})

async function handleSaveRecord(record: LampRecord) {
  await lampStore.saveLampRecord(record.id, {
    amount: record.amount,
    isPaid: record.isPaid,
    notes: record.notes,
  })
}

async function handleAddLamp(data: { memberId: number; lampType: string; amount: number }) {
  await lampStore.createLamp({
    householdId,
    memberId: data.memberId,
    lampType: data.lampType,
    year: lampStore.selectedYear,
    amount: data.amount,
    isPaid: false,
  })
  await lampStore.loadHouseholdLamps(householdId)
}

async function showHistory() {
  await lampStore.loadLampHistory(householdId)
  historyVisible.value = true
}
</script>

<template>
  <div class="lamp-edit-page">
    <AppHeader compact />
    <PageTitleBar title="編輯點燈" :show-save="false">
      <template #default>
        <el-button text type="primary" @click="showHistory">查看歷史紀錄</el-button>
      </template>
    </PageTitleBar>

    <main class="edit-content" v-loading="lampStore.loading">
      <div v-if="lampStore.householdLamps">
        <LampEditForm
          v-for="member in lampStore.householdLamps.members"
          :key="member.memberId"
          :records="member.lamps"
          :member-name="member.memberName"
          @save="handleSaveRecord"
          @add="handleAddLamp"
        />
      </div>

      <el-empty v-else-if="!lampStore.loading" description="無點燈紀錄" />
    </main>

    <LampHistoryDialog
      v-model:visible="historyVisible"
      :records="lampStore.lampHistory"
    />
  </div>
</template>

<style scoped lang="scss">
.lamp-edit-page {
  min-height: 100vh;
  background: $temple-bg-cream;
}

.edit-content {
  max-width: 800px;
  margin: 0 auto;
  padding: 32px 40px;
}
</style>
