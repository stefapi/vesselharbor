<!-- src/views/Auth/ForgotPasswordView.vue -->
<template>
  <div class="u-min-h-[calc(100vh-1rem)] u-w-full u-flex u-items-center u-justify-center u-bg-gray-100">
    <el-card class="u-w-full u-max-w-md">
      <h1 class="u-text-2xl u-font-bold u-text-center">Mot de passe oublié</h1>

      <ForgotPasswordForm @submit="handleFormSubmit" />

      <router-link
        to="/login"
        class="u-block u-text-center u-text-primary u-mt-4"
      >
        Retour à la connexion
      </router-link>
    </el-card>
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
