<script setup lang="ts">
import type { LampRecord } from '@/types'

defineProps<{
  visible: boolean
  records: LampRecord[]
  loading?: boolean
}>()

const emit = defineEmits<{
  'update:visible': [value: boolean]
}>()
</script>

<template>
  <el-dialog
    :model-value="visible"
    title="點燈歷史紀錄"
    width="700px"
    @close="emit('update:visible', false)"
  >
    <el-table :data="records" v-loading="loading" stripe max-height="400">
      <el-table-column prop="year" label="年度" width="80" />
      <el-table-column prop="memberName" label="姓名" width="100" />
      <el-table-column prop="lampType" label="燈種" width="100" />
      <el-table-column label="金額" width="100">
        <template #default="{ row }">
          {{ row.amount.toLocaleString() }}
        </template>
      </el-table-column>
      <el-table-column label="繳費" width="80">
        <template #default="{ row }">
          <el-tag :type="row.isPaid ? 'success' : 'warning'" size="small">
            {{ row.isPaid ? '已繳' : '未繳' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="notes" label="備註" />
    </el-table>
  </el-dialog>
</template>
