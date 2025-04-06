<!-- src/components/ChangePasswordForm.vue -->
<template>
  <div class="w-full max-w-sm p-6 rounded-xl shadow bg-white">
    <form @submit.prevent="handleSubmit" class="space-y-4">
      <VaInput
        v-model="state.oldPassword"
        type="password"
        placeholder="Ancien mot de passe"
        label="Ancien mot de passe"
        :error="v$.oldPassword.$error && v$.oldPassword.$errors[0]?.$message"
        @blur="v$.oldPassword.$touch()"
        class="w-full"
      />
      <VaInput
        v-model="state.newPassword"
        type="password"
        placeholder="Nouveau mot de passe"
        label="Nouveau mot de passe"
        :error="v$.newPassword.$error && v$.newPassword.$errors[0]?.$message"
        @blur="v$.newPassword.$touch()"
        class="w-full"
      />

      <VaButton type="submit" color="primary" class="w-full">
        Changer le mot de passe
      </VaButton>
    </form>
  </div>
</template>

<script setup lang="ts">
import { reactive } from 'vue';
import { useVuelidate } from '@vuelidate/core';
import { required, minLength, helpers } from '@vuelidate/validators';
import { changePassword } from '@/services/userService';
import { useAuthStore } from '@/store/auth';
import { useNotificationStore } from '@/store/notifications';

const authStore = useAuthStore();
const notificationStore = useNotificationStore();

// State réactif
const state = reactive({
  oldPassword: '',
  newPassword: '',
});

// Règles de validation
const validationRules = {
  oldPassword: {
    required: helpers.withMessage('Ancien mot de passe requis', required),
  },
  newPassword: {
    required: helpers.withMessage('Nouveau mot de passe requis', required),
    minLength: helpers.withMessage(
      'Minimum 6 caractères',
      minLength(6)
    ),
  },
};

const v$ = useVuelidate(validationRules, state);

const handleSubmit = async () => {
  const isValid = await v$.value.$validate();

  if (!isValid) return;

  try {
    await changePassword(authStore.user!.id, {
      old_password: state.oldPassword,
      new_password: state.newPassword
    });

    notificationStore.addNotification({
      type: 'success',
      message: 'Mot de passe mis à jour'
    });

    // Réinitialisation du formulaire
    state.oldPassword = '';
    state.newPassword = '';
    v$.value.$reset();

  } catch (error) {
    notificationStore.addNotification({
      type: 'error',
      message: 'Erreur lors du changement de mot de passe'
    });
  }
};
</script>
