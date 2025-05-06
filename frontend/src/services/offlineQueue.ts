// src/services/offlineQueue.ts
import { dbPromise } from './db.ts'

export type OfflineAction = {
  method: 'post' | 'put' | 'delete'
  url: string
  data?: any
  timestamp: number
  retries?: number
}

export async function queueOfflineAction(action: OfflineAction) {
  const db = await dbPromise
  await db.add('queue', action)
}

export async function getQueuedActions(): Promise<OfflineAction[]> {
  const db = await dbPromise
  return db.getAll('queue')
}

export async function clearQueuedAction(timestamp: number) {
  const db = await dbPromise
  await db.delete('queue', timestamp)
}

export async function incrementRetryCount(timestamp: number) {
  const db = await dbPromise
  const tx = db.transaction('queue', 'readwrite')
  const store = tx.objectStore('queue')

  const item = await store.get(timestamp)
  if (item) {
    item.retries = (item.retries || 0) + 1
    await store.put(item)
  }

  await tx.done
}
