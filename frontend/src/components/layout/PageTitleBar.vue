<script setup lang="ts">
import { useRouter } from 'vue-router'

const props = withDefaults(defineProps<{
  title: string
  showSave?: boolean
  showCancel?: boolean
  saveText?: string
  cancelText?: string
  loading?: boolean
  saveDisabled?: boolean
  cancelDisabled?: boolean
  cancelGoBack?: boolean
}>(), {
  showSave: true,
  showCancel: true,
  saveDisabled: false,
  cancelDisabled: false,
  cancelGoBack: true,
})

const emit = defineEmits<{
  save: []
  cancel: []
}>()

const router = useRouter()

function handleCancel() {
  emit('cancel')
  if (props.cancelGoBack) {
    router.back()
  }
}
</script>

<template>
  <div class="page-title-bar">
    <h2 class="page-title">{{ title }}</h2>
    <div class="page-actions">
      <el-button
        v-if="showCancel"
        :disabled="cancelDisabled"
        @click="handleCancel"
      >
        {{ cancelText || '取消' }}
      </el-button>
      <el-button
        v-if="showSave"
        type="primary"
        :disabled="saveDisabled"
        :loading="loading"
        @click="emit('save')"
      >
        {{ saveText || '存檔' }}
      </el-button>
    </div>
  </div>
</template>

<style scoped lang="scss">
.page-title-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 40px;
  position: relative;

  &::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 40px;
    right: 40px;
    height: 1px;
    background-color: $temple-border-light;
  }
}

.page-title {
  font-size: 22px;
  font-weight: bold;
  color: $temple-text-dark;
}

.page-actions {
  display: flex;
  gap: 8px;

  :deep(.el-button) {
    border-radius: 8px;
    padding: 8px 20px;
    border: none;
    font-size: 14px;

    &:not(.el-button--primary) {
      background: #888;
      color: white;

      &:hover {
        background: #777;
      }

      &.is-disabled {
        opacity: 0.5;
        cursor: not-allowed;

        &:hover {
          background: #888;
        }
      }
    }

    &.el-button--primary {
      background: $temple-gold-primary;
      color: white;

      &:hover {
        background: $temple-gold-dark;
      }

      &.is-disabled {
        opacity: 0.5;
        cursor: not-allowed;

        &:hover {
          background: $temple-gold-primary;
        }
      }
    }
  }
}
</style>
