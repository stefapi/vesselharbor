<!-- src/components/UserForm.vue -->
<template>
  <div class="w-full max-w-sm p-6 rounded-xl shadow bg-white">
    <form @submit.prevent="handleSubmit" class="space-y-4">
      <!-- Mode création -->
      <template v-if="mode === 'create'">
        <VaInput
          v-model="state.email"
          type="email"
          placeholder="Entrez l'email"
          label="Email"
          :error="v$.email.$error && v$.email.$errors[0]?.$message"
          @blur="v$.email.$touch()"
          class="w-full"
        />
        <VaInput
          v-model="state.password"
          type="password"
          placeholder="Entrez le mot de passe"
          label="Mot de passe"
          :error="v$.password.$error && v$.password.$errors[0]?.$message"
          @blur="v$.password.$touch()"
          class="w-full"
        />
      </template>

      <!-- Mode édition -->
      <template v-else-if="mode === 'edit' && initialData">
        <VaInput
          :model-value="initialData.email"
          label="Email"
          disabled
          class="w-full"
        />
        <VaCheckbox
          v-model="state.is_superadmin"
          label="Superadmin"
          class="mt-2"
        />
      </template>

      <VaButton type="submit" color="primary" class="w-full">
        {{ mode === 'create' ? 'Créer' : 'Mettre à jour' }}
      </VaButton>
    </form>
  </div>
</template>

<script setup lang="ts">
import { reactive, watch, computed } from 'vue';
import { useVuelidate } from '@vuelidate/core';
import { required, email, minLength, helpers } from '@vuelidate/validators';
import { useNotificationStore } from '@/store/notifications';
import { createUser, updateSuperadmin } from '@/services/userService';

const props = defineProps({
  mode: {
    type: String as PropType<'create' | 'edit'>,
    default: 'create',
  },
  initialData: {
    type: Object as PropType<{ id: number; email: string; is_superadmin: boolean }>,
    default: null,
  },
});

const emit = defineEmits(['success']);
const notificationStore = useNotificationStore();

const state = reactive({
  email: '',
  password: '',
  is_superadmin: props.mode === 'edit' ? props.initialData?.is_superadmin || false : false,
});

// Règles de validation conditionnelles
const validationRules = computed(() => {
  if (props.mode === 'create') {
    return {
      email: {
        required: helpers.withMessage("L'email est requis", required),
        email: helpers.withMessage('Email invalide', email),
      },
      password: {
        required: helpers.withMessage('Le mot de passe est requis', required),
        minLength: helpers.withMessage('Minimum 6 caractères', minLength(6)),
      },
    };
  }
  return {
    is_superadmin: {
      required: helpers.withMessage('Le statut est requis', required),
    },
  };
});

const v$ = useVuelidate(validationRules, state);

// Synchronisation des données initiales
watch(
  () => props.initialData,
  (newVal) => {
    if (props.mode === 'edit' && newVal) {
      state.is_superadmin = newVal.is_superadmin;
    }
  },
  { immediate: true }
);

const handleSubmit = async () => {
  const isValid = await v$.value.$validate();
  if (!isValid) return;

  try {
    if (props.mode === 'create') {
      await createUser(state);
      notificationStore.addNotification({
        type: 'success',
        message: 'Utilisateur créé avec succès',
      });
      state.email = '';
      state.password = '';
    } else if (props.mode === 'edit' && props.initialData) {
      await updateSuperadmin(props.initialData.id, state.is_superadmin);
      notificationStore.addNotification({
        type: 'success',
        message: 'Statut superadmin mis à jour',
      });
    }

    v$.value.$reset();
    emit('success');
  } catch (error) {
    notificationStore.addNotification({
      type: 'error',
      message: "Erreur lors de l'opération sur l'utilisateur",
    });
  }
};
</script>
