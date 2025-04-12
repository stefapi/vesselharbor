<!-- src/views/Auth/ResetPasswordView.vue -->
<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-100">
    <div class="w-full max-w-md">
      <VaCard class="p-6">
        <h1 class="text-xl font-bold mb-4 text-center">Réinitialisation du mot de passe</h1>
        <PasswordResetForm
          button-text="Réinitialiser"
          @submit="handlePasswordReset"
        />
        <router-link
          to="/login"
          class="block text-center text-primary hover:text-primary-dark transition-colors mt-4"
        >
          <va-icon name="arrow_back" class="mr-1" />
          Retour à la connexion
        </router-link>
      </VaCard>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useNotificationStore } from '@/store/notifications';
import { useRouter, useRoute } from 'vue-router';
import {isAxiosError} from '@/services/api';
import PasswordResetForm from '@/components/Auth/PasswordResetForm.vue';
import {reset_password} from "@/services/authService.js";

interface ResetPasswordSubmitEvent {
  isValid: boolean
  credentials: {
    newPassword: string
    confirmPassword: string
  }
}

const notificationStore = useNotificationStore();
const router = useRouter();
const route = useRoute();

const getResetToken = () => {
  // Récupération du token depuis l'URL
  const token = route.query.token as string;
  if (!token) {
    notificationStore.addNotification({
      type: 'error',
      message: 'Lien de réinitialisation invalide'
    });
    router.push({ name: 'Login' });
  }
  return token;
};


const handlePasswordReset = async (event: ResetPasswordSubmitEvent) => {
  const token = getResetToken();
  if (!token) return;
  if (!event.isValid) {
    notificationStore.addNotification({
      type: 'error',
      message: 'Veuillez corriger les erreurs dans le formulaire'
    });
    return;
  }

  try {
    await reset_password(token, event.credentials.newPassword);

    notificationStore.addNotification({
      type: 'success',
      message: 'Mot de passe réinitialisé avec succès'
    });

    setTimeout(() => {
      router.push({
        name: 'Login',
        query: { password_reset: 'success' }
      });
    }, 300);

  } catch (error: unknown) {
    handleResetError(error);
  }
};

const handleResetError = (error: unknown) => {
  let errorMessage = "Erreur lors de la réinitialisation du mot de passe";

  if (isAxiosError(error)) {
    errorMessage = error.response?.data?.message || errorMessage;
    if (error.response?.status === 401) {
      errorMessage = "Lien de réinitialisation invalide ou expiré";
    }
  }

  notificationStore.addNotification({
    type: 'error',
    message: errorMessage
  });
};
</script>
