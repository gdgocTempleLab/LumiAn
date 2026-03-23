<script setup lang="ts">
import { type Component } from 'vue'
import { useRouter } from 'vue-router'

const props = defineProps<{
  icon: Component
  title: string
  description: string
  to: string
  color?: string
}>()

const router = useRouter()
</script>

<template>
  <div class="homepage-card" @click="router.push(props.to)">
    <div class="card-header">
      <el-icon :size="24" :style="{ color: color || '#C8A951' }">
        <component :is="icon" />
      </el-icon>
      <span class="card-title" :style="{ color: color || '#C8A951' }">
        {{ title }}
      </span>
    </div>
    <p class="card-desc">{{ description }}</p>
  </div>
</template>

<style scoped lang="scss">
.homepage-card {
  background: #FFFDF7;
  border: 1px solid $temple-border-light;
  border-radius: 12px;
  padding: 24px;
  min-height: 120px;
  cursor: pointer;
  position: relative;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  transition: box-shadow 0.3s;

  &:hover {
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);

    .card-header {
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      gap: 16px;
    }

    .card-header :deep(.el-icon) {
      transform: scale(2);
    }

    .card-title {
      font-size: 28px;
    }

    .card-desc {
      opacity: 0;
    }
  }
}

.card-header {
  position: absolute;
  top: 24px;
  left: 24px;
  display: flex;
  align-items: center;
  gap: 8px;
  transform: translate(0, 0);
  transition: top 0.3s cubic-bezier(0.4, 0, 0.2, 1),
              left 0.3s cubic-bezier(0.4, 0, 0.2, 1),
              transform 0.3s cubic-bezier(0.4, 0, 0.2, 1),
              gap 0.3s cubic-bezier(0.4, 0, 0.2, 1);

  :deep(.el-icon) {
    transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  }
}

.card-title {
  font-size: 18px;
  font-weight: bold;
  transition: font-size 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.card-desc {
  font-size: 14px;
  color: $temple-text-muted;
  padding-top: 40px;
  transition: opacity 0.3s;
}
</style>
