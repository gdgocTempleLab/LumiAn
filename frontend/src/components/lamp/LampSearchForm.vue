<script setup lang="ts">
import { ref } from 'vue'

const emit = defineEmits<{
  search: [params: { year: number; searchMethod: string; searchText: string }]
}>()

const currentYear = new Date().getFullYear()
const year = ref(currentYear)
const searchMethod = ref('phone')
const searchText = ref('')

const years: number[] = []
for (let y = currentYear; y >= currentYear - 10; y--) {
  years.push(y)
}

function handleSearch() {
  emit('search', {
    year: year.value,
    searchMethod: searchMethod.value,
    searchText: searchText.value,
  })
}
</script>

<template>
  <div class="lamp-search-form">
    <div class="year-filter">
      <label class="filter-label">年份：</label>
      <el-select v-model="year" class="year-select">
        <el-option v-for="y in years" :key="y" :label="`${y} 年`" :value="y" />
      </el-select>
    </div>

    <div class="search-section">
      <h4 class="search-title">查詢家庭資料</h4>
      <div class="search-method">
        <el-radio-group v-model="searchMethod">
          <el-radio value="phone">市話號碼</el-radio>
          <el-radio value="mobile">手機號碼</el-radio>
          <el-radio value="name">姓名</el-radio>
        </el-radio-group>
      </div>
      <div class="search-input-row">
        <el-input
          v-model="searchText"
          placeholder="請輸入查詢內容"
          class="search-input"
          @keyup.enter="handleSearch"
        />
        <el-button type="primary" @click="handleSearch">查詢</el-button>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.lamp-search-form {
  background: white;
  border: 1px solid $temple-border-light;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
}

.year-filter {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 20px;
}

.filter-label {
  font-size: 14px;
  font-weight: bold;
}

.year-select {
  width: 120px;
}

.search-title {
  font-size: 14px;
  font-weight: bold;
  margin-bottom: 12px;
}

.search-method {
  margin-bottom: 12px;
}

.search-input-row {
  display: flex;
  gap: 8px;
}

.search-input {
  max-width: 300px;
}
</style>
