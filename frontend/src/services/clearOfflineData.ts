// src/services/clearOfflineData.ts
import { dbPromise } from './db.ts'

export async function clearAllOfflineData() {
  const db = await dbPromise

  const stores = ['responses', 'queue']

  for (const store of stores) {
    if (db.objectStoreNames.contains(store)) {
      const tx = db.transaction(store, 'readwrite')
      await tx.objectStore(store).clear()
      await tx.done
      console.info(`[Offline] Données supprimées du store "${store}"`)
    }
  }
}
