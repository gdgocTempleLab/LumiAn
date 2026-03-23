<script setup lang="ts">
import { ref, computed } from 'vue'
import { ArrowLeft, ArrowRight } from '@element-plus/icons-vue'

const props = defineProps<{
  startDate: Date
  endDate: Date
}>()

const emit = defineEmits<{
  'update:startDate': [date: Date]
  'update:endDate': [date: Date]
}>()

const leftPanel = ref({ year: props.startDate.getFullYear(), month: props.startDate.getMonth() })
const rightPanel = ref({ year: props.endDate.getFullYear(), month: props.endDate.getMonth() })

const weekDays = ['日', '一', '二', '三', '四', '五', '六']

interface CalendarDay {
  date: Date
  day: number
  isCurrentMonth: boolean
}

function generateDays(year: number, month: number): CalendarDay[] {
  const firstDay = new Date(year, month, 1)
  const startOffset = firstDay.getDay()
  const days: CalendarDay[] = []

  for (let i = startOffset - 1; i >= 0; i--) {
    const d = new Date(year, month, -i)
    days.push({ date: d, day: d.getDate(), isCurrentMonth: false })
  }

  const daysInMonth = new Date(year, month + 1, 0).getDate()
  for (let i = 1; i <= daysInMonth; i++) {
    const d = new Date(year, month, i)
    days.push({ date: d, day: i, isCurrentMonth: true })
  }

  const remaining = 42 - days.length
  for (let i = 1; i <= remaining; i++) {
    const d = new Date(year, month + 1, i)
    days.push({ date: d, day: i, isCurrentMonth: false })
  }

  return days
}

const leftDays = computed(() => generateDays(leftPanel.value.year, leftPanel.value.month))
const rightDays = computed(() => generateDays(rightPanel.value.year, rightPanel.value.month))

function leftTitle() {
  return `${leftPanel.value.year}年 ${getMonthName(leftPanel.value.month)}`
}

function rightTitle() {
  return `${rightPanel.value.year}年 ${getMonthName(rightPanel.value.month)}`
}

function getMonthName(month: number) {
  const names = ['一月', '二月', '三月', '四月', '五月', '六月', '七月', '八月', '九月', '十月', '十一月', '十二月']
  return names[month]
}

function prevMonth(panel: 'left' | 'right') {
  const p = panel === 'left' ? leftPanel : rightPanel
  if (p.value.month === 0) {
    p.value = { year: p.value.year - 1, month: 11 }
  } else {
    p.value = { ...p.value, month: p.value.month - 1 }
  }
}

function nextMonth(panel: 'left' | 'right') {
  const p = panel === 'left' ? leftPanel : rightPanel
  if (p.value.month === 11) {
    p.value = { year: p.value.year + 1, month: 0 }
  } else {
    p.value = { ...p.value, month: p.value.month + 1 }
  }
}

function selectDate(day: CalendarDay, panel: 'left' | 'right') {
  if (!day.isCurrentMonth) return
  if (panel === 'left') {
    emit('update:startDate', day.date)
  } else {
    emit('update:endDate', day.date)
  }
}

function isSameDay(a: Date, b: Date) {
  return a.getFullYear() === b.getFullYear() && a.getMonth() === b.getMonth() && a.getDate() === b.getDate()
}

function isSelected(day: CalendarDay) {
  return isSameDay(day.date, props.startDate) || isSameDay(day.date, props.endDate)
}

function formatDate(date: Date) {
  const y = date.getFullYear()
  const m = String(date.getMonth() + 1).padStart(2, '0')
  const d = String(date.getDate()).padStart(2, '0')
  return `${y} 年 ${m} 月 ${d} 日`
}
</script>

<template>
  <div class="date-range-picker">
    <div class="calendar-panels">
      <div class="calendar-panel">
        <div class="panel-header">
          <button class="nav-btn" @click="prevMonth('left')">
            <el-icon><ArrowLeft /></el-icon>
          </button>
          <span class="panel-title">{{ leftTitle() }}</span>
          <button class="nav-btn" @click="nextMonth('left')">
            <el-icon><ArrowRight /></el-icon>
          </button>
        </div>
        <div class="weekdays">
          <span v-for="w in weekDays" :key="w" class="weekday">{{ w }}</span>
        </div>
        <div class="days-grid">
          <button
            v-for="(day, i) in leftDays"
            :key="i"
            class="day-cell"
            :class="{
              'other-month': !day.isCurrentMonth,
              'selected': day.isCurrentMonth && isSelected(day),
            }"
            @click="selectDate(day, 'left')"
          >
            {{ day.day }}
          </button>
        </div>
        <div class="date-display">{{ formatDate(startDate) }}</div>
      </div>

      <div class="separator">至</div>

      <div class="calendar-panel">
        <div class="panel-header">
          <button class="nav-btn" @click="prevMonth('right')">
            <el-icon><ArrowLeft /></el-icon>
          </button>
          <span class="panel-title">{{ rightTitle() }}</span>
          <button class="nav-btn" @click="nextMonth('right')">
            <el-icon><ArrowRight /></el-icon>
          </button>
        </div>
        <div class="weekdays">
          <span v-for="w in weekDays" :key="w" class="weekday">{{ w }}</span>
        </div>
        <div class="days-grid">
          <button
            v-for="(day, i) in rightDays"
            :key="i"
            class="day-cell"
            :class="{
              'other-month': !day.isCurrentMonth,
              'selected': day.isCurrentMonth && isSelected(day),
            }"
            @click="selectDate(day, 'right')"
          >
            {{ day.day }}
          </button>
        </div>
        <div class="date-display">{{ formatDate(endDate) }}</div>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.date-range-picker {
  margin-bottom: 24px;
}

.calendar-panels {
  display: flex;
  align-items: flex-start;
  justify-content: center;
  gap: 16px;
}

.calendar-panel {
  width: 220px;
}

.panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 8px;
}

.panel-title {
  font-size: 14px;
  font-weight: bold;
  color: $temple-text-dark;
}

.nav-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 4px;
  color: $temple-text-muted;
  display: flex;
  align-items: center;

  &:hover {
    color: $temple-gold-primary;
  }
}

.weekdays {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  text-align: center;
  margin-bottom: 4px;
}

.weekday {
  font-size: 12px;
  color: $temple-text-muted;
  padding: 4px 0;
}

.days-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  text-align: center;
}

.day-cell {
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 1px auto;
  font-size: 13px;
  border: none;
  background: none;
  cursor: pointer;
  border-radius: 50%;
  color: $temple-text-dark;

  &:hover:not(.other-month) {
    background: $temple-gold-light;
  }

  &.other-month {
    color: #ccc;
    cursor: default;
  }

  &.selected {
    background: $temple-gold-primary;
    color: white;
    font-weight: bold;
  }
}

.separator {
  display: flex;
  align-items: center;
  padding-top: 100px;
  font-size: 14px;
  color: $temple-text-muted;
}

.date-display {
  text-align: center;
  margin-top: 8px;
  font-size: 14px;
  color: $temple-text-dark;
  letter-spacing: 2px;
}
</style>
