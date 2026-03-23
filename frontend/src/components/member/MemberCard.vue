<script setup lang="ts">
import { reactive, watch } from 'vue'
import LunarDatePicker from '@/components/common/LunarDatePicker.vue'
import type { CalendarType, MemberRole } from '@/types'

const props = defineProps<{
  modelValue: {
    name: string
    role: MemberRole
    birthday: {
      calendarType: CalendarType
      year: number | undefined
      month: number | undefined
      day: number | undefined
    }
  }
  index: number
  removable?: boolean
}>()

const emit = defineEmits<{
  'update:modelValue': [value: typeof props.modelValue]
  remove: []
}>()

const form = reactive({ ...props.modelValue })

watch(form, () => {
  emit('update:modelValue', {
    name: form.name,
    role: form.role,
    birthday: { ...form.birthday },
  })
}, { deep: true })

watch(() => props.modelValue, (val) => {
  Object.assign(form, val)
  form.birthday = { ...val.birthday }
}, { deep: true })
</script>

<template>
  <div class="member-card">
    <div class="card-header" v-if="removable">
      <el-button
        type="danger"
        text
        size="small"
        @click="emit('remove')"
      >
        移除
      </el-button>
    </div>

    <div class="card-field">
      <label class="field-label">
        戶員姓名：<span class="required-star">*</span>
      </label>
      <el-input v-model="form.name" placeholder="姓名" />
    </div>

    <div class="card-field">
      <label class="field-label">
        戶員身份：<span class="required-star">*</span>
      </label>
      <el-select v-model="form.role" placeholder="選擇身份">
        <el-option label="戶長" value="head" />
        <el-option label="戶員" value="member" />
      </el-select>
    </div>

    <div class="card-field">
      <LunarDatePicker
        label="戶員誕辰："
        :required="true"
        v-model:calendarType="form.birthday.calendarType"
        v-model:year="form.birthday.year"
        v-model:month="form.birthday.month"
        v-model:day="form.birthday.day"
      />
    </div>
  </div>
</template>

<style scoped lang="scss">
.member-card {
  position: relative;
  padding: 0;
}

.card-header {
  position: absolute;
  top: 8px;
  right: 8px;
}

.card-field {
  margin-bottom: 16px;

  &:last-child {
    margin-bottom: 0;
  }

  > :deep(.el-input) {
    width: 250px;
  }

  > :deep(.el-select) {
    width: 120px;
  }
}

.field-label {
  display: block;
  font-size: 14px;
  color: $temple-text-dark;
  margin-bottom: 6px;
}

.required-star {
  color: #f56c6c;
}
</style>
