<!-- src/components/Auth/ForgotPasswordForm.vue -->
<template>
  <form @submit.prevent="handleSubmit" class="u-space-y-4">
    <el-form-item :error="EmailError" label="Email">
      <el-input v-model="state.email" type="email" placeholder="Votre email" @blur="v$.email.$touch()" />
    </el-form-item>

    <el-button type="primary" native-type="submit" class="u-w-full"> Envoyer le lien de réinitialisation </el-button>
  </form>
</template>

<script setup lang="ts">
import { reactive, computed, unref } from 'vue'
import { useVuelidate } from '@vuelidate/core'
import { required, email, helpers } from '@vuelidate/validators'

interface Emits {
  (e: 'submit', payload: { isValid: boolean; email: string }): void
}

const emit = defineEmits<Emits>()

// State réactif local au composant
const state = reactive({
  email: '',
})

// Règles de validation
const validationRules = {
  email: {
    required: helpers.withMessage("L'email est requis", required),
    email: helpers.withMessage("L'email est invalide", email),
  },
}

const v$ = useVuelidate(validationRules, state)

// Computed properties for error handling
const EmailError = computed(() => unref((v$.value.email.$error && v$.value.email?.$errors[0]?.$message) || ''))

// Soumission du formulaire
const handleSubmit = async () => {
  const isValid = await v$.value.$validate()

  emit('submit', {
    isValid,
    email: state.email,
  })
}
</script>
