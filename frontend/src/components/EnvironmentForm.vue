<!-- src/components/EnvironmentForm.vue -->
<template>
  <form @submit.prevent="submit">
    <div>
      <label for="name">Nom de l'environnement</label>
      <Field id="name" name="name" placeholder="Entrez le nom de l'environnement" />
      <ErrorMessage name="name" class="error" />
    </div>
    <button type="submit">Créer</button>
  </form>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { useForm, Field, ErrorMessage } from 'vee-validate';
import * as yup from 'yup';
import { createEnvironment } from '@/services/environmentService';
import { useEnvironmentsStore } from '@/store/entities';
import { useNotificationStore } from '@/store/notifications';

export default defineComponent({
  components: { Field, ErrorMessage },
  setup() {
    const environmentsStore = useEnvironmentsStore();
    const notificationStore = useNotificationStore();
    const schema = yup.object({
      name: yup.string().required("Le nom de l'environnement est requis"),
    });

    const { handleSubmit, resetForm } = useForm({
      validationSchema: schema,
    });

    const submit = handleSubmit(async (values) => {
      try {
        await createEnvironment(values);
        await environmentsStore.fetchEnvironments();
        resetForm();
        notificationStore.addNotification({ type: 'success', message: "Environnement créé avec succès" });
      } catch (error) {
        console.error("Erreur lors de la création de l'environnement", error);
        notificationStore.addNotification({ type: 'error', message: "Erreur lors de la création de l'environnement" });
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

