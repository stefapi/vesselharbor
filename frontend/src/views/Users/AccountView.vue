<template>
  <div>
    <h1>Mon Compte</h1>
    <div>
      <p>Email : {{ authStore.user?.email }}</p>
      <p>Superadmin : {{ authStore.user?.is_superadmin ? 'Oui' : 'Non' }}</p>
    </div>
    <h2>Modifier mes droits</h2>
    <UserForm mode="edit" :initial-data="authStore.user || undefined" @success="onSuccess" />
    <h2>Changer mon mot de passe</h2>
    <ChangePasswordForm />
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '@/store/auth'
import UserForm from '@/components/UserForm.vue'
import ChangePasswordForm from '@/components/Auth/ChangePasswordForm.vue'

const authStore = useAuthStore()

const onSuccess = () => {
  // Optionnel : rafraîchir les infos utilisateur
  // Exemple possible : authStore.fetchUser();
}
</script>
