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

async function loadData() {
  await lampStore.loadRoster({ year: year.value })
}

onMounted(loadData)

function handlePrint() {
  window.print()
}
</script>

<template>
  <div class="lamp-print-form-page">
    <div class="no-print">
      <AppHeader compact />
      <PageTitleBar title="列印報名表" :show-save="false" :show-cancel="false" />

      <div class="toolbar">
        <el-select v-model="year" @change="loadData" class="year-select">
          <el-option v-for="y in years" :key="y" :label="`${y} 年`" :value="y" />
        </el-select>
        <el-button type="primary" @click="handlePrint">列印</el-button>
      </div>
    </div>

    <div class="print-content">
      <h2 class="print-title">八卦禪寺 {{ year }} 年度點燈報名表</h2>
      <table class="print-table">
        <thead>
          <tr>
            <th>序號</th>
            <th>姓名</th>
            <th>燈種</th>
            <th>金額</th>
            <th>繳費</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, index) in lampStore.rosterData" :key="index">
            <td>{{ index + 1 }}</td>
            <td>{{ item.memberName }}</td>
            <td>{{ item.lampType }}</td>
            <td>{{ item.amount.toLocaleString() }}</td>
            <td>{{ item.isPaid ? '已繳' : '未繳' }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<style scoped lang="scss">
.lamp-print-form-page { min-height: 100vh; background: $temple-bg-cream; }
.toolbar {
  display: flex; gap: 12px; padding: 16px 40px; max-width: 900px; margin: 0 auto;
}
.year-select { width: 120px; }

.print-content {
  max-width: 900px; margin: 0 auto; padding: 20px 40px;
  background: white; border-radius: 8px;
}

.print-title {
  text-align: center; font-size: 20px; margin-bottom: 20px;
}

.print-table {
  width: 100%; border-collapse: collapse;
  th, td { border: 1px solid #ccc; padding: 8px 12px; text-align: center; }
  th { background: #f5f5f5; font-weight: bold; }
}

@media print {
  .no-print { display: none; }
  .print-content { padding: 0; border-radius: 0; }
}
</style>
