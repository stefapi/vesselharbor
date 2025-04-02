<!-- src/components/UserForm.vue -->
<template>
  <form @submit.prevent="submit">
    <!-- En mode création, on saisit email et mot de passe -->
    <div v-if="mode === 'create'">
      <label for="email">Email</label>
      <Field id="email" name="email" type="email" placeholder="Entrez l'email" />
      <ErrorMessage name="email" class="error" />
    </div>
    <div v-if="mode === 'create'">
      <label for="password">Mot de passe</label>
      <Field id="password" name="password" type="password" placeholder="Entrez le mot de passe" />
      <ErrorMessage name="password" class="error" />
    </div>
    <!-- En mode édition, on affiche l'email en lecture seule et on permet de modifier le statut superadmin -->
    <div v-if="mode === 'edit' && initialData">
      <label>Email</label>
      <input type="text" :value="initialData.email" disabled />
      <label>
        <input type="checkbox" v-model="values.is_superadmin" />
        Superadmin
      </label>
    </div>
    <button type="submit">{{ mode === 'create' ? 'Créer' : 'Mettre à jour' }}</button>
  </form>
</template>

<script lang="ts">
import { useForm, Field, ErrorMessage } from 'vee-validate';
import * as yup from 'yup';
import { createUser, updateSuperadmin } from '@/services/userService';
import { useNotificationStore } from '@/store/notifications';

export default defineComponent({
  name: 'UserForm',
  components: { Field, ErrorMessage },
  props: {
    mode: {
      type: String as PropType<'create' | 'edit'>,
      default: 'create',
    },
    // Pour l'édition, on passe les données initiales de l'utilisateur
    initialData: {
      type: Object as PropType<{ id: number; email: string; is_superadmin: boolean }>,
      default: null,
    },
  },
  emits: ['success'],
  setup(props, { emit }) {
    const notificationStore = useNotificationStore();
    const schemaCreate = yup.object({
      email: yup.string().email('Email invalide').required("L'email est requis"),
      password: yup.string().min(6, 'Minimum 6 caractères').required('Le mot de passe est requis'),
    });
    const schemaEdit = yup.object({
      is_superadmin: yup.boolean().required(),
    });
    const { handleSubmit, resetForm, setValues, values } = useForm({
      validationSchema: props.mode === 'create' ? schemaCreate : schemaEdit,
      initialValues: props.mode === 'edit' && props.initialData
        ? { is_superadmin: props.initialData.is_superadmin }
        : {},
    });
    if (props.mode === 'edit' && props.initialData) {
      setValues({ is_superadmin: props.initialData.is_superadmin });
    }
    const submit = handleSubmit(async (formValues) => {
      try {
        if (props.mode === 'create') {
          await createUser(formValues);
          notificationStore.addNotification({ type: 'success', message: "Utilisateur créé avec succès" });
        } else if (props.mode === 'edit' && props.initialData) {
          await updateSuperadmin(props.initialData.id, formValues.is_superadmin);
          notificationStore.addNotification({ type: 'success', message: "Statut superadmin mis à jour" });
        }
        resetForm();
        emit('success');
      } catch (error) {
        notificationStore.addNotification({ type: 'error', message: "Erreur lors de l'opération sur l'utilisateur" });
      }
    });
    return { submit, values };
  },
});
</script>

<style scoped>
.error {
  color: red;
}
</style>

