<script setup lang="ts">
import MemberCard from './MemberCard.vue'
import type { CalendarType, MemberRole } from '@/types'

interface MemberFormData {
  name: string
  role: MemberRole
  birthday: {
    calendarType: CalendarType
    year: number | undefined
    month: number | undefined
    day: number | undefined
  }
}

const props = defineProps<{
  modelValue: MemberFormData[]
}>()

const emit = defineEmits<{
  'update:modelValue': [value: MemberFormData[]]
}>()

function addMember() {
  const newMembers = [...props.modelValue, {
    name: '',
    role: 'member' as MemberRole,
    birthday: {
      calendarType: 'solar' as CalendarType,
      year: undefined,
      month: undefined,
      day: undefined,
    },
  }]
  emit('update:modelValue', newMembers)
}

function removeMember(index: number) {
  const newMembers = props.modelValue.filter((_, i) => i !== index)
  emit('update:modelValue', newMembers)
}

function updateMember(index: number, value: MemberFormData) {
  const newMembers = [...props.modelValue]
  newMembers[index] = value
  emit('update:modelValue', newMembers)
}
</script>

<template>
  <div class="member-card-list">
    <MemberCard
      v-for="(member, index) in modelValue"
      :key="index"
      :model-value="member"
      :index="index"
      :removable="modelValue.length > 1"
      @update:model-value="updateMember(index, $event)"
      @remove="removeMember(index)"
    />

    <button class="add-member-btn" @click="addMember" title="新增戶員">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 56 40" fill="currentColor">
        <!-- + 號 -->
        <rect x="4" y="16" width="16" height="3.5" rx="1.5" />
        <rect x="10.25" y="9.75" width="3.5" height="16" rx="1.5" />
        <!-- 人物頭部 -->
        <circle cx="39" cy="12" r="8" />
        <!-- 人物肩膀 -->
        <path d="M26,38 C26,27 31,24 39,24 C47,24 52,27 52,38 Z" />
      </svg>
    </button>
  </div>
</template>

<style scoped lang="scss">
.member-card-list {
  display: flex;
  flex-direction: column;
  gap: 24px;
  padding: 24px 0;

  :deep(.member-card + .member-card) {
    border-top: 1px solid $temple-border-light;
    padding-top: 24px;
  }
}

.add-member-btn {
  width: 100%;
  display: flex;
  justify-content: center;
  background: none;
  border: none;
  padding: 8px;
  cursor: pointer;
  color: $temple-text-muted;
  transition: color 0.2s;
  border-radius: 8px;

  &:hover {
    color: $temple-gold-primary;
  }

  svg {
    width: 96px;
    height: 68px;
    display: block;
  }
}
</style>
