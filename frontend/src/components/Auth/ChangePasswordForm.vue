<!-- src/components/ChangePasswordForm.vue -->
<template>
  <div class="u-w-full u-max-w-sm u-p-6 u-rounded-xl u-shadow u-bg-white">
    <form @submit.prevent="handleSubmit" class="u-space-y-4">
      <!-- Ancien mot de passe -->
      <el-form-item
        label="Ancien mot de passe"
        :error="OldPasswordError"
        class="u-w-full"
      >
        <el-input
          v-model="state.oldPassword"
          type="password"
          placeholder="Ancien mot de passe"
          @blur="v$.oldPassword.$touch()"
          show-password
        />
      </el-form-item>

      <!-- Nouveau mot de passe -->
      <el-form-item
        label="Nouveau mot de passe"
        :error="NewPasswordError"
        class="u-w-full"
      >
        <el-input
          v-model="state.newPassword"
          type="password"
          placeholder="Nouveau mot de passe"
          @blur="v$.newPassword.$touch()"
          show-password
        />
      </el-form-item>

      <!-- Bouton -->
      <el-button
        type="primary"
        native-type="submit"
        class="u-w-full"
      >
        Changer le mot de passe
      </el-button>
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
