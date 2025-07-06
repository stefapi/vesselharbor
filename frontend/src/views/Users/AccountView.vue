<template>
  <div>
    <h1>Mon Compte</h1>
    <div>
      <p>Email : {{ userEmail }}</p>
      <p>Superadmin : {{ isSuperAdmin ? 'Oui' : 'Non' }}</p>
    </div>
    <h2>Modifier mes droits</h2>
    <UserForm mode="edit" :initial-data="user || undefined" @success="onSuccess" />
    <h2>Changer mon mot de passe</h2>
    <ChangePasswordForm />
  </div>
</template>

<script setup lang="ts">
import { useAuth } from '@/composables/api/useAuth'
import UserForm from '@/components/business/Users/UserForm.vue'
import ChangePasswordForm from '@/components/business/Auth/ChangePasswordForm.vue'

const { user, userEmail, isSuperAdmin } = useAuth()

const onSuccess = () => {
  // Optionnel : rafraîchir les infos utilisateur
  // TODO: Implémenter la méthode de rafraîchissement du profil utilisateur dans useAuth
}
</script>
