<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import AppHeader from '@/components/layout/AppHeader.vue'
import PageTitleBar from '@/components/layout/PageTitleBar.vue'
import LampEditForm from '@/components/lamp/LampEditForm.vue'
import LampHistoryDialog from '@/components/lamp/LampHistoryDialog.vue'
import { useLampStore } from '@/stores/lamp'
import { useMemberStore } from '@/stores/member'
import type { LampRecord } from '@/types'

const route = useRoute()
const router = useRouter()
const lampStore = useLampStore()
const memberStore = useMemberStore()
const historyVisible = ref(false)
const pageReady = ref(false)

const householdIdParam = Array.isArray(route.params.householdId)
  ? route.params.householdId[0]
  : route.params.householdId

const householdId = householdIdParam ? Number(householdIdParam) : 0

onMounted(async () => {
  if (!householdId) {
    ElMessage.error('缺少戶口編號')
    router.push({ name: 'MemberList' })
    return
  }

  try {
    // 先從 member store 載入戶號信息以取得電話
    const household = await memberStore.loadHousehold(householdId)
    if (!household) {
      ElMessage.error('找不到指定戶口')
      router.push({ name: 'MemberList' })
      return
    }

    // 組合電話號碼並載入點燈紀錄
    const fullPhone = household.phoneAreaCode && household.phoneNumber
      ? `${household.phoneAreaCode}-${household.phoneNumber}`
      : household.phoneAreaCode || household.phoneNumber || ''

    await lampStore.loadHouseholdLamps(householdId, fullPhone)
    pageReady.value = true
  } catch (error) {
    console.error('載入點燈資料失敗:', error)
    ElMessage.error('載入點燈資料失敗')
  }
})

async function handleSaveRecord(record: LampRecord) {
  try {
    await lampStore.saveLampRecord(record.id, {
      amount: record.amount,
      isPaid: record.isPaid,
      notes: record.notes,
    })
    ElMessage.success('更新成功')
    
    // 重新載入數據以確保顯示最新狀態
    const household = memberStore.currentHousehold
    if (household) {
      const fullPhone = household.phoneAreaCode && household.phoneNumber
        ? `${household.phoneAreaCode}-${household.phoneNumber}`
        : household.phoneAreaCode || household.phoneNumber || ''
      await lampStore.loadHouseholdLamps(householdId, fullPhone)
    }
  } catch (error) {
    console.error('保存失敗:', error)
    ElMessage.error('保存失敗')
  }
}

async function handleAddLamp(data: { memberId: number; lampType: string; amount: number }) {
  try {
    await lampStore.createLamp({
      householdId,
      memberId: data.memberId,
      lampType: data.lampType,
      year: lampStore.selectedYear,
      amount: data.amount,
      isPaid: false,
    })
    ElMessage.success('新增成功')
    
    // 重新載入數據
    const household = memberStore.currentHousehold
    if (household) {
      const fullPhone = household.phoneAreaCode && household.phoneNumber
        ? `${household.phoneAreaCode}-${household.phoneNumber}`
        : household.phoneAreaCode || household.phoneNumber || ''
      await lampStore.loadHouseholdLamps(householdId, fullPhone)
    }
  } catch (error) {
    console.error('新增失敗:', error)
    ElMessage.error('新增失敗')
  }
}

async function showHistory() {
  try {
    await lampStore.loadLampHistory(householdId)
    historyVisible.value = true
  } catch (error) {
    console.error('載入歷史紀錄失敗:', error)
    ElMessage.error('載入歷史紀錄失敗')
  }
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

    <main class="edit-content" v-loading="lampStore.loading || !pageReady">
      <div v-if="pageReady && lampStore.householdLamps">
        <LampEditForm
          v-for="member in lampStore.householdLamps.members"
          :key="member.memberId"
          :records="member.lamps"
          :member-name="member.memberName"
          @save="handleSaveRecord"
          @add="handleAddLamp"
        />
      </div>

      <el-empty v-else-if="pageReady && !lampStore.loading" description="無點燈紀錄" />
    </main>

    <LampHistoryDialog
      v-model:visible="historyVisible"
      :records="lampStore.lampHistory"
      :loading="lampStore.loading"
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
