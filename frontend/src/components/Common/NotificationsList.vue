<template>
  <div class="u-fixed u-top-4 u-right-4 u-z-50 u-space-y-2 u-max-w-sm">
    <el-alert
      v-for="notification in notifications"
      :key="notification.id"
      :title="notification.message"
      :type="notification.type"
      :closable="true"
      @close="removeNotification(notification.id)"
      show-icon
    />
  </div>
</template>

<script setup lang="ts">
import { useNotificationStore } from '@/store/notifications'
import { storeToRefs } from 'pinia'

const notificationStore = useNotificationStore()
const { notifications } = storeToRefs(notificationStore)

const removeNotification = (id: number) => {
  notificationStore.removeNotification(id)
}
</script>
