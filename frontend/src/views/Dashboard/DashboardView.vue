<template>
  <VaCard class="p-4 max-w-800px mx-auto">
    <VaCardTitle class="mb-4 text-center">Bienvenue sur le Dashboard</VaCardTitle>
    <VaCardContent>
      <p class="text-lg">
        Vous êtes connecté en tant que
        <span class="font-semibold text-primary">{{ authStore.user.email }}</span>
      </p>
    </VaCardContent>
    <!-- Ajoutez ici des composants Vuestic pour les statistiques -->
  </VaCard>
</template>

<script setup lang="ts">
import { useAuthStore } from '@/store/auth'

const authStore = useAuthStore()
</script>
