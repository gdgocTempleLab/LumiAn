<script setup lang="ts">
import AppHeader from '@/components/layout/AppHeader.vue'
import HomepageCard from '@/components/common/HomepageCard.vue'
import {
  Plus,
  EditPen,
  Sunrise,
  Document,
  Printer,
  User,
} from '@element-plus/icons-vue'

const sections = [
  {
    title: '信徒',
    cards: [
      { icon: Plus, title: '建立', description: '建立信徒資料', to: '/member/create' },
      { icon: EditPen, title: '編輯', description: '編輯信徒資料', to: '/member/edit' },
    ],
  },
  {
    title: '點燈',
    cards: [
      { icon: Plus, title: '點燈', description: '新增點燈紀錄', to: '/lamp/edit' },
      { icon: Document, title: '匯出', description: '匯出點燈清冊', to: '/lamp/export' },
      { icon: Printer, title: '列印', description: '列印信徒燈條', to: '/lamp/print-strip' },
    ],
  },
  {
    title: '帳號',
    cards: [
      { icon: User, title: '帳號', description: '管理帳號資料', to: '/account' },
    ],
  },
]
</script>

<template>
  <div class="home-page">
    <AppHeader compact />

    <main class="home-content">
      <section v-for="section in sections" :key="section.title" class="home-section">
        <h3 class="section-title">{{ section.title }}</h3>
        <div class="section-divider"></div>
        <div class="section-cards">
          <HomepageCard
            v-for="card in section.cards"
            :key="card.to"
            :icon="card.icon"
            :title="card.title"
            :description="card.description"
            :to="card.to"
          />
        </div>
      </section>
    </main>
  </div>
</template>

<style scoped lang="scss">
.home-page {
  min-height: 100vh;
  background: $temple-bg-cream;
}

.home-content {
  max-width: 900px;
  margin: 0 auto;
  padding: 40px 24px;
}

.home-section {
  margin-bottom: 48px;
}

.section-title {
  font-size: 18px;
  font-weight: bold;
  color: $temple-gold-primary;
  margin-bottom: 0;
}

.section-divider {
  height: 1px;
  background-color: $temple-border-light;
  margin: 12px 0 20px 0;
}

.section-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 20px;
}
</style>
