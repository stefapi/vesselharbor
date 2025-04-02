<!-- src/views/Auth/LoginView.vue -->
<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-100">
    <VaCard class="w-full max-w-md p-6">
      <h1 class="text-2xl font-bold mb-4 text-center">Connexion</h1>
      <LoginForm @loginSuccess="onLoginSuccess" />
      <div class="mt-4 text-center">
        <router-link to="/forgot-password" class="text-blue-500 hover:underline">
          Mot de passe oublié ?
        </router-link>
      </div>
    </VaCard>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { useRouter } from 'vue-router';
import LoginForm from "@/components/LoginForm.vue";

export default defineComponent({
  name: 'LoginView',
  components: { LoginForm },
  setup() {
    const router = useRouter();

    const onLoginSuccess = () => {
      // Rediriger l'utilisateur vers le Dashboard après une connexion réussie
      router.push({ name: 'Dashboard' });
    };

    return { onLoginSuccess };
  },
});
</script>

<style scoped>
/* Utilisation de classes UnoCSS pour la mise en page */
</style>
