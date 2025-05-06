// src/services/useOfflineCache.ts
import { dbPromise } from './db.ts'

export async function getCachedResponse<T = unknown>(key: string): Promise<T | undefined> {
  const db = await dbPromise
  return db.get('responses', key)
}

export async function setCachedResponse<T = unknown>(key: string, data: T): Promise<void> {
  const db = await dbPromise
  await db.put('responses', data, key)
}
