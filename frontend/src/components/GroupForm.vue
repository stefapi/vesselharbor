<!-- src/components/GroupForm.vue -->
<template>
  <form @submit.prevent="submit">
    <div>
      <label for="name">Nom du groupe</label>
      <Field id="name" name="name" placeholder="Nom du groupe" />
      <ErrorMessage name="name" class="error" />
    </div>
    <div>
      <label for="description">Description</label>
      <Field id="description" name="description" placeholder="Description du groupe" />
      <ErrorMessage name="description" class="error" />
    </div>
    <button type="submit">{{ isEdit ? 'Mettre à jour' : 'Créer' }}</button>
  </form>
</template>

<script lang="ts">
import { defineComponent, PropType } from 'vue';
import { useForm, Field, ErrorMessage } from 'vee-validate';
import * as yup from 'yup';
import { createGroup, updateGroup } from '@/services/groupService';
import { useNotificationStore } from '@/store/notifications';

export default defineComponent({
  name: 'GroupForm',
  components: { Field, ErrorMessage },
  props: {
    environmentId: {
      type: Number,
      required: true,
    },
    // Pour l'édition, on passe les données initiales du groupe
    initialData: {
      type: Object as PropType<{ id: number; name: string; description: string }>,
      default: null,
    },
  },
  emits: ['success'],
  setup(props, { emit }) {
    const notificationStore = useNotificationStore();
    const isEdit = props.initialData !== null;

    const schema = yup.object({
      name: yup.string().required('Le nom est requis'),
      description: yup.string().required('La description est requise'),
    });

    const { handleSubmit, resetForm, setValues } = useForm({
      validationSchema: schema,
      initialValues: {
        name: props.initialData?.name || '',
        description: props.initialData?.description || '',
      },
    });

    // Si en mode édition, mettre à jour les valeurs du formulaire
    if (isEdit && props.initialData) {
      setValues({
        name: props.initialData.name,
        description: props.initialData.description,
      });
    }

    const submit = handleSubmit(async (values) => {
      try {
        if (isEdit && props.initialData) {
          // Mise à jour du groupe existant
          await updateGroup(props.initialData.id, values);
          notificationStore.addNotification({ type: 'success', message: 'Groupe mis à jour avec succès' });
        } else {
          // Création d'un nouveau groupe
          await createGroup(props.environmentId, values);
          notificationStore.addNotification({ type: 'success', message: 'Groupe créé avec succès' });
        }
        resetForm();
        emit('success');
      } catch (error) {
        notificationStore.addNotification({ type: 'error', message: "Erreur lors de l'opération sur le groupe" });
      }
    });

    return { submit, isEdit };
  },
});
</script>

<style scoped>
.error {
  color: red;
}
</style>

