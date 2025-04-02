<template>
  <div class="dashboard">
    <h1>Bienvenue sur le Dashboard</h1>
    <p>Vous êtes connecté en tant que {{ authStore.user.email }}</p>
    <!-- Vous pouvez ajouter ici des liens ou des statistiques -->
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { useAuthStore } from '@/store/auth';

export default defineComponent({
  name: 'DashboardView',
  setup() {
    const authStore = useAuthStore();
    return { authStore };
  },
});
</script>

<style scoped>
.dashboard {
  padding: 2rem;
}
</style>

