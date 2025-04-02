<!-- src/views/Users/AccountView.vue -->
<template>
  <div>
    <h1>Mon Compte</h1>
    <div>
      <p>Email : {{ authStore.user.email }}</p>
      <p>Superadmin : {{ authStore.user.is_superadmin ? 'Oui' : 'Non' }}</p>
    </div>
    <h2>Modifier mes droits</h2>
    <UserForm mode="edit" :initialData="authStore.user" @success="onSuccess" />
    <h2>Changer mon mot de passe</h2>
    <ChangePasswordForm />
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { useAuthStore } from '@/store/auth';
import UserForm from '@/components/UserForm.vue';
import ChangePasswordForm from '@/components/ChangePasswordForm.vue';

export default defineComponent({
  components: { UserForm, ChangePasswordForm },
  setup() {
    const authStore = useAuthStore();
    const onSuccess = () => {
      // Optionnel : rafraîchir les infos utilisateur
    };
    return { authStore, onSuccess };
  },
});
</script>

