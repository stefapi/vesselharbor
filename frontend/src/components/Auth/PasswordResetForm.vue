<template>
  <div class="u-w-full u-max-w-sm u-p-6 u-rounded-xl u-shadow u-bg-white">
    <form @submit.prevent="handlesubmit" class="u-space-y-4">
      <!-- Nouveau mot de passe -->
      <el-form-item
        label="Nouveau mot de passe"
        :error="NewPasswordError"
      >
        <el-input
          v-model="newPassword"
          type="password"
          placeholder="••••••"
          @blur="v$.newPassword.$touch()"
          show-password
        />
      </el-form-item>

      <!-- Confirmation -->
      <el-form-item
        label="Confirmer le mot de passe"
        :error="ConfirmPasswordError"
      >
        <el-input
          v-model="confirmPassword"
          type="password"
          placeholder="••••••"
          @blur="v$.confirmPassword.$touch()"
          show-password
        />
      </el-form-item>

      <el-button
        type="primary"
        native-type="submit"
        class="u-w-full"
      >
        {{ buttonText }}
      </el-button>
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
