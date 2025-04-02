<!-- src/components/Common/NotificationsList.vue -->
<template>
  <div class="notifications">
    <va-toast
      v-for="notification in notifications"
      :key="notification.id"
      :message="notification.message"
      position="top-right"
      :color="typeToColor[notification.type]"
      closeable
      @close="removeNotification(notification.id)"
      class="notification-toast"
      :offset="16"
    >
      <template #icon>
        <va-icon
          :name="typeToIcon[notification.type]"
          :color="typeToColor[notification.type]"
          size="small"
        />
      </template>
    </va-toast>
  </div>
</template>

<script setup lang="ts">
import { useNotificationStore } from '@/store/notifications';
import { storeToRefs } from 'pinia';

const notificationStore = useNotificationStore();
const { notifications } = storeToRefs(notificationStore);

const typeToColor = {
  success: 'success',
  error: 'danger',
  info: 'info',
  warning: 'warning'
};

const typeToIcon = {
  success: 'mdi-check-circle',
  error: 'mdi-alert-circle',
  info: 'mdi-information',
  warning: 'mdi-alert'
};

const removeNotification = (id: number) => {
  notificationStore.removeNotification(id);
};
</script>
