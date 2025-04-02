<!-- src/views/Auth/LoginView.vue -->
<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-100">
    <va-card class="w-full max-w-md p-6">
      <h1 class="text-2xl font-bold mb-4 text-center">Connexion</h1>
      <NotificationsList />
      <LoginForm @submit="handleFormSubmit" />
      <div class="mt-4 text-center">
        <router-link
          to="/forgot-password"
          class="va-text-primary va-link hover:va-link--hover"
        >
          Mot de passe oublié ?
        </router-link>
      </div>
    </va-card>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';
import { login } from "@/services/userService";
import { useNotificationStore } from '@/store/notifications';
import LoginForm from '@/components/Auth/LoginForm.vue';
import NotificationsList from '@/components/Common/NotificationsList.vue';
import type { AxiosError } from 'axios';

interface LoginSubmitEvent {
  isValid: boolean;
  credentials: {
    email: string;
    password: string;
  };
}

const notificationStore = useNotificationStore();
const router = useRouter();

const handleFormSubmit = async (event: LoginSubmitEvent) => {
  if (!event.isValid) {
    notificationStore.addNotification({
      type: 'error',
      message: 'Veuillez corriger les erreurs dans le formulaire'
    });
    return;
  }

  try {
    const response = await login({
      username: event.credentials.email,
      password: event.credentials.password,
    });

    localStorage.setItem('authToken', response.access_token);

    notificationStore.addNotification({
      type: 'success',
      message: 'Connexion réussie ! Redirection en cours...'
    });

    router.push({ name: 'Dashboard' });
  } catch (error: unknown) {
    handleLoginError(error);
  }
};

const handleLoginError = (error: unknown) => {
  let errorMessage = "Une erreur est survenue lors de la connexion";

  if (isAxiosError(error)) {
    errorMessage = error.response?.data?.message || errorMessage;
    if (error.response?.status === 401) {
      errorMessage = "Identifiants incorrects";
    }
  }

  notificationStore.addNotification({
    type: 'error',
    message: errorMessage
  });
};

const isAxiosError = (error: unknown): error is AxiosError => {
  return typeof error === 'object'
    && error !== null
    && 'isAxiosError' in error
    && (error as AxiosError).isAxiosError === true;
};
</script>
