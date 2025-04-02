<template>
  <div class="w-full max-w-sm p-6 rounded-xl shadow bg-white">
    <!-- Message d'erreur API -->
    <div v-if="apiError" class="mb-4 p-3 text-sm text-red-600 bg-red-50 rounded">
      {{ apiError }}
    </div>

    <form @submit.prevent="submit" class="space-y-4">
      <VaInput
        v-model="state.newPassword"
        type="password"
        label="Nouveau mot de passe"
        placeholder="••••••"
        :error="v$.newPassword.$error && v$.newPassword.$errors[0]?.$message"
        @blur="v$.newPassword.$touch()"
        class="w-full"
      />

      <VaInput
        v-model="state.confirmPassword"
        type="password"
        label="Confirmer le mot de passe"
        placeholder="••••••"
        :error="v$.confirmPassword.$error && v$.confirmPassword.$errors[0]?.$message"
        @blur="v$.confirmPassword.$touch()"
        class="w-full"
      />

      <VaButton
        type="submit"
        color="primary"
        class="w-full"
        :loading="isSubmitting"
      >
        {{ buttonText }}
      </VaButton>
    </form>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useVuelidate } from '@vuelidate/core'
import { required, minLength, sameAs } from '@vuelidate/validators'

const props = defineProps({
  buttonText: {
    type: String,
    default: 'Réinitialiser'
  },
  onSubmit: {
    type: Function,
    required: true
  }
})

const state = reactive({
  newPassword: '',
  confirmPassword: ''
})

const apiError = ref(null)
const isSubmitting = ref(false)

const rules = {
  newPassword: {
    required,
    minLength: minLength(6)
  },
  confirmPassword: {
    required,
    sameAs: sameAs(() => state.newPassword)
  }
}

const v$ = useVuelidate(rules, state)

const submit = async () => {
  apiError.value = null
  const isValid = await v$.value.$validate()
  if (!isValid) return

  isSubmitting.value = true
  try {
    await props.onSubmit(state.newPassword)
  } catch (error) {
    handleApiError(error)
  } finally {
    isSubmitting.value = false
  }
}

const handleApiError = (error) => {
  if (error.response?.data?.message) {
    apiError.value = error.response.data.message
  } else {
    apiError.value = "Une erreur est survenue, veuillez réessayer"
    console.error("Erreur lors de la réinitialisation", error)
  }
}
</script>
