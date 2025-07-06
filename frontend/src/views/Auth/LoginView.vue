<!-- src/views/Auth/LoginView.vue -->
<template>
  <div class="u-min-h-[calc(100vh-1rem)] u-w-full u-flex u-items-center u-justify-center u-bg-gray-100">
    <el-card class="u-w-full u-max-w-md">
      <div class="u-text-2xl u-font-bold u-text-center">Connexion</div>
      <LoginForm @submit="handleFormSubmit" />
      <router-link to="/forgot-password" class="u-block u-text-center u-text-primary u-mt-4"> Mot de passe oublié ? </router-link>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import LoginForm from '@/components/business/Auth/LoginForm.vue'

interface LoginSubmitEvent {
  isValid: boolean
  credentials: {
    email: string
    password: string
  }
}

// Use the authStore for consistent authentication state
const authStore = useAuthStore()
const notificationStore = useNotificationStore()
const router = useRouter()

const handleFormSubmit = async (event: LoginSubmitEvent) => {
  if (!event.isValid) {
    notificationStore.addNotification({
      type: 'error',
      message: 'Veuillez corriger les erreurs dans le formulaire',
    })
    return
  }

  try {
    // Use the authStore's login method for consistent authentication state
    await authStore.login({
      username: event.credentials.email,
      password: event.credentials.password
    })

    notificationStore.addNotification({
      type: 'success',
      message: 'Connexion réussie ! Redirection en cours...',
    })

    // Redirection après un léger délai pour laisser le store se mettre à jour
    setTimeout(() => {
      router.push({ name: 'Dashboard' })
    }, 150)
  } catch (loginError: unknown) {
    handleLoginError(loginError)
  }
}

const handleLoginError = (loginError: unknown) => {
  let errorMessage = 'Une erreur est survenue lors de la connexion'

  if (isAxiosError(loginError)) {
    errorMessage = (loginError.response?.data as any)?.message || errorMessage
    if (loginError.response?.status === 401) {
      errorMessage = 'Identifiants incorrects'
    }
  }

  notificationStore.addNotification({
    type: 'error',
    message: errorMessage,
  })
}
</script>
