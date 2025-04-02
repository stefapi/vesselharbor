<!-- src/views/Auth/Notifications.vue -->
<template>
  <div class="notifications">
    <va-toast
      v-for="notification in notifications"
      :key="notification.id"
      :message="notification.message"
      position="top-right"
      :color="typeToColor[notification.type]"
      closeable
      @close="remove(notification.id)"
      class="notification-toast"
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
import { computed } from 'vue';

const store = useNotificationStore();
const notifications = computed(() => store.notifications);

const typeToColor = {
  success: 'success',
  error: 'danger',
  info: 'info',
  warning: 'warning'
};

// Icônes Material Design officielles
const typeToIcon = {
  success: 'mdi-check-circle',
  error: 'mdi-alert-circle',
  info: 'mdi-information',
  warning: 'mdi-alert'
};

const remove = (id: number) => store.removeNotification(id);
</script>

<style scoped>
.notifications {
  position: fixed;
  top: 1rem;
  right: 1rem;
  z-index: 10000;
  display: flex;
  flex-direction: column-reverse;
  gap: 0.5rem;
}

:deep(.notification-toast) {
  position: static !important;
  margin: 0 !important;
  transform: none !important;
}

/* Correction couleur des icônes */
:deep(.va-toast__icon) {
  color: inherit !important;
}
</style>
