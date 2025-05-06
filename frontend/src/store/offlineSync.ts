import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getQueuedActions, clearQueuedAction } from '@/services/offlineQueue.ts'
import api from '@/services/api.ts'
import { useNotificationStore } from '@/store/notifications.ts'
import { isOfflineSyncEnabled } from '@/utils/env.ts'

export const useOfflineSyncStore = defineStore('offlineSync', () => {
  const pendingCount = ref(0)
  const isSyncing = ref(false)
  let intervalId: ReturnType<typeof setInterval> | null = null

  // ✅ Récupère les actions en attente
  async function updatePendingCount() {
    if (!isOfflineSyncEnabled) return
    const actions = await getQueuedActions()
    pendingCount.value = actions.length
  }

  // ✅ Lance la synchronisation manuelle
  async function syncNow() {
    if (!isOfflineSyncEnabled) return
    const notificationStore = useNotificationStore()
    const actions = await getQueuedActions()
    if (actions.length === 0) return

    isSyncing.value = true
    let success = 0
    let failed = 0

    for (const action of actions) {
      try {
        await api.request({
          method: action.method,
          url: action.url,
          data: action.data,
        })
        await clearQueuedAction(action.timestamp)
        success++
      } catch (e) {
        console.error(`Erreur sync: ${action.method} ${action.url}`, e)
        failed++
      }
    }

    isSyncing.value = false
    await updatePendingCount()

    if (success > 0) {
      notificationStore.addNotification({
        type: 'success',
        message: `${success} action${success > 1 ? 's' : ''} synchronisée${success > 1 ? 's' : ''}`,
      })
    }

    if (failed > 0) {
      notificationStore.addNotification({
        type: 'error',
        message: `${failed} action${failed > 1 ? 's' : ''} non synchronisée${failed > 1 ? 's' : ''}`,
      })
    }
  }

  // ✅ Boucle automatique
  function startAutoSyncLoop(interval = 5 * 60 * 1000) {
    if (!isOfflineSyncEnabled || intervalId) return
    intervalId = setInterval(() => {
      if (navigator.onLine) syncNow()
    }, interval)
  }

  function stopAutoSyncLoop() {
    if (intervalId) {
      clearInterval(intervalId)
      intervalId = null
    }
  }

  // ✅ Événement navigateur
  function initSyncListener() {
    if (!isOfflineSyncEnabled) return
    window.addEventListener('online', syncNow)
  }

  function stopSyncListener() {
    window.removeEventListener('online', syncNow)
  }

  return {
    pendingCount,
    isSyncing,
    syncNow,
    updatePendingCount,
    startAutoSyncLoop,
    stopAutoSyncLoop,
    initSyncListener,
    stopSyncListener,
  }
})
