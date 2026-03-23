<script setup lang="ts">
defineProps<{
  visible: boolean
  title?: string
  message: string
  confirmText?: string
  cancelText?: string
  loading?: boolean
}>()

const emit = defineEmits<{
  'update:visible': [value: boolean]
  confirm: []
  cancel: []
}>()

function handleClose() {
  emit('update:visible', false)
  emit('cancel')
}
</script>

<template>
  <el-dialog
    :model-value="visible"
    :title="title || '確認'"
    width="400px"
    @close="handleClose"
  >
    <p>{{ message }}</p>

    <template #footer>
      <el-button @click="handleClose">
        {{ cancelText || '取消' }}
      </el-button>
      <el-button
        type="danger"
        :loading="loading"
        @click="emit('confirm')"
      >
        {{ confirmText || '確認刪除' }}
      </el-button>
    </template>
  </el-dialog>
</template>
