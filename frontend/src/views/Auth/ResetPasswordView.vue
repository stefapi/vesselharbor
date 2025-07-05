<!-- src/views/Auth/ResetPasswordView.vue -->
<template>
  <div class="u-min-h-screen u-flex u-items-center u-justify-center u-bg-gray-100">
    <div class="u-w-full u-max-w-md">
      <el-card class="u-p-6 u-rounded u-shadow">
        <h1 class="u-text-xl u-font-bold u-mb-4 u-text-center">Réinitialisation du mot de passe</h1>

        <PasswordResetForm button-text="Réinitialiser" @submit="handlePasswordReset" />

        <router-link to="/login" class="u-block u-text-center u-text-primary hover:u-text-primary-dark u-transition-colors u-mt-4 u-flex u-items-center u-justify-center">
          <Icon icon="material-symbols:arrow-back" class="u-mr-1 u-text-lg" />
          Retour à la connexion
        </router-link>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useNotificationStore } from '@/store/notifications'
import { useRouter, useRoute } from 'vue-router'
import { isAxiosError } from '@/services/api'
import PasswordResetForm from '@/components/Auth/PasswordResetForm.vue'
import { reset_password } from '@/services/authService.js'

interface ResetPasswordSubmitEvent {
  isValid: boolean
  credentials: {
    newPassword: string
    confirmPassword: string
  }
}

const notificationStore = useNotificationStore()
const router = useRouter()
const route = useRoute()

const getResetToken = () => {
  // Récupération du token depuis l'URL
  const token = route.query.token as string
  if (!token) {
    notificationStore.addNotification({
      type: 'error',
      message: 'Lien de réinitialisation invalide',
    })
    router.push({ name: 'Login' })
  }
  return token
}

const handlePasswordReset = async (event: ResetPasswordSubmitEvent) => {
  const token = getResetToken()
  if (!token) return
  if (!event.isValid) {
    notificationStore.addNotification({
      type: 'error',
      message: 'Veuillez corriger les erreurs dans le formulaire',
    })
    return
  }

  try {
    await reset_password(token, event.credentials.newPassword)

    notificationStore.addNotification({
      type: 'success',
      message: 'Mot de passe réinitialisé avec succès',
    })

    setTimeout(() => {
      router.push({
        name: 'Login',
        query: { password_reset: 'success' },
      })
    }, 300)
  } catch (error: unknown) {
    handleResetError(error)
  }
}

const handleResetError = (error: unknown) => {
  let errorMessage = 'Erreur lors de la réinitialisation du mot de passe'

  if (isAxiosError(error)) {
    errorMessage = (error.response?.data as any)?.message || errorMessage
    if (error.response?.status === 401) {
      errorMessage = 'Lien de réinitialisation invalide ou expiré'
    }
  }

  notificationStore.addNotification({
    type: 'error',
    message: errorMessage,
  })
}
</script>
