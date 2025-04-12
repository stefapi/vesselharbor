<!-- src/App.vue -->
<template>
  <MainLayout class="u-min-h-screen u-bg-white u-text-gray-800">
  </MainLayout>
  <NotificationsList/>
</template>

<script setup lang="ts">
import MainLayout from '@/layouts/MainLayout.vue';
import NotificationsList from '@/components/Common/NotificationsList.vue';
</script>

<style lang="scss">
// Utilisation des variables CSS de Vuestic
#nprogress {
  &::before {
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    height: 3px;
    width: 100%;
    background-image: linear-gradient(
      90deg,
      var(--va-primary) 0%,
      var(--va-success) 50%,
      var(--va-primary) 100%
    );
    background-size: 200% auto;
    z-index: 9999;
    animation: nprogress-stripe 1.5s linear infinite;
  }

  @keyframes nprogress-stripe {
    0% {
      background-position: 200% 0;
    }
    100% {
      background-position: -200% 0;
    }
  }
}
</style>
