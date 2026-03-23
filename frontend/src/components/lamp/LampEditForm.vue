<script setup lang="ts">
import { reactive, ref } from 'vue'
import { ElMessage } from 'element-plus'
import type { LampRecord } from '@/types'

const props = defineProps<{
  records: LampRecord[]
  memberName: string
}>()

const emit = defineEmits<{
  save: [record: LampRecord]
  add: [data: { memberId: number; lampType: string; amount: number }]
}>()

const lampTypes = ['光明燈', '太歲燈', '藥師燈', '財神燈', '文昌燈', '安太歲']

const adding = ref(false)
const newLamp = reactive({
  lampType: '',
  amount: 500,
})

function handleSaveRecord(record: LampRecord) {
  emit('save', record)
  ElMessage.success('更新成功')
}

function handleAddLamp() {
  if (!newLamp.lampType) {
    ElMessage.warning('請選擇燈種')
    return
  }
  emit('add', {
    memberId: props.records[0]?.memberId || 0,
    lampType: newLamp.lampType,
    amount: newLamp.amount,
  })
  adding.value = false
  newLamp.lampType = ''
  newLamp.amount = 500
}
</script>

<template>
  <div class="lamp-edit-form">
    <h4 class="member-name">{{ memberName }}</h4>

    <div v-for="record in records" :key="record.id" class="lamp-item">
      <span class="lamp-type">{{ record.lampType }}</span>
      <el-input-number v-model="record.amount" :min="0" :step="100" size="small" />
      <el-checkbox v-model="record.isPaid">已繳費</el-checkbox>
      <el-input v-model="record.notes" placeholder="備註" size="small" class="notes-input" />
      <el-button type="primary" size="small" @click="handleSaveRecord(record)">儲存</el-button>
    </div>

    <div v-if="adding" class="lamp-item new-lamp">
      <el-select v-model="newLamp.lampType" placeholder="選擇燈種" size="small">
        <el-option v-for="t in lampTypes" :key="t" :label="t" :value="t" />
      </el-select>
      <el-input-number v-model="newLamp.amount" :min="0" :step="100" size="small" />
      <el-button type="primary" size="small" @click="handleAddLamp">確定</el-button>
      <el-button size="small" @click="adding = false">取消</el-button>
    </div>

    <el-button v-if="!adding" text type="primary" size="small" @click="adding = true">
      + 新增燈種
    </el-button>
  </div>
</template>

<style scoped lang="scss">
.lamp-edit-form {
  background: white;
  border: 1px solid $temple-border-light;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 16px;
}

.member-name {
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 12px;
  color: $temple-text-dark;
}

.lamp-item {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
}

.lamp-type {
  min-width: 80px;
  font-weight: 500;
}

.notes-input {
  max-width: 150px;
}
</style>
