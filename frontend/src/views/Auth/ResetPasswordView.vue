<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-100">
    <div class="w-full max-w-md">
      <PasswordResetForm
        button-text="Réinitialiser"
        :on-submit="handlePasswordReset"
      />

      <div class="mt-6 text-center">
        <router-link
          to="/login"
          class="text-blue-500 hover:underline text-sm"
        >
          <va-icon name="arrow_back" class="mr-1" />
          Retour à la connexion
        </router-link>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import api from '@/services/api';
import PasswordResetForm from '@/components/PasswordResetForm.vue';

export default defineComponent({
  name: 'ResetPasswordView',
  components: { PasswordResetForm },
  setup() {
    const router = useRouter();
    const route = useRoute();
    const token = route.query.token as string;

    const handlePasswordReset = async (newPassword: string) => {
      try {
        await api.post('/users/reset_password', {
          token,
          new_password: newPassword
        });
        router.push({
          name: 'Login',
          query: { password_reset: 'success' }
        });
      } catch (error) {
        // L'erreur sera gérée automatiquement par le composant PasswordResetForm
        throw error;
      }
    };

    return { handlePasswordReset };
  },
});
</script>
