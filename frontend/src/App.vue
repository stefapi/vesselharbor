<!-- src/App.vue -->
<template>
  <MainLayout>
    <router-view />
  </MainLayout>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import MainLayout from '@/layouts/MainLayout.vue';

export default defineComponent({
  name: 'App',
  components: { MainLayout },
});
</script>

<style>
/* Exemple : barre fine en haut avec une couleur UnoCSS */
#nprogress::before {
  content: '';
  position: fixed;
  top: 0;
  left: 0;
  height: 3px;
  width: 100%;
  background-color: var(--nprogress-color, #3b82f6); /* tailwind blue-500 */
  z-index: 9999;
  animation: nprogress-stripe 2s linear infinite;
}

@keyframes nprogress-stripe {
  0% {
    background-position: 1rem 0;
  }
  100% {
    background-position: 0 0;
  }
}
</style>
