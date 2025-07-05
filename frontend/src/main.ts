// src/main.ts
import { createApp } from 'vue'
import App from '@/App.vue'
import router from '@/router/index.js'
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
// ✅ Element Plus styles - doivent être chargés avant UnoCSS
import 'element-plus/dist/index.css'
// ✅ UnoCSS avec preset Element Plus
import 'virtual:uno.css'
import '@/styles/unocss.css'
import NProgress from 'nprogress'
import 'nprogress/nprogress.css'
import '@/styles/nprogress.css'
import 'material-icons/iconfont/material-icons.css'
import { createHead } from '@unhead/vue/client'
import { useOfflineSyncStore } from '@/store/offlineSync.ts'
import { isOfflineSyncEnabled } from '@/utils/env.ts'

const app = createApp(App)

NProgress.configure({ showSpinner: true })

const pinia = createPinia()
pinia.use(piniaPluginPersistedstate.default || piniaPluginPersistedstate)
const head = createHead()
app.use(head)
app.use(pinia)
app.use(router)

app.mount('#app')

// ✅ Initialisation de la synchronisation offline (si activée)
if (isOfflineSyncEnabled) {
  const syncStore = useOfflineSyncStore()
  // 1. Charge le nombre d’actions en attente
  syncStore.updatePendingCount()
  // 2. Démarre la boucle automatique (toutes les 5 min)
  syncStore.startAutoSyncLoop()
  // 3. Réagit au retour en ligne
  syncStore.initSyncListener()
}
