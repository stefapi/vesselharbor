<template>
  <NotificationsList />
  <SyncStatusIndicator v-if="isOfflineSyncEnabled" />
  <!-- ⬇️ on rend le layout adapté, puis la vue à l’intérieur -->
  <component :is="layoutComponent">
    <router-view />
  </component>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'

import MainLayout from '@/layouts/MainLayout.vue'
import AuthLayout from '@/layouts/AuthLayout.vue'

import NotificationsList from '@/components/common/NotificationsList.vue'
import SyncStatusIndicator from '@/components/common/SyncStatusIndicator.vue'
import { isOfflineSyncEnabled } from '@/utils/env'

const route = useRoute()

/* Petit dictionnaire des layouts disponibles  */
const layouts = {
  main: MainLayout, // par défaut : barre latérale + header
  auth: AuthLayout, // pages publiques (login, register, etc.)
}

/* renvoie le composant layout demandé ou, sinon, MainLayout */
const layoutComponent = computed(() => {
  const key = route.meta.layout as keyof typeof layouts | undefined
  return layouts[key ?? 'main']
})
</script>
