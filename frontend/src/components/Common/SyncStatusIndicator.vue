<!-- src/components/Common/SyncStatusIndicator.vue -->
<template>
  <div class="u-relative">
    <el-tooltip :content="tooltipText" placement="bottom">
      <el-button link @click="syncStore.syncNow" :loading="false" class="u-relative">
        <!-- 🔁 En cours -->
        <i-material-symbols-autorenew
          v-if="syncStore.isSyncing"
          class="u-text-blue-500 u-text-xl u-animate-spin"
        />

        <!-- 🟡 En attente -->
        <template v-else-if="syncStore.pendingCount > 0">
          <i-material-symbols-sync-problem class="u-text-yellow-500 u-text-xl" />
          <span class="u-absolute u-top-0 u-right-0 u-bg-red-500 u-rounded-full u-w-2.5 u-h-2.5 u-border-2 u-border-white" />
        </template>

        <!-- ✅ OK -->
        <i-material-symbols-check-circle
          v-else
          class="u-text-green-500 u-text-xl"
        />
      </el-button>
    </el-tooltip>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useOfflineSyncStore } from '@/store/offlineSync.ts'

const syncStore = useOfflineSyncStore()

const tooltipText = computed(() => {
  if (syncStore.isSyncing) return 'Synchronisation en cours...'
  if (syncStore.pendingCount > 0)
    return `${syncStore.pendingCount} action${syncStore.pendingCount > 1 ? 's' : ''} en attente`
  return 'Tout est synchronisé'
})
</script>
