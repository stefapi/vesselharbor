<template>
  <div class="w-full max-w-sm p-6 rounded-xl shadow bg-white">
    <form @submit.prevent="handlesubmit" class="space-y-4">
      <VaInput
        v-model="state.newPassword"
        type="password"
        label="Nouveau mot de passe"
        placeholder="••••••"
        :error="v$.newPassword.$error"
        :error-messages="v$.newPassword.$error && v$.newPassword.$errors[0]?.$message || ''"
        @blur="v$.newPassword.$touch()"
        class="w-full"
      />

      <VaInput
        v-model="state.confirmPassword"
        type="password"
        label="Confirmer le mot de passe"
        placeholder="••••••"
        :error="v$.confirmPassword.$error"
        :error-messages="v$.confirmPassword.$error && v$.confirmPassword.$errors[0]?.$message|| ''"
        @blur="v$.confirmPassword.$touch()"
        class="w-full"
      />

      <VaButton
        type="submit"
        color="primary"
        class="w-full"
      >
        {{ buttonText }}
      </VaButton>
    </form>
  </div>
</template>

<script setup lang="ts">
import { reactive} from 'vue'
import { useVuelidate } from '@vuelidate/core'
import { required, minLength, sameAs, helpers } from '@vuelidate/validators'

interface Emits {
  (e: 'submit', payload: {
    isValid: boolean
    credentials: {
      newPassword: string
      confirmPassword: string
    }
  }): void
}

const emit = defineEmits<Emits>();


const props = defineProps({
  buttonText: {
    type: String,
    default: 'Réinitialiser'
  }
})
// Utiliser des refs au lieu de reactive afin d'avoir une version à jour de newPassword
const newPassword = ref('')
const confirmPassword = ref('')

const state = reactive({
  newPassword,
  confirmPassword
})

// Règles de validation
const validationRules = {
  newPassword: {
    required: helpers.withMessage('Le mot de passe est requis', required),
    minLength: helpers.withMessage('Minimum 6 caractères', minLength(6))
  },
  confirmPassword: {
    required: helpers.withMessage('La confirmation est requise', required),
    sameAs: helpers.withMessage(
      'Les mots de passe ne correspondent pas',
      sameAs(newPassword)
    )
  }
}

const v$ = useVuelidate(validationRules, state)

const handlesubmit = async () => {
  const isValid = await v$.value.$validate()
  if (!isValid) return

  emit('submit', {
    isValid,
    credentials: {
      newPassword: newPassword.value,
      confirmPassword: confirmPassword.value
    }
  });
};

</script>
