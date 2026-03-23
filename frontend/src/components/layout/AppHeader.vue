<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import logoMain from '@/assets/images/logo.png'
import logoWord from '@/assets/images/logo_word.png'
import logoPic from '@/assets/images/logo_pic.png'

const props = withDefaults(defineProps<{
  compact?: boolean
}>(), {
  compact: false,
})

const router = useRouter()
const authStore = useAuthStore()

async function handleLogout() {
  await authStore.logout()
  router.push('/login')
}
</script>

<template>
  <header class="app-header" :class="{ 'app-header--compact': compact }">
    <div class="header-content">
      <div class="header-brand" @click="router.push('/')">
        <img :src="logoPic" class="header-logo" alt="八卦禪寺" />
        <img :src="logoMain" class="header-title-img" alt="八卦禪寺" />
      </div>
      <div class="header-actions">
        <el-button text @click="handleLogout">
          <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" /><polyline points="16 17 21 12 16 7" /><line x1="21" y1="12" x2="9" y2="12" /></svg>
          登出
        </el-button>
      </div>
    </div>
    <div class="header-banner" v-if="!compact">
      <div class="banner-overlay">
        <div class="banner-brand">
          <img :src="logoPic" class="banner-logo" alt="八卦禪寺" />
          <div>
            <img :src="logoMain" class="banner-title-img" alt="八卦禪寺" />
            <img :src="logoWord" class="banner-subtitle-img" alt="信徒管理系統" />
          </div>
        </div>
      </div>
    </div>
  </header>
</template>

<style scoped lang="scss">
.app-header {
  width: 100%;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 24px;
  background: white;
  border-bottom: 1px solid $temple-border-light;
}

.header-brand {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
}

.header-logo {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
}

.header-title-img {
  height: 32px;
  width: auto;
}

.header-actions {
  :deep(.el-button) {
    color: $temple-text-muted;
    &:hover, &:focus {
      color: $temple-text-dark;
    }
  }
}

.header-banner {
  height: 280px;
  background: url('@/assets/images/temple.jpg') center/cover no-repeat;
  background-color: #3a3a3a;
  position: relative;
}

.banner-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.3);
  display: flex;
  align-items: center;
  padding: 40px;
}

.banner-brand {
  display: flex;
  align-items: center;
  gap: 20px;
}

.banner-logo {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  object-fit: cover;
}

.banner-title-img {
  height: 56px;
  width: auto;
  display: block;
}

.banner-subtitle-img {
  height: 36px;
  width: auto;
  display: block;
  margin-top: 8px;
  opacity: 0.9;
}

// --- Compact mode (subpages) ---
.app-header--compact {
  .header-content {
    background: #3a3a3a;
    border-bottom: none;
    justify-content: center;
    position: relative;
  }

  .header-content {
    padding: 0 24px;
  }

  .header-logo {
    width: 40px;
    height: 40px;
    border: 2px solid $temple-gold-primary;
  }

  .header-title-img {
    height: 88px;
    margin: -14px 0;
  }

  .header-actions {
    position: absolute;
    right: 24px;
    top: 50%;
    transform: translateY(-50%);

    :deep(.el-button) {
      color: white;
      &:hover, &:focus {
        color: white;
        background-color: rgba(255, 255, 255, 0.15);
      }
    }
  }
}

</style>
