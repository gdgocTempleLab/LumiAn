<script setup lang="ts">
import type { Household } from '@/types'
import { User, Phone, Iphone, Location, EditPen } from '@element-plus/icons-vue'

defineProps<{
  data: Household[]
  loading?: boolean
  showActions?: boolean
}>()

const emit = defineEmits<{
  edit: [household: Household]
  delete: [household: Household]
  select: [household: Household]
}>()

function getDisplayPhone(h: Household) {
  if (h.phoneAreaCode && h.phoneNumber) {
    return `${h.phoneAreaCode}-${h.phoneNumber}`
  }
  return '-'
}

function getDisplayAddress(h: Household) {
  const addr = h.registeredAddress
  return `${addr.countyName}${addr.districtName}${addr.villageName || ''}${addr.detail}`
}

function getHeadName(h: Household) {
  const head = h.members.find((m) => m.role === 'head')
  return head?.name || h.members[0]?.name || '-'
}
</script>

<template>
  <div class="household-table">
    <el-table :data="data" v-loading="loading">
      <el-table-column min-width="100">
        <template #header>
          <span class="column-header"><el-icon><User /></el-icon> 姓名</span>
        </template>
        <template #default="{ row }">
          {{ getHeadName(row) }}
        </template>
      </el-table-column>

      <el-table-column min-width="140">
        <template #header>
          <span class="column-header"><el-icon><Phone /></el-icon> 電話（市話）</span>
        </template>
        <template #default="{ row }">
          {{ getDisplayPhone(row) }}
        </template>
      </el-table-column>

      <el-table-column min-width="140">
        <template #header>
          <span class="column-header"><el-icon><Iphone /></el-icon> 電話（手機）</span>
        </template>
        <template #default="{ row }">
          {{ row.mobile || '-' }}
        </template>
      </el-table-column>

      <el-table-column min-width="250">
        <template #header>
          <span class="column-header"><el-icon><Location /></el-icon> 地址</span>
        </template>
        <template #default="{ row }">
          {{ getDisplayAddress(row) }}
        </template>
      </el-table-column>

      <el-table-column v-if="showActions" label="操作" width="120" fixed="right">
        <template #default="{ row }">
          <el-button type="primary" text size="small" @click="emit('edit', row)">
            編輯
          </el-button>
          <el-button type="danger" text size="small" @click="emit('delete', row)">
            刪除
          </el-button>
        </template>
      </el-table-column>

      <el-table-column v-if="!showActions" width="80" fixed="right">
        <template #header>
          <span class="column-header"><el-icon><EditPen /></el-icon> 操作</span>
        </template>
        <template #default="{ row }">
          <el-button type="primary" text size="small" @click="emit('select', row)">
            <el-icon :size="18"><EditPen /></el-icon>
          </el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<style scoped lang="scss">
.household-table {
  background: white;
  border-radius: 8px;
  overflow: hidden;
}

.column-header {
  display: inline-flex;
  align-items: center;
  gap: 4px;
}
</style>
