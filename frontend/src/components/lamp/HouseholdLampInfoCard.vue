<script setup lang="ts">
import { computed } from 'vue'
import { User, Phone, Iphone, OfficeBuilding, Document, Timer, SuccessFilled, RemoveFilled } from '@element-plus/icons-vue'
import type { Household, HouseholdLampSummary } from '@/types'
import { formatBirthday } from '@/utils/birthday-format'

const props = defineProps<{
  household: Household
  householdLamps: HouseholdLampSummary
}>()

const emit = defineEmits<{
  print: []
  history: []
}>()

const headName = computed(() => {
  const head = props.household.members.find((m) => m.role === 'head')
  return head?.name || props.household.members[0]?.name || '-'
})

const displayPhone = computed(() => {
  if (props.household.phoneAreaCode && props.household.phoneNumber) {
    return `${props.household.phoneAreaCode}-${props.household.phoneNumber}`
  }
  return '-'
})

const displayAddress = computed(() => {
  const addr = props.household.registeredAddress
  const zipCode = addr.districtCode || ''
  return `${zipCode}${addr.countyName}${addr.districtName}${addr.villageName || ''}${addr.detail}`
})

interface MemberLampRow {
  memberId: number
  name: string
  birthday: string
  hasGuangMing: boolean
  hasTaiSui: boolean
}

const memberRows = computed<MemberLampRow[]>(() => {
  return props.household.members.map((member) => {
    const lampMember = props.householdLamps.members.find((m) => m.memberId === member.id)
    const lampTypes = lampMember?.lamps.map((l) => l.lampType) || []
    return {
      memberId: member.id,
      name: member.name,
      birthday: formatBirthday(member.birthday),
      hasGuangMing: lampTypes.includes('光明燈'),
      hasTaiSui: lampTypes.includes('太歲燈'),
    }
  })
})
</script>

<template>
  <div class="household-lamp-info">
    <div class="info-header">
      <h3 class="info-title">戶口點燈資訊</h3>
      <div class="info-actions">
        <el-button @click="emit('print')">
          <el-icon><Document /></el-icon>
          列印報名表
        </el-button>
        <el-button @click="emit('history')">
          <el-icon><Timer /></el-icon>
          歷史紀錄
        </el-button>
      </div>
    </div>

    <div class="household-detail">
      <p class="detail-row">
        <el-icon><User /></el-icon>
        <span class="detail-label">戶長姓名：</span>
        <span>{{ headName }}</span>
      </p>
      <p class="detail-row">
        <el-icon><Phone /></el-icon>
        <span class="detail-label">電話（市話）：</span>
        <span>{{ displayPhone }}</span>
      </p>
      <p class="detail-row">
        <el-icon><Iphone /></el-icon>
        <span class="detail-label">電話（手機）：</span>
        <span>{{ household.mobile || '-' }}</span>
      </p>
      <p class="detail-row">
        <el-icon><OfficeBuilding /></el-icon>
        <span class="detail-label">地址：</span>
        <span>{{ displayAddress }}</span>
      </p>
    </div>

    <div class="member-lamp-table">
      <el-table :data="memberRows" :show-header="true">
        <el-table-column min-width="120">
          <template #header>
            <span class="column-header"><el-icon><User /></el-icon> 姓名</span>
          </template>
          <template #default="{ row }">
            {{ row.name }}
          </template>
        </el-table-column>

        <el-table-column min-width="240">
          <template #header>
            <span class="column-header"><el-icon><Timer /></el-icon> 誕辰</span>
          </template>
          <template #default="{ row }">
            {{ row.birthday }}
          </template>
        </el-table-column>

        <el-table-column min-width="100" align="center">
          <template #header>
            <span class="column-header"><el-icon><User /></el-icon> 光明燈</span>
          </template>
          <template #default="{ row }">
            <el-icon :size="22" :color="row.hasGuangMing ? '#409EFF' : '#dcdfe6'">
              <SuccessFilled v-if="row.hasGuangMing" />
              <RemoveFilled v-else />
            </el-icon>
          </template>
        </el-table-column>

        <el-table-column min-width="100" align="center">
          <template #header>
            <span class="column-header"><el-icon><Timer /></el-icon> 太歲燈</span>
          </template>
          <template #default="{ row }">
            <el-icon :size="22" :color="row.hasTaiSui ? '#409EFF' : '#dcdfe6'">
              <SuccessFilled v-if="row.hasTaiSui" />
              <RemoveFilled v-else />
            </el-icon>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<style scoped lang="scss">
.household-lamp-info {
  background: white;
  border: 1px solid $temple-border-light;
  border-radius: 8px;
  padding: 20px;
}

.info-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.info-title {
  font-size: 18px;
  font-weight: bold;
  color: $temple-text-dark;
}

.info-actions {
  display: flex;
  gap: 8px;
}

.household-detail {
  background: #f9f7f2;
  border-radius: 8px;
  padding: 16px 20px;
  margin-bottom: 20px;
}

.detail-row {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 15px;
  color: $temple-text-dark;
  line-height: 2;
}

.detail-label {
  font-weight: 500;
}

.member-lamp-table {
  border-radius: 8px;
  overflow: hidden;
}

.column-header {
  display: inline-flex;
  align-items: center;
  gap: 4px;
}
</style>
