<script lang="ts">
import { defineComponent, ref, watch, computed } from 'vue'
import { ElMessage } from 'element-plus'
import * as lampApi from '@/api/lamp'
import { useLampStore } from '@/stores/lamp'

export default defineComponent({
  name: 'MemberLampStatusDialog',
  props: {
    modelValue: { type: Boolean, required: true },
    memberId: { type: [Number, String], required: true },
    year: { type: Number, required: true },
    householdId: { type: [Number, String], required: true },
  },
  emits: ['update:modelValue', 'saved'],
  setup(props, { emit }) {
    const lampStore = useLampStore()
    const loading = ref(false)
    const lampRows = ref<any[]>([])

    const visible = computed({
      get: () => props.modelValue,
      set: (v: boolean) => emit('update:modelValue', v),
    })

    async function loadStatuses() {
      if (!props.memberId) return
      loading.value = true
      try {
        const res = await lampApi.getMemberLightingStatus(props.memberId, props.year)
        const raw = (res.data.Data ?? []) as Record<string, unknown>[]
        lampRows.value = raw.map((r) => ({
          lampTypeId: r.Lamp_Type_ID,
          lampType: r.Lamp_Type,
          price: r.Price,
          isLit: Boolean(r.Is_Lit),
          lightingRecordId: r.Lighting_Record_ID || null,
          amount: Number(r.Price || 0),
        }))
      } catch (e) {
        lampRows.value = []
      } finally {
        loading.value = false
      }
    }

    watch(
      () => [props.modelValue, props.memberId, props.year],
      () => {
        if (props.modelValue) loadStatuses()
      }
    )

    async function toggleLamp(row: any) {
      if (!props.householdId) {
        ElMessage.error('缺少戶口資訊')
        return
      }

      try {
        loading.value = true
        if (row.isLit) {
          await lampApi.createLightingRecord({
            Household_ID: props.householdId,
            Member_ID: props.memberId,
            Lamp_Type_IDs: [row.lampTypeId],
            Year: props.year,
            Amount: row.amount || row.price || 0,
          })
          ElMessage.success('已新增燈種')
        } else {
          if (row.lightingRecordId) {
            await lampApi.deleteLightingRecord(row.lightingRecordId, props.memberId)
            ElMessage.success('已取消燈種')
          }
        }
        await loadStatuses()
        emit('saved')
      } catch (e) {
        console.error(e)
        ElMessage.error('同步失敗')
      } finally {
        loading.value = false
      }
    }

    async function updateAmount(row: any) {
      if (!row.lightingRecordId) return
      try {
        loading.value = true
        await lampApi.updateLightingRecord(row.lightingRecordId, {
          Member_ID: props.memberId,
          Year: props.year,
          Amount: row.amount,
        })
        ElMessage.success('已更新金額')
        await loadStatuses()
        emit('saved')
      } catch (e) {
        console.error(e)
        ElMessage.error('更新金額失敗')
      } finally {
        loading.value = false
      }
    }

    function close() {
      emit('update:modelValue', false)
    }

    return {
      lampStore,
      loading,
      lampRows,
      visible,
      loadStatuses,
      toggleLamp,
      updateAmount,
      close,
    }
  },
})
</script>

<template>
  <el-dialog :model-value="visible" title="編輯戶員點燈" width="640px" @close="close">
    <div v-loading="loading">
      <el-table :data="lampRows" style="width:100%" size="small" border>
        <el-table-column prop="lampType" label="燈種" />
        <el-table-column prop="price" label="價格" width="100">
          <template #default="{ row }">{{ row.price }}</template>
        </el-table-column>
        <el-table-column label="啟用" width="100">
          <template #default="{ row }">
            <el-switch v-model="row.isLit" @change="() => toggleLamp(row)" />
          </template>
        </el-table-column>
        <el-table-column label="金額" width="160">
          <template #default="{ row }">
            <el-input-number v-model="row.amount" :min="0" @change="() => updateAmount(row)" />
          </template>
        </el-table-column>
      </el-table>
    </div>
    <template #footer>
      <el-button @click="close">關閉</el-button>
    </template>
  </el-dialog>
</template>

<style scoped>
.el-table .el-switch { display: inline-flex }
</style>
