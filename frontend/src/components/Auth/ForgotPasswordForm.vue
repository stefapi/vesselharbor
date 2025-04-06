<!-- src/components/Auth/ForgotPasswordForm.vue -->
<template>
  <form @submit.prevent="handleSubmit" class="space-y-4">
    <VaInput
      v-model="state.email"
      type="email"
      placeholder="Votre email"
      label="Email"
      :error="v$.email.$error && v$.email.$errors[0]?.$message"
      @blur="v$.email.$touch()"
      class="w-full"
    />

    <VaButton
      type="submit"
      color="primary"
      class="w-full"
    >
      Envoyer le lien de réinitialisation
    </VaButton>
  </form>
</template>

<script setup lang="ts">
import { reactive } from 'vue';
import { useVuelidate } from '@vuelidate/core';
import { required, email, helpers } from '@vuelidate/validators';

interface Emits {
  (e: 'submit', payload: { isValid: boolean; email: string }): void;
}

const emit = defineEmits<Emits>();

// State réactif local au composant
const state = reactive({
  email: '',
});

// Règles de validation
const validationRules = {
  email: {
    required: helpers.withMessage('L\'email est requis', required),
    email: helpers.withMessage('L\'email est invalide', email),
  },
};

const v$ = useVuelidate(validationRules, state);

// Soumission du formulaire
const handleSubmit = async () => {
  const isValid = await v$.value.$validate();

  emit('submit', {
    isValid,
    email: state.email
  });
};
</script>
