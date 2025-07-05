<!-- src/components/Auth/LoginForm.vue -->
<template>
  <form @submit.prevent="handleSubmit" class="u-space-y-4">
    <!-- Champ Email -->
    <el-form-item label="Email" :error="EmailError">
      <el-input v-model="state.email" type="email" placeholder="Votre email" @blur="v$.email.$touch()" />
    </el-form-item>

    <!-- Champ Mot de passe -->
    <el-form-item label="Mot de passe" :error="PasswordError">
      <el-input v-model="state.password" type="password" placeholder="Votre mot de passe" @blur="v$.password.$touch()" show-password />
    </el-form-item>

    <!-- Bouton -->
    <el-button type="primary" native-type="submit" class="u-w-full"> Se connecter </el-button>
  </form>
</template>

<script setup lang="ts">
import { reactive, computed, unref } from 'vue'
import { useVuelidate } from '@vuelidate/core'
import { required, email, helpers } from '@vuelidate/validators'

const hasEmailError = computed(() => v$.value.email.$error)
const EmailError = computed(() => unref((v$.value.email.$error && v$.value.email?.$errors[0]?.$message) || ''))
const hasPasswordError = computed(() => v$.value.password.$error)
const PasswordError = computed(() => unref((v$.value.password.$error && v$.value.password?.$errors[0]?.$message) || ''))

interface Emits {
  (e: 'submit', payload: { isValid: boolean; credentials: { email: string; password: string } }): void
}

const emit = defineEmits<Emits>()

// State réactif local au composant
const state = reactive({
  email: '',
  password: '',
})

// Règles de validation
const validationRules = {
  email: {
    required: helpers.withMessage("L'email est requis", required),
    email: helpers.withMessage("L'email est invalide", email),
  },
  password: {
    required: helpers.withMessage('Le mot de passe est requis', required),
  },
}

const v$ = useVuelidate(validationRules, state)

const handleSubmit = async () => {
  const isValid = await v$.value.$validate()

  emit('submit', {
    isValid,
    credentials: {
      email: state.email,
      password: state.password,
    },
  })
}
</script>
