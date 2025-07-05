<template>
  <h2 class="u-text-center u-text-2xl u-font-semibold u-mb-6">Bienvenue sur le Dashboard</h2>
  <p class="u-text-lg u-text-gray-700 dark:u-text-gray-300">
    Vous êtes connecté en tant que
    <span class="u-font-semibold u-text-primary">{{ authStore.user?.email }}</span>
  </p>
  <!-- ✨ Ajoutez ici des composants pour les statistiques -->
</template>

<script setup lang="ts">
import { useAuthStore } from '@/store/auth'

const authStore = useAuthStore()
</script>
