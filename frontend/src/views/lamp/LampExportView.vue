<script setup lang="ts">
import { ref, onUnmounted, nextTick } from 'vue'
import { Search, Download } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import AppHeader from '@/components/layout/AppHeader.vue'
import PageTitleBar from '@/components/layout/PageTitleBar.vue'
import InlineDateRangePicker from '@/components/common/InlineDateRangePicker.vue'
import { useLampStore } from '@/stores/lamp'
import { getPdfMake } from '@/utils/pdf-fonts'
import { buildRosterPdfDefinition } from '@/utils/generate-roster-pdf'

const lampStore = useLampStore()

const now = new Date()
const startDate = ref(new Date(now.getFullYear(), now.getMonth(), 1))
const endDate = ref(new Date(now.getFullYear(), now.getMonth() + 2, 0))

const lampType = ref('')
const name = ref('')
const phoneType = ref('mobile')
const phone = ref('')
const loading = ref(false)

const pdfUrl = ref('')
const pdfPreviewRef = ref<HTMLDivElement>()
const pdfIframeRef = ref<HTMLIFrameElement>()

const lampTypes = [
  { label: '全部', value: '' },
  { label: '光明燈', value: '光明燈' },
  { label: '太歲燈', value: '太歲燈' },
  { label: '財神燈', value: '財神燈' },
  { label: '藥師燈', value: '藥師燈' },
  { label: '文昌燈', value: '文昌燈' },
]

function revokePdfUrl() {
  if (pdfUrl.value) {
    URL.revokeObjectURL(pdfUrl.value)
    pdfUrl.value = ''
  }
}

onUnmounted(revokePdfUrl)

async function handleSearch() {
  loading.value = true
  revokePdfUrl()
  try {
    const year = startDate.value.getFullYear()
    await lampStore.loadRoster({
      year,
      lampType: lampType.value || undefined,
    })

    if (lampStore.rosterData.length === 0) {
      ElMessage.warning('查無資料')
      return
    }

    const pdfMake = await getPdfMake()
    const docDef = buildRosterPdfDefinition(lampStore.rosterData, {
      year,
      lampType: lampType.value || undefined,
    })

    const blob = await pdfMake.createPdf(docDef).getBlob()
    pdfUrl.value = URL.createObjectURL(blob)

    await nextTick()
    pdfPreviewRef.value?.scrollIntoView({ behavior: 'smooth' })
  } catch {
    ElMessage.error('查詢或產生 PDF 失敗')
  } finally {
    loading.value = false
  }
}

function handleExport() {
  if (!pdfUrl.value) return
  const year = startDate.value.getFullYear()
  const a = document.createElement('a')
  a.href = pdfUrl.value
  a.download = `點燈清冊_${year}.pdf`
  a.click()
}
</script>

<template>
  <div class="lamp-export-page">
    <AppHeader compact />
    <PageTitleBar
      title="點燈"
      save-text="匯出"
      :save-disabled="!pdfUrl"
      @save="handleExport"
    />

    <main class="export-content">
      <div class="export-card">
        <h3 class="card-title">查詢清冊</h3>

        <InlineDateRangePicker
          v-model:start-date="startDate"
          v-model:end-date="endDate"
        />

        <div class="filter-row">
          <div class="filter-item">
            <label class="filter-label">燈種</label>
            <el-select v-model="lampType" class="lamp-type-select">
              <el-option
                v-for="t in lampTypes"
                :key="t.value"
                :label="t.label"
                :value="t.value"
              />
            </el-select>
          </div>

          <div class="filter-item">
            <label class="filter-label">姓名</label>
            <el-input v-model="name" class="name-input" />
          </div>

          <div class="filter-item filter-phone">
            <div class="phone-label-row">
              <label class="filter-label">電話</label>
              <el-radio-group v-model="phoneType" class="phone-radio">
                <el-radio value="mobile">手機</el-radio>
                <el-radio value="phone">市話</el-radio>
              </el-radio-group>
            </div>
            <el-input v-model="phone" class="phone-input" />
          </div>
        </div>

        <div class="search-action">
          <el-button class="search-btn" :loading="loading" @click="handleSearch">
            <el-icon v-if="!loading"><Search /></el-icon>
            查詢
          </el-button>
        </div>
      </div>

      <div v-if="pdfUrl" ref="pdfPreviewRef" class="pdf-preview-card">
        <div class="pdf-toolbar">
          <h3 class="pdf-title">查詢結果</h3>
          <el-button @click="handleExport">
            <el-icon><Download /></el-icon>
            下載
          </el-button>
        </div>
        <iframe
          ref="pdfIframeRef"
          :src="pdfUrl"
          class="pdf-iframe"
        />
      </div>
    </main>
  </div>
</template>

<style scoped lang="scss">
.lamp-export-page {
  min-height: 100vh;
  background: $temple-bg-cream;
}

.export-content {
  max-width: 800px;
  margin: 0 auto;
  padding: 32px 40px;
}

.export-card {
  background: white;
  border: 1px solid $temple-border-light;
  border-radius: 8px;
  padding: 32px;
}

.card-title {
  font-size: 18px;
  font-weight: bold;
  color: $temple-text-dark;
  text-align: center;
  margin-bottom: 24px;
}

.filter-row {
  display: flex;
  gap: 20px;
  align-items: flex-end;
  flex-wrap: wrap;
  margin-bottom: 20px;
}

.filter-item {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.filter-label {
  font-size: 13px;
  color: $temple-text-muted;
}

.lamp-type-select {
  width: 120px;
}

.name-input {
  width: 140px;
}

.filter-phone {
  flex: 1;
}

.phone-label-row {
  display: flex;
  align-items: center;
  gap: 8px;
}

.phone-radio {
  :deep(.el-radio) {
    margin-right: 8px;
  }
}

.phone-input {
  width: 100%;
}

.search-action {
  display: flex;
  justify-content: flex-end;
}

.search-btn {
  background: $temple-gold-primary;
  color: white;
  border: none;
  border-radius: 8px;
  padding: 8px 16px;

  &:hover,
  &:focus {
    background: $temple-gold-dark;
    color: white;
  }
}

.pdf-preview-card {
  background: white;
  border: 1px solid $temple-border-light;
  border-radius: 8px;
  padding: 20px;
  margin-top: 20px;
}

.pdf-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.pdf-title {
  font-size: 16px;
  font-weight: bold;
  color: $temple-text-dark;
}

.pdf-iframe {
  width: 100%;
  height: 600px;
  border: 1px solid $temple-border-light;
  border-radius: 4px;
}
</style>
