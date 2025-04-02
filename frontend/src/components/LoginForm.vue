<!-- src/views/Auth/LoginForm.vue -->
<template>
  <div class="w-full max-w-sm p-6 rounded-xl shadow bg-white">
    <!-- Composant Notifications -->
    <Notifications />

    <form @submit.prevent="submit" class="space-y-4">
      <VaInput
        v-model="state.email"
        type="email"
        placeholder="Votre email"
        label="Email"
        :error="v$.email.$error && v$.email.$errors[0]?.$message"
        @blur="v$.email.$touch()"
        class="w-full"
      />
      <VaInput
        v-model="state.password"
        type="password"
        placeholder="Votre mot de passe"
        label="Mot de passe"
        :error="v$.password.$error && v$.password.$errors[0]?.$message"
        @blur="v$.password.$touch()"
        class="w-full"
      />
      <VaButton type="submit" color="primary" class="w-full">Se connecter</VaButton>
    </form>
  </div>
</template>

<script setup>
import { reactive } from 'vue';
import useVuelidate from '@vuelidate/core';
import {required, email, helpers} from '@vuelidate/validators';
import { login } from "@/services/userService";
import { useNotificationStore } from '@/store/notifications';

const state = reactive({
  email: '',
  password: '',
});

const rules = {
  email: {     required: helpers.withMessage("L'email est requis", required),
    email: helpers.withMessage("L'email est invalide", email) },
  password: { required: helpers.withMessage("Le mot de passe est requis", required) },
};

const v$ = useVuelidate(rules, state);
const notificationStore = useNotificationStore();

const submit = async () => {
  const isValid = await v$.value.$validate();
  if (!isValid) {
    // Ajouter une notification d'erreur pour les champs invalides
    notificationStore.addNotification({
      type: 'error',
      message: 'Veuillez corriger les erreurs dans le formulaire'
    });
    return;
  }

  try {
    const response = await login({
      username: state.email,
      password: state.password,
    });
    localStorage.setItem('authToken', response.access_token);

    // Notification de succès
    notificationStore.addNotification({
      type: 'success',
      message: 'Connexion réussie ! Redirection en cours...'
    });

  } catch (error) {
    let errorMessage = "Une erreur est survenue lors de la connexion";

    if (error.response?.status === 400) {
      errorMessage = error.response.data.message || errorMessage;
    } else if (error.response?.status === 401) {
      errorMessage = "Identifiants incorrects";
    }

    // Notification d'erreur
    notificationStore.addNotification({
      type: 'error',
      message: errorMessage
    });

    console.error("Erreur lors de la connexion", error);
  }
};
</script>
