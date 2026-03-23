<script setup lang="ts">
import { reactive } from 'vue'
import { Search } from '@element-plus/icons-vue'

const emit = defineEmits<{
  search: [params: { searchMethod: string; searchText: string }]
}>()

const form = reactive({
  searchMethod: 'phone',
  searchText: '',
})

function handleSearch() {
  emit('search', { ...form })
}

const searchMethods = [
  { value: 'phone', label: '電話（市話）' },
  { value: 'mobile', label: '電話（手機）' },
  { value: 'name', label: '戶長姓名' },
]

const placeholders: Record<string, string> = {
  phone: '請輸入市話號碼',
  mobile: '請輸入手機號碼',
  name: '請輸入戶長姓名',
}
</script>

<template>
  <div class="member-search-form">
    <div class="search-header">
      <h3 class="search-title">查詢家庭資料</h3>
    </div>

    <div class="search-row">
      <div class="search-method">
        <el-radio-group v-model="form.searchMethod">
          <el-radio
            v-for="method in searchMethods"
            :key="method.value"
            :value="method.value"
          >
            {{ method.label }}
          </el-radio>
        </el-radio-group>
      </div>

      <div class="search-input-row">
        <el-input
          v-model="form.searchText"
          :placeholder="placeholders[form.searchMethod]"
          class="search-input"
          @keyup.enter="handleSearch"
        />
        <el-button class="search-btn" @click="handleSearch">
          <el-icon><Search /></el-icon>
          查詢
        </el-button>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.member-search-form {
  background: white;
  border: 1px solid $temple-border-light;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
}

.search-title {
  font-size: 16px;
  font-weight: bold;
  color: $temple-text-dark;
  margin-bottom: 16px;
}

.search-method {
  margin-bottom: 12px;
}

.search-input-row {
  display: flex;
  gap: 8px;
}

.search-input {
  flex: 1;
}

.search-btn {
  background: $temple-gold-primary;
  color: white;
  border: none;
  border-radius: 8px;
  padding: 8px 16px;

  &:hover,
  &:focus {
    background: $temple-gold-dark;
    color: white;
  }
}
</style>
