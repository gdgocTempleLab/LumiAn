import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import './assets/styles/global.scss'

async function bootstrap() {
  if (import.meta.env.VITE_USE_MOCK === 'true') {
    const { setupMocks } = await import('./mock')
    setupMocks()
  }

  const app = createApp(App)
  app.use(createPinia())
  app.use(router)
  app.mount('#app')
}

bootstrap()
