<!-- src/layouts/MainLayout.vue -->
<template>
  <div class="main-layout">
    <!-- Menu latéral affiché uniquement si l'utilisateur est authentifié -->
    <aside class="sidebar" v-if="isAuthenticated">
      <nav>
        <ul>
          <li><router-link to="/">Dashboard</router-link></li>
          <li><router-link to="/environments">Environnements</router-link></li>
          <li><router-link to="/groups">Groupes & Utilisateurs</router-link></li>
          <li><router-link to="/elements">Éléments</router-link></li>
          <li v-if="isSuperadmin">
            <router-link to="/audit-logs">Audit Logs</router-link>
          </li>
        </ul>
      </nav>
    </aside>
    <div class="content">
      <!-- En-tête avec bouton déconnexion visible uniquement pour les utilisateurs connectés -->
      <header v-if="isAuthenticated">
        <button @click="logout">Déconnexion</button>
      </header>
      <main>
        <router-view />
      </main>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, computed } from 'vue';
import { useAuthStore } from '@/store/auth';
import { useRouter } from 'vue-router';

export default defineComponent({
  name: 'MainLayout',
  setup() {
    const authStore = useAuthStore();
    const router = useRouter();

    const isAuthenticated = computed(() => authStore.isAuthenticated);
    const isSuperadmin = computed(() => authStore.user?.is_superadmin);

    const logout = () => {
      authStore.logout();
      router.push({ name: 'Login' });
    };

    return { isAuthenticated, isSuperadmin, logout };
  },
});
</script>

<style scoped>
.main-layout {
  display: flex;
  min-height: 100vh;
}

.sidebar {
  width: 200px;
  background-color: #f5f5f5;
  padding: 1rem;
}

.content {
  flex: 1;
  display: flex;
  flex-direction: column;
}

header {
  background-color: #fff;
  padding: 1rem;
  border-bottom: 1px solid #ccc;
}

main {
  flex: 1;
  padding: 1rem;
  overflow-y: auto;
}
</style>
