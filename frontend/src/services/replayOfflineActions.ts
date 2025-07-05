import { getQueuedActions, clearQueuedAction, incrementRetryCount } from './offlineQueue.ts'
import api, { isAxiosError } from './api.ts'
import { useNotificationStore } from '@/store/notifications.ts'
import { useOfflineSyncStore } from '@/store/offlineSync.ts'
import { isOfflineSyncEnabled } from '@/utils/env.ts'

export async function replayOfflineActions() {
  if (!isOfflineSyncEnabled) return

  const notificationStore = useNotificationStore()
  const syncStore = useOfflineSyncStore()
  const actions = await getQueuedActions()

  if (!actions.length) return

  let success = 0
  let failed = 0
  let invalid = 0
  let discarded = 0

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
      if (isAxiosError(e) && e.response?.status === 400) {
        // ❌ Requête invalide (400) → suppression immédiate
        await clearQueuedAction(action.timestamp)
        invalid++
        notificationStore.addNotification({
          type: 'warning',
          message: `Requête invalide supprimée : ${action.method.toUpperCase()} ${action.url}`,
        })
      } else {
        const retries = action.retries ?? 0
        if (retries >= 2) {
          // ❌ Après 3 tentatives → abandon
          await clearQueuedAction(action.timestamp)
          discarded++
          notificationStore.addNotification({
            type: 'error',
            message: `Requête abandonnée après 3 échecs : ${action.method.toUpperCase()} ${action.url}`,
          })
        } else {
          // 🔁 Réessai possible → incrémenter le compteur
          await incrementRetryCount(action.timestamp)
          failed++
          console.warn(`[OfflineSync] Échec temporaire : ${action.method.toUpperCase()} ${action.url} (tentative ${retries + 1}/3)`)
        }
      }
    }
  }

  await syncStore.updatePendingCount()

  if (success > 0) {
    notificationStore.addNotification({
      type: 'success',
      message: `${success} action${success > 1 ? 's' : ''} synchronisée${success > 1 ? 's' : ''} avec succès`,
    })
  }

  if (failed > 0) {
    notificationStore.addNotification({
      type: 'info',
      message: `${failed} tentative${failed > 1 ? 's' : ''} reportée${failed > 1 ? 's' : ''}`,
    })
  }

  if (invalid > 0) {
    notificationStore.addNotification({
      type: 'warning',
      message: `${invalid} requête${invalid > 1 ? 's' : ''} invalide supprimée`,
    })
  }

  if (discarded > 0) {
    notificationStore.addNotification({
      type: 'error',
      message: `${discarded} requête${discarded > 1 ? 's' : ''} abandonnée après 3 échecs`,
    })
  }
}
