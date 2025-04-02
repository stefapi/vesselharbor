<!-- src/components/GroupFunctionsManager.vue -->
<template>
  <div class="group-functions-manager">
    <h3>Fonctions du groupe</h3>
    <ul>
      <li v-for="func in groupFunctions" :key="func.id">
        {{ func.name }}
        <button @click="removeFunction(func.id)">Retirer</button>
      </li>
    </ul>
    <h4>Ajouter une fonction</h4>
    <select v-model="selectedFunctionId">
      <option value="" disabled>Sélectionnez une fonction</option>
      <option v-for="func in availableFunctions" :key="func.id" :value="func.id">
        {{ func.name }}
      </option>
    </select>
    <button @click="addFunction" :disabled="!selectedFunctionId">Ajouter</button>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue';
import { getGroupFunctions, addFunctionToGroup, removeFunctionFromGroup, getAvailableFunctions } from '@/services/groupService';
import { useNotificationStore } from '@/store/notifications';

export default defineComponent({
  name: 'GroupFunctionsManager',
  props: {
    groupId: {
      type: Number,
      required: true,
    },
  },
  setup(props) {
    const groupFunctions = ref([] as any[]);
    const availableFunctions = ref([] as any[]);
    const selectedFunctionId = ref<number | ''>('');
    const notificationStore = useNotificationStore();

    const fetchGroupFunctions = async () => {
      try {
        const response = await getGroupFunctions(props.groupId);
        groupFunctions.value = response.data.data;
      } catch (error) {
        notificationStore.addNotification({ type: 'error', message: "Erreur lors du chargement des fonctions du groupe" });
      }
    };

    const fetchAvailableFunctions = async () => {
      try {
        const response = await getAvailableFunctions();
        availableFunctions.value = response.data.data;
      } catch (error) {
        notificationStore.addNotification({ type: 'error', message: "Erreur lors du chargement des fonctions disponibles" });
      }
    };

    const addFunction = async () => {
      if (!selectedFunctionId.value) return;
      try {
        // On récupère la fonction sélectionnée depuis availableFunctions
        const func = availableFunctions.value.find((f: any) => f.id === selectedFunctionId.value);
        await addFunctionToGroup(props.groupId, { name: func.name, description: func.description });
        notificationStore.addNotification({ type: 'success', message: "Fonction ajoutée avec succès" });
        await fetchGroupFunctions();
      } catch (error) {
        notificationStore.addNotification({ type: 'error', message: "Erreur lors de l'ajout de la fonction" });
      }
    };

    const removeFunction = async (functionId: number) => {
      try {
        await removeFunctionFromGroup(props.groupId, functionId);
        notificationStore.addNotification({ type: 'success', message: "Fonction retirée avec succès" });
        await fetchGroupFunctions();
      } catch (error) {
        notificationStore.addNotification({ type: 'error', message: "Erreur lors du retrait de la fonction" });
      }
    };

    onMounted(() => {
      fetchGroupFunctions();
      fetchAvailableFunctions();
    });

    return {
      groupFunctions,
      availableFunctions,
      selectedFunctionId,
      addFunction,
      removeFunction,
    };
  },
});
</script>

<style scoped>
.group-functions-manager {
  border: 1px solid #ccc;
  padding: 1rem;
  margin-top: 1rem;
}
.group-functions-manager ul {
  list-style: none;
  padding: 0;
}
.group-functions-manager li {
  margin-bottom: 0.5rem;
}
</style>

