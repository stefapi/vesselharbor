<template>
  <VaForm
    ref="formRef"
    @submit.prevent="submitForm"
    class="max-w-md mx-auto space-y-4"
  >
    <!-- Ancien mot de passe -->
    <VaInput
      v-model="state.oldPassword"
      label="Ancien mot de passe"
      type="password"
      :error="v$.oldPassword.$error"
      :error-messages="v$.oldPassword.$errors.map(e => e.$message)"
      @blur="v$.oldPassword.$touch()"
      class="mb-4"
    />

    <!-- Nouveau mot de passe -->
    <VaInput
      v-model="state.newPassword"
      label="Nouveau mot de passe"
      type="password"
      :error="v$.newPassword.$error"
      :error-messages="v$.newPassword.$errors.map(e => e.$message)"
      @blur="v$.newPassword.$touch()"
      class="mb-4"
    />

    <!-- Confirmation nouveau mot de passe -->
    <VaInput
      v-model="state.confirmPassword"
      label="Confirmer le nouveau mot de passe"
      type="password"
      :error="v$.confirmPassword.$error"
      :error-messages="v$.confirmPassword.$errors.map(e => e.$message)"
      @blur="v$.confirmPassword.$touch()"
      class="mb-4"
    />

    <VaButton
      type="submit"
      :disabled="v$.$invalid"
      class="w-full"
    >
      Valider
    </VaButton>
  </VaForm>
</template>

<script setup>
import { reactive, computed } from 'vue'
import { useVuelidate } from '@vuelidate/core'
import { required, minLength, sameAs } from '@vuelidate/validators'
import { VaForm, VaInput, VaButton } from 'vuestic-ui'

const emit = defineEmits(['submit'])

// State management
const state = reactive({
  oldPassword: '',
  newPassword: '',
  confirmPassword: ''
})

// Validation rules
const rules = computed(() => ({
  oldPassword: {
    required,
    minLength: minLength(8)
  },
  newPassword: {
    required,
    minLength: minLength(8)
  },
  confirmPassword: {
    required,
    sameAs: sameAs(state.newPassword)
  }
}))

const v$ = useVuelidate(rules, state)

// Form submission
const submitForm = async () => {
  const isValid = await v$.value.$validate()

  if (!isValid) return

  emit('submit', {
    oldPassword: state.oldPassword,
    newPassword: state.newPassword
  })

  // Reset form
  Object.assign(state, {
    oldPassword: '',
    newPassword: '',
    confirmPassword: ''
  })
  v$.value.$reset()
}
// Exposition des états pour les stories
defineExpose({
  state,
  v$
})
</script>
