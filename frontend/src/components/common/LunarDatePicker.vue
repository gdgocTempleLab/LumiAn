<script setup lang="ts">
import { computed } from 'vue'
import type { CalendarType } from '@/types'

const props = defineProps<{
  calendarType: CalendarType
  year: number | undefined
  month: number | undefined
  day: number | undefined
  label?: string
  required?: boolean
}>()

const emit = defineEmits<{
  'update:calendarType': [value: CalendarType]
  'update:year': [value: number]
  'update:month': [value: number]
  'update:day': [value: number]
}>()

const currentYear = new Date().getFullYear()

const years = computed(() => {
  const result = []
  for (let y = currentYear; y >= 1920; y--) {
    result.push(y)
  }
  return result
})

const months = computed(() => {
  const result = []
  for (let m = 1; m <= 12; m++) {
    result.push(m)
  }
  return result
})

const days = computed(() => {
  const result = []
  const maxDay = props.calendarType === 'lunar' ? 30 : 31
  for (let d = 1; d <= maxDay; d++) {
    result.push(d)
  }
  return result
})
</script>

<template>
  <div class="lunar-date-picker">
    <div class="date-label" v-if="label">
      {{ label }}{{ required ? '' : '' }}
      <span v-if="required" class="required-star">*</span>
      <el-radio-group
        :model-value="calendarType"
        @update:model-value="emit('update:calendarType', $event as CalendarType)"
        class="calendar-toggle"
      >
        <el-radio value="lunar">農曆</el-radio>
        <el-radio value="solar">國曆</el-radio>
      </el-radio-group>
    </div>

    <div class="date-selects">
      <el-select
        :model-value="year"
        @update:model-value="emit('update:year', $event as number)"
        placeholder="年"
        class="date-select year-select"
      >
        <el-option
          v-for="y in years"
          :key="y"
          :label="y"
          :value="y"
        />
      </el-select>
      <span class="date-unit">年</span>

      <el-select
        :model-value="month"
        @update:model-value="emit('update:month', $event as number)"
        placeholder="月"
        class="date-select"
      >
        <el-option
          v-for="m in months"
          :key="m"
          :label="m"
          :value="m"
        />
      </el-select>
      <span class="date-unit">月</span>

      <el-select
        :model-value="day"
        @update:model-value="emit('update:day', $event as number)"
        placeholder="日"
        class="date-select"
      >
        <el-option
          v-for="d in days"
          :key="d"
          :label="d"
          :value="d"
        />
      </el-select>
      <span class="date-unit">日</span>
    </div>
  </div>
</template>

<style scoped lang="scss">
.lunar-date-picker {
  width: 100%;
}

.date-label {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
  font-size: 14px;
  color: $temple-text-dark;
}

.required-star {
  color: #f56c6c;
}

.calendar-toggle {
  margin-left: 8px;
}

.date-selects {
  display: flex;
  align-items: center;
  gap: 4px;
}

.date-select {
  width: 90px;
}

.year-select {
  width: 110px;
}

.date-unit {
  font-size: 14px;
  color: $temple-text-muted;
}
</style>
