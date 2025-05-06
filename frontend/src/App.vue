<template>
  <NotificationsList />
  <SyncStatusIndicator v-if="isOfflineSyncEnabled" />
  <MainLayout>
    <router-view />
  </MainLayout>
</template>

<script setup lang="ts">
import MainLayout from '@/layouts/MainLayout.vue'
import NotificationsList from '@/components/Common/NotificationsList.vue'
import SyncStatusIndicator from '@/components/Common/SyncStatusIndicator.vue'
import { isOfflineSyncEnabled } from '@/utils/env'
</script>
