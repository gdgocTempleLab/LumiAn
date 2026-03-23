<script setup lang="ts">
import { ref, onMounted } from 'vue'
import AppHeader from '@/components/layout/AppHeader.vue'
import PageTitleBar from '@/components/layout/PageTitleBar.vue'
import { useLampStore } from '@/stores/lamp'

const lampStore = useLampStore()
const currentYear = new Date().getFullYear()
const year = ref(currentYear)

const years: number[] = []
for (let y = currentYear; y >= currentYear - 10; y--) years.push(y)

async function loadRoster() {
  await lampStore.loadRoster({ year: year.value })
}

onMounted(loadRoster)
</script>

<template>
  <div class="lamp-roster-page">
    <AppHeader compact />
    <PageTitleBar title="查詢點燈清冊" :show-save="false" :show-cancel="false" />

    <main class="roster-content">
      <div class="filter-bar">
        <el-select v-model="year" @change="loadRoster" class="year-select">
          <el-option v-for="y in years" :key="y" :label="`${y} 年`" :value="y" />
        </el-select>
      </div>

      <el-table :data="lampStore.rosterData" v-loading="lampStore.loading" stripe>
        <el-table-column prop="memberName" label="姓名" width="120" />
        <el-table-column prop="lampType" label="燈種" width="120" />
        <el-table-column prop="year" label="年度" width="80" />
        <el-table-column label="金額" width="100">
          <template #default="{ row }">{{ row.amount.toLocaleString() }}</template>
        </el-table-column>
        <el-table-column label="繳費" width="80">
          <template #default="{ row }">
            <el-tag :type="row.isPaid ? 'success' : 'warning'" size="small">
              {{ row.isPaid ? '已繳' : '未繳' }}
            </el-tag>
          </template>
        </el-table-column>
      </el-table>
    </main>
  </div>
</template>

<style scoped lang="scss">
.lamp-roster-page { min-height: 100vh; background: $temple-bg-cream; }
.roster-content { max-width: 900px; margin: 0 auto; padding: 32px 40px; }
.filter-bar { margin-bottom: 16px; }
.year-select { width: 120px; }
</style>
