<!-- src/components/ChangePasswordForm.vue -->
<template>
  <form @submit.prevent="submit">
    <div>
      <label for="old_password">Ancien mot de passe</label>
      <Field id="old_password" name="old_password" type="password" placeholder="Ancien mot de passe" />
      <ErrorMessage name="old_password" class="error" />
    </div>
    <div>
      <label for="new_password">Nouveau mot de passe</label>
      <Field id="new_password" name="new_password" type="password" placeholder="Nouveau mot de passe" />
      <ErrorMessage name="new_password" class="error" />
    </div>
    <button type="submit">Changer le mot de passe</button>
  </form>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { useForm, Field, ErrorMessage } from 'vee-validate';
import * as yup from 'yup';
import { changePassword } from '@/services/userService';
import { useAuthStore } from '@/store/auth';
import { useNotificationStore } from '@/store/notifications';

export default defineComponent({
  components: { Field, ErrorMessage },
  setup() {
    const authStore = useAuthStore();
    const notificationStore = useNotificationStore();
    const schema = yup.object({
      old_password: yup.string().required("Ancien mot de passe requis"),
      new_password: yup.string().min(6, "Minimum 6 caractères").required("Nouveau mot de passe requis"),
    });
    const { handleSubmit, resetForm } = useForm({ validationSchema: schema });
    const submit = handleSubmit(async (values) => {
      try {
        await changePassword(authStore.user!.id, values);
        notificationStore.addNotification({ type: 'success', message: 'Mot de passe mis à jour' });
        resetForm();
      } catch (error) {
        notificationStore.addNotification({ type: 'error', message: 'Erreur lors du changement de mot de passe' });
      }
    });
    return { submit };
  },
});
</script>

<style scoped>
.error {
  color: red;
}
</style>

