<!-- src/views/Environments/EnvironmentsView.vue -->
<template>
  <div class="u-p-6">
    <h1 class="u-text-3xl u-font-bold u-mb-6">
      Environnement : {{ environment.name }}
    </h1>

    <!-- Section de gestion de l'environnement accessible uniquement si l'utilisateur peut gérer -->
    <div v-if="canManage" class="u-space-y-8">
      <section class="u-p-6 u-border u-border-gray-300 u-rounded-lg">
        <h2 class="u-text-2xl u-font-semibold u-mb-4">Modifier l'environnement</h2>
        <form @submit.prevent="updateEnv" class="u-space-y-4">
          <div>
            <label for="envName" class="u-block u-text-sm u-font-medium u-text-gray-700 u-mb-2">
              Nom de l'environnement
            </label>
            <input
              id="envName"
              type="text"
              v-model="envName"
              class="u-w-full u-px-3 u-py-2 u-border u-border-gray-300 u-rounded u-focus:outline-none u-focus:ring-2 u-focus:ring-blue-500"
            />
          </div>
          <button
            type="submit"
            class="u-px-4 u-py-2 u-bg-blue-500 u-text-white u-rounded u-hover:bg-blue-600 u-mr-2"
          >
            Mettre à jour
          </button>
        </form>
        <button
          @click="deleteEnv"
          class="u-px-4 u-py-2 u-bg-red-500 u-text-white u-rounded u-hover:bg-red-600 u-mt-4"
        >
          Supprimer l'environnement
        </button>
      </section>

      <section class="u-p-6 u-border u-border-gray-300 u-rounded-lg">
        <h2 class="u-text-2xl u-font-semibold u-mb-4">Gestion des éléments</h2>
        <button
          @click="toggleElementForm"
          class="u-px-4 u-py-2 u-bg-green-500 u-text-white u-rounded u-hover:bg-green-600 u-mb-4"
        >
          {{ showElementForm ? 'Annuler' : 'Créer un élément' }}
        </button>
        <div v-if="showElementForm" class="u-p-4 u-bg-gray-50 u-rounded">
          <form @submit.prevent="createElement" class="u-space-y-4">
            <div>
              <label for="elemName" class="u-block u-text-sm u-font-medium u-text-gray-700 u-mb-2">
                Nom de l'élément
              </label>
              <input
                id="elemName"
                type="text"
                v-model="newElement.name"
                class="u-w-full u-px-3 u-py-2 u-border u-border-gray-300 u-rounded u-focus:outline-none u-focus:ring-2 u-focus:ring-blue-500"
              />
            </div>
            <div>
              <label for="elemDesc" class="u-block u-text-sm u-font-medium u-text-gray-700 u-mb-2">
                Description
              </label>
              <input
                id="elemDesc"
                type="text"
                v-model="newElement.description"
                class="u-w-full u-px-3 u-py-2 u-border u-border-gray-300 u-rounded u-focus:outline-none u-focus:ring-2 u-focus:ring-blue-500"
              />
            </div>
            <button
              type="submit"
              class="u-px-4 u-py-2 u-bg-blue-500 u-text-white u-rounded u-hover:bg-blue-600"
            >
              Créer l'élément
            </button>
          </form>
        </div>
      </section>
    </div>

    <!-- Section de consultation (accessible à tous) -->
    <section class="u-mt-8">
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
          class="u-flex u-justify-between u-items-center u-p-4 u-bg-white u-border u-border-gray-200 u-rounded-lg u-shadow-sm"
        >
          <div>
            <h3 class="u-font-semibold u-text-lg u-text-gray-900">
              {{ element.name }}
            </h3>
            <p class="u-text-gray-600">
              {{ element.description }}
            </p>
          </div>
          <!-- Si l'utilisateur peut gérer, on affiche le bouton de suppression -->
          <button
            v-if="canManage"
            @click="deleteElement(element.id)"
            class="u-px-3 u-py-1 u-bg-red-500 u-text-white u-rounded u-text-sm u-hover:bg-red-600"
          >
            Supprimer
          </button>
        </li>
      </ul>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getEnvironment, updateEnvironment, deleteEnvironment } from '@/services/environmentService'
import { listElements, createElement as createElementService, deleteElement as deleteElementService } from '@/services/elementService'
import { useAuthStore } from '@/store/auth'
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
const router = useRouter()
const authStore = useAuthStore()
const notificationStore = useNotificationStore()
const envId = Number(route.params.envId)

// Données de l'environnement
const environment = ref<Environment>({ id: 0, name: '' })
const envName = ref('')

// Liste des éléments de l'environnement
const elements = ref<Element[]>([])
const showElementForm = ref(false)
const newElement = ref({ name: '', description: '' })

// Détermine si l'utilisateur a le droit de gérer l'environnement
const canManage = computed(() => {
  return authStore.user?.is_superadmin || authStore.isEnvironmentAdmin(envId)
})

// Récupère les informations de l'environnement
const fetchEnvironment = async () => {
  try {
    const response = await getEnvironment(envId)
    environment.value = response.data.data
    envName.value = environment.value.name
  } catch (error) {
    notificationStore.addNotification({
      type: 'error',
      message: "Erreur lors de la récupération de l'environnement"
    })
  }
}

// Récupère la liste des éléments
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

// Met à jour le nom de l'environnement
const updateEnv = async () => {
  try {
    await updateEnvironment(envId, { name: envName.value })
    await fetchEnvironment()
    notificationStore.addNotification({
      type: 'success',
      message: "Environnement mis à jour avec succès"
    })
  } catch (error) {
    notificationStore.addNotification({
      type: 'error',
      message: "Erreur lors de la mise à jour de l'environnement"
    })
  }
}

// Supprime l'environnement et redirige vers le dashboard
const deleteEnv = async () => {
  try {
    await deleteEnvironment(envId)
    notificationStore.addNotification({
      type: 'success',
      message: "Environnement supprimé avec succès"
    })
    router.push({ name: 'Dashboard' })
  } catch (error) {
    notificationStore.addNotification({
      type: 'error',
      message: "Erreur lors de la suppression de l'environnement"
    })
  }
}

// Gestion des éléments
const toggleElementForm = () => {
  showElementForm.value = !showElementForm.value
}

const createElement = async () => {
  try {
    await createElementService(envId, newElement.value)
    newElement.value = { name: '', description: '' }
    showElementForm.value = false
    await fetchElements()
    notificationStore.addNotification({
      type: 'success',
      message: "Élément créé avec succès"
    })
  } catch (error) {
    notificationStore.addNotification({
      type: 'error',
      message: "Erreur lors de la création de l'élément"
    })
  }
}

const deleteElement = async (elementId: number) => {
  try {
    await deleteElementService(elementId)
    await fetchElements()
    notificationStore.addNotification({
      type: 'success',
      message: "Élément supprimé avec succès"
    })
  } catch (error) {
    notificationStore.addNotification({
      type: 'error',
      message: "Erreur lors de la suppression de l'élément"
    })
  }
}

onMounted(() => {
  fetchEnvironment()
  fetchElements()
})
</script>
