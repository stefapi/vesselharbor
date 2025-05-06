<template>
  <div class="">
    <el-alert
      v-for="notification in notifications"
      :key="notification.id"
      :title="notification.message"
      :type="notification.type"
      :closable="true"
      @close="removeNotification(notification.id)"
      class=""
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
