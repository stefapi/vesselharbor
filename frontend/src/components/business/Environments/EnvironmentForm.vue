<!-- src/components/EnvironmentForm.vue -->
<template>
  <form @submit.prevent="handleSubmit" class="u-space-y-4">
    <el-form-item label="Nom de l'environnement" :error="NameError">
      <el-input v-model="state.name" placeholder="Entrez le nom de l'environnement" @blur="v$.name.$touch()" />
    </el-form-item>

    <el-button type="primary" native-type="submit" class="u-w-full"> Créer </el-button>
  </form>
</template>

<script setup lang="ts">
import { reactive, computed, unref } from 'vue'
import { useVuelidate } from '@vuelidate/core'
import { required, helpers } from '@vuelidate/validators'
import { createEnvironment } from '@/services/environmentService'
import { useEnvironmentsStore } from '@/store/entities'
import { useNotificationStore } from '@/store/notifications'

const environmentsStore = useEnvironmentsStore()
const notificationStore = useNotificationStore()

const emit = defineEmits<{
  (e: 'success'): void
}>()

const state = reactive({
  name: '',
})

// Règles de validation
const validationRules = {
  name: {
    required: helpers.withMessage("Le nom de l'environnement est requis", required),
  },
}

const v$ = useVuelidate(validationRules, state)

// Computed properties for error handling
const NameError = computed(() => unref((v$.value.name.$error && v$.value.name?.$errors[0]?.$message) || ''))

const handleSubmit = async () => {
  const isValid = await v$.value.$validate()
  if (!isValid) return

  try {
    await createEnvironment(state)
    await environmentsStore.fetchEnvironments()

    // Réinitialisation du formulaire
    state.name = ''
    v$.value.$reset()

    notificationStore.addNotification({
      type: 'success',
      message: 'Environnement créé avec succès',
    })

    emit('success')
  } catch (error) {
    notificationStore.addNotification({
      type: 'error',
      message: "Erreur lors de la création de l'environnement",
    })
  }
}
</script>
