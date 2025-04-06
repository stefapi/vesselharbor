<!-- src/components/Auth/LoginForm.vue -->
<template>
  <div class="w-full max-w-sm p-6 rounded-xl shadow bg-white">
    <form @submit.prevent="handleSubmit" class="space-y-4">
      <!-- Champs avec validation intégrée -->
      <VaInput
        v-model="state.email"
        type="email"
        placeholder="Votre email"
        label="Email"
        :error="hasEmailError"
        :error-messages="EmailError"
        @blur="v$.email.$touch()"
        class="w-full"
        :class="{ 'va-input--error': v$.email.$error }"
      />
      <VaInput
        v-model="state.password"
        type="password"
        placeholder="Votre mot de passe"
        label="Mot de passe"
        :error="hasPasswordError"
        :error-messages="PasswordError"
        @blur="v$.password.$touch()"
        class="w-full"
      />

      <VaButton type="submit" color="primary" class="w-full">
        Se connecter
      </VaButton>
    </form>
  </div>
</template>

<script setup lang="ts">
import { reactive, computed } from 'vue';
import { useVuelidate } from '@vuelidate/core';
import { required, email, helpers } from '@vuelidate/validators';

const hasEmailError = computed(() => v$.value.email.$error);
const EmailError = computed(() => (v$.value.email.$error && v$.value.email?.$errors[0]?.$message) || '');
const hasPasswordError = computed(() => v$.value.password.$error);
const PasswordError = computed(() => (v$.value.password.$error && v$.value.password?.$errors[0]?.$message) || '');

interface Emits {
  (e: 'submit', payload: { isValid: boolean; credentials: { email: string; password: string } }): void;
}

const emit = defineEmits<Emits>();

// State réactif local au composant
const state = reactive({
  email: '',
  password: '',
});

// Règles de validation
const validationRules = {
  email: {
    required: helpers.withMessage("L'email est requis", required),
    email: helpers.withMessage("L'email est invalide", email)
  },
  password: {
    required: helpers.withMessage("Le mot de passe est requis", required)
  },
};

const v$ = useVuelidate(validationRules, state);

const handleSubmit = async () => {
  const isValid = await v$.value.$validate();

  emit('submit', {
    isValid,
    credentials: {
      email: state.email,
      password: state.password
    }
  });
};
</script>
