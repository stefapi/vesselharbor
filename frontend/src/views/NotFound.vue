<!-- src/views/NotFound.vue -->
<template>
  <div class="min-h-screen flex flex-col items-center justify-center bg-gray-100 p-4">
    <h1 class="text-4xl font-bold mb-4">404 - Page non trouvée</h1>
    <p class="mb-6">La page que vous cherchez n'existe pas.</p>
    <router-link to="/" class="text-blue-500 hover:underline">
      Retourner à l'accueil
    </router-link>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
export default defineComponent({
  name: 'NotFound',
});
</script>

<style scoped>
/* Vous pouvez ajouter des styles complémentaires ici */
</style>
