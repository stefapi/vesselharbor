<!-- src/views/Auth/ForgotPasswordView.vue -->
<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-100">
    <VaCard class="w-full max-w-md p-6">
      <h1 class="text-xl font-bold mb-4 text-center">Mot de passe oublié</h1>
      <ForgotPasswordForm @submit="handleFormSubmit" />
      <router-link
        to="/login"
        class="block text-center text-primary hover:text-primary-dark transition-colors mt-4"
      >
        Retour à la connexion
      </router-link>
    </VaCard>
  </div>
</template>

<script setup lang="ts">
import { useNotificationStore } from '@/store/notifications';
import { useRouter } from 'vue-router';
import ForgotPasswordForm from '@/components/Auth/ForgotPasswordForm.vue';
import { isAxiosError } from '@/services/api';
import {reset_password} from "@/services/authService.js";

interface ForgotPasswordSubmitEvent {
  isValid: boolean
  email: string
}

const notificationStore = useNotificationStore();
const router = useRouter();

const handleFormSubmit = async (event: ForgotPasswordSubmitEvent) => {
  if (!event.isValid) {
    notificationStore.addNotification({
      type: 'error',
      message: 'Veuillez corriger les erreurs dans le formulaire'
    });
    return;
  }

  try {
    await reset_password_request(event.email );

    notificationStore.addNotification({
      type: 'success',
      message: 'Si cet email est enregistré, vous recevrez un lien de réinitialisation'
    });

    setTimeout(() => {
      router.push({ name: 'Login' });
    }, 150);

  } catch (error: unknown) {
    handlePasswordResetError(error);
  }
};

const handlePasswordResetError = (error: unknown) => {
  let errorMessage = "Erreur lors de la demande de réinitialisation";

  if (isAxiosError(error)) {
    errorMessage = error.response?.data?.message || errorMessage;
    if (error.response?.status === 404) {
      errorMessage = "Aucun compte associé à cet email";
    }
  }

  notificationStore.addNotification({
    type: 'error',
    message: errorMessage
  });
};

</script>
