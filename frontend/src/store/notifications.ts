// src/store/notifications.ts
import { defineStore } from 'pinia'

export interface Notification {
  id: number
  type: 'success' | 'error' | 'info' | 'warning'
  message: string
}

export const useNotificationStore = defineStore('notifications', {
  state: () => ({
    notifications: [] as Notification[],
  }),
  actions: {
    addNotification(notification: Omit<Notification, 'id'>) {
      const id = Date.now()
      this.notifications.push({ ...notification, id })
      // Suppression automatique après 5 secondes
      setTimeout(() => {
        this.removeNotification(id)
      }, 5000)
    },
    removeNotification(id: number) {
      this.notifications = this.notifications.filter((n) => n.id !== id)
    },
  },
})
