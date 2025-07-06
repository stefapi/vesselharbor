<!-- src/components/UserForm.vue -->
<template>
  <div class="u-w-full u-max-w-sm u-p-6 u-rounded-xl u-shadow u-bg-white">
    <form @submit.prevent="handleSubmit" class="u-space-y-4">
      <!-- Mode création -->
      <template v-if="mode === 'create'">
        <el-form-item label="Nom d'utilisateur" :error="UsernameError">
          <el-input v-model="state.username" placeholder="Entrez le nom d'utilisateur" @blur="v$.username?.$touch()" />
        </el-form-item>

        <el-form-item label="Prénom" :error="FirstNameError">
          <el-input v-model="state.first_name" placeholder="Entrez le prénom" @blur="v$.first_name?.$touch()" />
        </el-form-item>

        <el-form-item label="Nom" :error="LastNameError">
          <el-input v-model="state.last_name" placeholder="Entrez le nom" @blur="v$.last_name?.$touch()" />
        </el-form-item>

        <el-form-item label="Email" :error="EmailError">
          <el-input v-model="state.email" type="email" placeholder="Entrez l'email" @blur="v$.email?.$touch()" />
        </el-form-item>

        <el-form-item label="Mot de passe" :error="PasswordError">
          <el-input v-model="state.password" type="password" placeholder="Entrez le mot de passe" show-password @blur="v$.password?.$touch()" />
        </el-form-item>
      </template>

      <!-- Mode édition -->
      <template v-else-if="mode === 'edit' && initialData">
        <el-form-item label="Email">
          <el-input :model-value="initialData.email" disabled />
        </el-form-item>

        <el-form-item>
          <el-checkbox v-model="state.is_superadmin"> Superadmin </el-checkbox>
        </el-form-item>
      </template>

      <!-- Bouton -->
      <el-button type="primary" native-type="submit" class="u-w-full">
        {{ mode === 'create' ? 'Créer' : 'Mettre à jour' }}
      </el-button>
    </form>
  </div>
</template>

<script setup lang="ts">
import { reactive, watch, computed, unref, type PropType } from 'vue'
import { useVuelidate } from '@vuelidate/core'
import { required, email, minLength, helpers } from '@vuelidate/validators'
import { useNotificationStore } from '@/store/notifications'
import { createauserinfreemode, modifysuperadminstatus } from '@/api'

const props = defineProps({
  mode: {
    type: String as PropType<'create' | 'edit'>,
    default: 'create',
  },
  initialData: {
    type: Object as PropType<{ id: number; email: string; is_superadmin: boolean }>,
    default: null,
  },
})

const emit = defineEmits(['success'])
const notificationStore = useNotificationStore()

const state = reactive({
  username: '',
  first_name: '',
  last_name: '',
  email: '',
  password: '',
  is_superadmin: props.mode === 'edit' ? props.initialData?.is_superadmin || false : false,
})

// Règles de validation conditionnelles
const validationRules = computed(() => {
  if (props.mode === 'create') {
    return {
      username: {
        required: helpers.withMessage("Le nom d'utilisateur est requis", required),
      },
      first_name: {
        required: helpers.withMessage('Le prénom est requis', required),
      },
      last_name: {
        required: helpers.withMessage('Le nom est requis', required),
      },
      email: {
        required: helpers.withMessage("L'email est requis", required),
        email: helpers.withMessage('Email invalide', email),
      },
      password: {
        required: helpers.withMessage('Le mot de passe est requis', required),
        minLength: helpers.withMessage('Minimum 6 caractères', minLength(6)),
      },
    }
  }
  return {
    is_superadmin: {
      required: helpers.withMessage('Le statut est requis', required),
    },
  }
})

const v$ = useVuelidate(validationRules, state)

// Computed properties for error handling
const UsernameError = computed(() => unref((v$.value.username?.$error && v$.value.username?.$errors[0]?.$message) || ''))
const FirstNameError = computed(() => unref((v$.value.first_name?.$error && v$.value.first_name?.$errors[0]?.$message) || ''))
const LastNameError = computed(() => unref((v$.value.last_name?.$error && v$.value.last_name?.$errors[0]?.$message) || ''))
const EmailError = computed(() => unref((v$.value.email?.$error && v$.value.email?.$errors[0]?.$message) || ''))
const PasswordError = computed(() => unref((v$.value.password?.$error && v$.value.password?.$errors[0]?.$message) || ''))

// Synchronisation des données initiales
watch(
  () => props.initialData,
  (newVal) => {
    if (props.mode === 'edit' && newVal) {
      state.is_superadmin = newVal.is_superadmin
    }
  },
  { immediate: true }
)

const handleSubmit = async () => {
  const isValid = await v$.value.$validate()
  if (!isValid) return

  try {
    if (props.mode === 'create') {
      await createauserinfreemode(state)
      notificationStore.addNotification({
        type: 'success',
        message: 'Utilisateur créé avec succès',
      })
      state.username = ''
      state.first_name = ''
      state.last_name = ''
      state.email = ''
      state.password = ''
    } else if (props.mode === 'edit' && props.initialData) {
      await modifysuperadminstatus(props.initialData.id, { is_superadmin: state.is_superadmin })
      notificationStore.addNotification({
        type: 'success',
        message: 'Statut superadmin mis à jour',
      })
    }

    v$.value.$reset()
    emit('success')
  } catch (error) {
    notificationStore.addNotification({
      type: 'error',
      message: "Erreur lors de l'opération sur l'utilisateur",
    })
  }
}
</script>
