<!--
  - Copyright (c) 2025.  VesselHarbor
  -
  - ____   ____                          .__    ___ ___             ___.
  - \   \ /   /____   ______ ______ ____ |  |  /   |   \_____ ______\_ |__   ___________
  -  \   Y   // __ \ /  ___//  ___// __ \|  | /    ~    \__  \\_  __ \ __ \ /  _ \_  __ \
  -   \     /\  ___/ \___ \ \___ \\  ___/|  |_\    Y    // __ \|  | \/ \_\ (  <_> )  | \/
  -    \___/  \___  >____  >____  >\___  >____/\___|_  /(____  /__|  |___  /\____/|__|
  -               \/     \/     \/     \/            \/      \/          \/
  -
  -
  - MIT License
  -
  - Permission is hereby granted, free of charge, to any person obtaining a copy
  - of this software and associated documentation files (the "Software"), to deal
  - in the Software without restriction, including without limitation the rights
  - to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
  - copies of the Software, and to permit persons to whom the Software is
  - furnished to do so, subject to the following conditions:
  -
  - The above copyright notice and this permission notice shall be included in all
  - copies or substantial portions of the Software.
  -
  - THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
  - IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
  - FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
  - AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
  - LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
  - OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
  - SOFTWARE.
  -
  -->

<!-- src/components/business/Organizations/OrganizationForm.vue -->
<template>
  <form @submit.prevent="handleSubmit" class="u-space-y-4">
    <el-form-item label="Nom de l'organisation" :error="NameError">
      <el-input v-model="state.name" placeholder="Nom de l'organisation" @blur="v$.name.$touch()" />
    </el-form-item>

    <el-form-item label="Description" :error="DescriptionError">
      <el-input v-model="state.description" type="textarea" placeholder="Description de l'organisation" @blur="v$.description.$touch()" />
    </el-form-item>

    <el-button type="primary" native-type="submit" class="u-w-full">
      {{ isEdit ? 'Mettre à jour' : 'Créer' }}
    </el-button>
  </form>
</template>

<script setup lang="ts">
import { reactive, computed, watch, unref } from 'vue'
import { useVuelidate } from '@vuelidate/core'
import { required, helpers } from '@vuelidate/validators'
import { createorganization, updateorganization } from '@/api/organizations'
import type { OrganizationOut } from '@/api/types'
import { useNotificationStore } from '@/store/notifications'

interface Props {
  initialData?: OrganizationOut | null
}

const props = withDefaults(defineProps<Props>(), {
  initialData: null,
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
    // Description is optional for organizations
  },
}

const v$ = useVuelidate(validationRules, state)

// Computed properties for error handling
const NameError = computed(() => unref((v$.value.name.$error && v$.value.name?.$errors[0]?.$message) || ''))
const DescriptionError = computed(() => unref((v$.value.description.$error && v$.value.description?.$errors[0]?.$message) || ''))

// Synchronisation des données initiales
watch(
  () => props.initialData,
  (newVal) => {
    if (newVal) {
      state.name = newVal.name
      state.description = newVal.description || ''
    }
  },
  { immediate: true }
)

const handleSubmit = async () => {
  const isValid = await v$.value.$validate()
  if (!isValid) return

  try {
    if (isEdit.value && props.initialData) {
      // Mise à jour de l'organisation existante
      await updateorganization(props.initialData.id, state)
      notificationStore.addNotification({
        type: 'success',
        message: 'Organisation mise à jour avec succès',
      })
    } else {
      // Création d'une nouvelle organisation
      await createorganization(state)
      notificationStore.addNotification({
        type: 'success',
        message: 'Organisation créée avec succès',
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
      message: "Erreur lors de l'opération sur l'organisation",
    })
  }
}
</script>
