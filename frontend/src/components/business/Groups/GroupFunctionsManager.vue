<!-- src/components/GroupFunctionsManager.vue -->
<template>
  <div class="u-border u-border-gray-300 u-p-4 u-mt-4 u-rounded">
    <h3 class="u-text-lg u-font-semibold u-mb-4">Fonctions du groupe</h3>

    <ul class="u-space-y-2 u-mb-6">
      <li v-for="func in groupFunctions" :key="func.id" class="u-flex u-justify-between u-items-center u-p-2 u-bg-gray-50 u-rounded">
        <span class="u-font-medium">{{ func.name }}</span>
        <button @click="removeFunction(func.id)" class="u-px-3 u-py-1 u-bg-red-500 u-text-white u-rounded u-text-sm u-hover:bg-red-600">Retirer</button>
      </li>
      <li v-if="groupFunctions.length === 0" class="u-text-gray-500 u-italic">Aucune fonction assignée</li>
    </ul>

    <div class="u-space-y-3">
      <h4 class="u-text-md u-font-medium">Ajouter une fonction</h4>
      <div class="u-flex u-gap-2">
        <select v-model="selectedFunctionId" class="u-flex-1 u-px-3 u-py-2 u-border u-border-gray-300 u-rounded u-focus:outline-none u-focus:ring-2 u-focus:ring-blue-500">
          <option value="" disabled>Sélectionnez une fonction</option>
          <option v-for="func in availableFunctions" :key="func.id" :value="func.id">
            {{ func.name }}
          </option>
        </select>
        <button @click="addFunction" :disabled="!selectedFunctionId" class="u-px-4 u-py-2 u-bg-blue-500 u-text-white u-rounded u-hover:bg-blue-600 u-disabled:opacity-50 u-disabled:cursor-not-allowed">Ajouter</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getGroupFunctions, addFunctionToGroup, removeFunctionFromGroup, getAvailableFunctions } from '@/services/groupService'
import { useNotificationStore } from '@/store/notifications'

interface GroupFunction {
  id: number
  name: string
  description: string
}

interface Props {
  groupId: number
}

const props = defineProps<Props>()

const groupFunctions = ref<GroupFunction[]>([])
const availableFunctions = ref<GroupFunction[]>([])
const selectedFunctionId = ref<number | ''>('')
const notificationStore = useNotificationStore()

const fetchGroupFunctions = async () => {
  try {
    const response = await getGroupFunctions(props.groupId)
    groupFunctions.value = response.data.data
  } catch (error) {
    notificationStore.addNotification({
      type: 'error',
      message: 'Erreur lors du chargement des fonctions du groupe',
    })
  }
}

const fetchAvailableFunctions = async () => {
  try {
    const response = await getAvailableFunctions()
    availableFunctions.value = response.data.data
  } catch (error) {
    notificationStore.addNotification({
      type: 'error',
      message: 'Erreur lors du chargement des fonctions disponibles',
    })
  }
}

const addFunction = async () => {
  if (!selectedFunctionId.value) return
  try {
    // On récupère la fonction sélectionnée depuis availableFunctions
    const func = availableFunctions.value.find((f) => f.id === selectedFunctionId.value)
    if (!func) return

    await addFunctionToGroup(props.groupId, {
      name: func.name,
      description: func.description,
    })
    notificationStore.addNotification({
      type: 'success',
      message: 'Fonction ajoutée avec succès',
    })
    selectedFunctionId.value = ''
    await fetchGroupFunctions()
  } catch (error) {
    notificationStore.addNotification({
      type: 'error',
      message: "Erreur lors de l'ajout de la fonction",
    })
  }
}

const removeFunction = async (functionId: number) => {
  try {
    await removeFunctionFromGroup(props.groupId, functionId)
    notificationStore.addNotification({
      type: 'success',
      message: 'Fonction retirée avec succès',
    })
    await fetchGroupFunctions()
  } catch (error) {
    notificationStore.addNotification({
      type: 'error',
      message: 'Erreur lors du retrait de la fonction',
    })
  }
}

onMounted(() => {
  fetchGroupFunctions()
  fetchAvailableFunctions()
})
</script>
