<!-- src/views/Environments/EnvironmentElementsView.vue -->
<template>
  <div class="u-p-6">
    <h1 class="u-text-3xl u-font-bold u-mb-6">
      Environnement : {{ environment.name }}
    </h1>

    <div class="u-mb-6">
      <h2 class="u-text-2xl u-font-semibold u-mb-4">Liste des éléments</h2>

      <div v-if="elements.length === 0" class="u-text-center u-py-8">
        <p class="u-text-gray-500 u-text-lg">
          Aucun élément disponible dans cet environnement.
        </p>
      </div>

      <ul v-else class="u-space-y-3">
        <li
          v-for="element in elements"
          :key="element.id"
          class="u-p-4 u-bg-white u-border u-border-gray-200 u-rounded-lg u-shadow-sm"
        >
          <div class="u-flex u-justify-between u-items-start">
            <div>
              <h3 class="u-font-semibold u-text-lg u-text-gray-900">
                {{ element.name }}
              </h3>
              <p class="u-text-gray-600 u-mt-1">
                {{ element.description }}
              </p>
            </div>
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getEnvironment } from '@/services/environmentService'
import { listElements } from '@/services/elementService'
import { useRoute } from 'vue-router'
import { useNotificationStore } from '@/store/notifications'

interface Environment {
  id: number
  name: string
}

interface Element {
  id: number
  name: string
  description: string
}

const route = useRoute()
const notificationStore = useNotificationStore()
const envId = Number(route.params.envId)
const environment = ref<Environment>({ id: 0, name: '' })
const elements = ref<Element[]>([])

const fetchEnvironment = async () => {
  try {
    const response = await getEnvironment(envId)
    environment.value = response.data.data
  } catch (error) {
    notificationStore.addNotification({
      type: 'error',
      message: "Erreur lors de la récupération de l'environnement"
    })
  }
}

const fetchElements = async () => {
  try {
    const response = await listElements(envId, {})
    elements.value = response.data.data
  } catch (error) {
    notificationStore.addNotification({
      type: 'error',
      message: "Erreur lors de la récupération des éléments"
    })
  }
}

onMounted(() => {
  fetchEnvironment()
  fetchElements()
})
</script>
