<!-- src/components/GroupForm.vue -->
<template>
  <form @submit.prevent="handleSubmit" class="u-space-y-4">
    <el-form-item
      label="Nom du groupe"
      :error="NameError"
    >
      <el-input
        v-model="state.name"
        placeholder="Nom du groupe"
        @blur="v$.name.$touch()"
      />
    </el-form-item>

    <el-form-item
      label="Description"
      :error="DescriptionError"
    >
      <el-input
        v-model="state.description"
        type="textarea"
        placeholder="Description du groupe"
        @blur="v$.description.$touch()"
      />
    </el-form-item>

    <el-button
      type="primary"
      native-type="submit"
      class="u-w-full"
    >
      {{ isEdit ? 'Mettre à jour' : 'Créer' }}
    </el-button>
  </form>
</template>

<script setup lang="ts">
import { reactive, computed, watch } from 'vue'
import { useVuelidate } from '@vuelidate/core'
import { required, helpers } from '@vuelidate/validators'
import { createGroup, updateGroup } from '@/services/groupService'
import { useNotificationStore } from '@/store/notifications'

interface Props {
  environmentId: number
  initialData?: { id: number; name: string; description: string } | null
}

const props = withDefaults(defineProps<Props>(), {
  initialData: null
})

const emit = defineEmits<{
  (e: 'success'): void
}>()

const notificationStore = useNotificationStore()
const isEdit = computed(() => props.initialData !== null)

const state = reactive({
  name: props.initialData?.name || '',
  description: props.initialData?.description || '',
})

// Règles de validation
const validationRules = {
  name: {
    required: helpers.withMessage('Le nom est requis', required),
  },
  description: {
    required: helpers.withMessage('La description est requise', required),
  },
}

const v$ = useVuelidate(validationRules, state)

// Computed properties for error handling
const NameError = computed(() => (v$.value.name.$error && v$.value.name?.$errors[0]?.$message) || '')
const DescriptionError = computed(() => (v$.value.description.$error && v$.value.description?.$errors[0]?.$message) || '')

// Synchronisation des données initiales
watch(
  () => props.initialData,
  (newVal) => {
    if (newVal) {
      state.name = newVal.name
      state.description = newVal.description
    }
  },
  { immediate: true }
)

const handleSubmit = async () => {
  const isValid = await v$.value.$validate()
  if (!isValid) return

  try {
    if (isEdit.value && props.initialData) {
      // Mise à jour du groupe existant
      await updateGroup(props.initialData.id, state)
      notificationStore.addNotification({
        type: 'success',
        message: 'Groupe mis à jour avec succès'
      })
    } else {
      // Création d'un nouveau groupe
      await createGroup(props.environmentId, state)
      notificationStore.addNotification({
        type: 'success',
        message: 'Groupe créé avec succès'
      })
    }

    // Réinitialisation du formulaire
    state.name = ''
    state.description = ''
    v$.value.$reset()
    emit('success')
  } catch (error) {
    notificationStore.addNotification({
      type: 'error',
      message: "Erreur lors de l'opération sur le groupe"
    })
  }
}
</script>
