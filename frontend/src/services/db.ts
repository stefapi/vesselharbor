// src/services/db.ts
import { openDB } from 'idb'

// 📦 Base unique avec tous les objectStores nécessaires
export const dbPromise = openDB('offline-cache', 3, {
  upgrade(db) {
    if (!db.objectStoreNames.contains('responses')) {
      db.createObjectStore('responses')
    }
    if (!db.objectStoreNames.contains('queue')) {
      db.createObjectStore('queue', { keyPath: 'timestamp' })
    }
  },
})
