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

async function loadStrips() {
  await lampStore.loadStrips({ year: year.value })
}

onMounted(loadStrips)
</script>

<template>
  <div class="lamp-strip-page">
    <AppHeader compact />
    <PageTitleBar title="查詢燈條名單" :show-save="false" :show-cancel="false" />

    <main class="strip-content">
      <div class="filter-bar">
        <el-select v-model="year" @change="loadStrips" class="year-select">
          <el-option v-for="y in years" :key="y" :label="`${y} 年`" :value="y" />
        </el-select>
      </div>

      <el-table :data="lampStore.stripData" v-loading="lampStore.loading" stripe>
        <el-table-column prop="memberName" label="姓名" width="150" />
        <el-table-column prop="lampType" label="燈種" width="150" />
        <el-table-column prop="year" label="年度" width="100" />
      </el-table>
    </main>
  </div>
</template>

<style scoped lang="scss">
.lamp-strip-page { min-height: 100vh; background: $temple-bg-cream; }
.strip-content { max-width: 700px; margin: 0 auto; padding: 32px 40px; }
.filter-bar { margin-bottom: 16px; }
.year-select { width: 120px; }
</style>
