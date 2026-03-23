<script setup lang="ts">
import type { LampRecord } from '@/types'

defineProps<{
  data: LampRecord[]
  loading?: boolean
}>()
</script>

<template>
  <div class="lamp-record-table">
    <el-table :data="data" v-loading="loading" stripe>
      <el-table-column prop="memberName" label="姓名" width="120" />
      <el-table-column prop="lampType" label="燈種" width="120" />
      <el-table-column prop="year" label="年度" width="80" />
      <el-table-column label="金額" width="100">
        <template #default="{ row }">
          {{ row.amount.toLocaleString() }}
        </template>
      </el-table-column>
      <el-table-column label="繳費狀態" width="100">
        <template #default="{ row }">
          <el-tag :type="row.isPaid ? 'success' : 'warning'" size="small">
            {{ row.isPaid ? '已繳' : '未繳' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="notes" label="備註" />
    </el-table>
  </div>
</template>

<style scoped lang="scss">
.lamp-record-table {
  background: white;
  border-radius: 8px;
  overflow: hidden;
}
</style>
