<!-- src/views/Environments/EnvironmentManagementView.vue -->
<template>
  <div class="u-p-6">
    <h1 class="u-text-3xl u-font-bold u-mb-6">
      Gestion de l'Environnement : {{ environment.name }}
    </h1>

    <!-- Section Modification de l'environnement -->
    <section class="u-mb-8 u-p-4 u-border u-border-gray-300 u-rounded">
      <h2 class="u-text-2xl u-font-semibold u-mb-4">Modifier l'environnement</h2>
      <form @submit.prevent="updateEnv" class="u-mb-4">
        <div class="u-mb-4">
          <label for="envName" class="u-block u-text-sm u-font-medium u-mb-2">
            Nom de l'environnement
          </label>
          <input
            type="text"
            id="envName"
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
        class="u-px-4 u-py-2 u-bg-red-500 u-text-white u-rounded u-hover:bg-red-600"
      >
        Supprimer l'environnement
      </button>
    </section>

    <!-- Section Gestion des éléments -->
    <section class="u-mb-8 u-p-4 u-border u-border-gray-300 u-rounded">
      <h2 class="u-text-2xl u-font-semibold u-mb-4">Gestion des éléments</h2>
      <button
        @click="toggleElementForm"
        class="u-px-4 u-py-2 u-bg-green-500 u-text-white u-rounded u-hover:bg-green-600 u-mb-4"
      >
        {{ showElementForm ? 'Annuler' : 'Créer un élément' }}
      </button>

      <div v-if="showElementForm" class="u-mb-4 u-p-4 u-bg-gray-50 u-rounded">
        <form @submit.prevent="createElement">
          <div class="u-mb-4">
            <label for="elemName" class="u-block u-text-sm u-font-medium u-mb-2">
              Nom de l'élément
            </label>
            <input
              type="text"
              id="elemName"
              v-model="newElement.name"
              class="u-w-full u-px-3 u-py-2 u-border u-border-gray-300 u-rounded u-focus:outline-none u-focus:ring-2 u-focus:ring-blue-500"
            />
          </div>
          <div class="u-mb-4">
            <label for="elemDesc" class="u-block u-text-sm u-font-medium u-mb-2">
              Description
            </label>
            <input
              type="text"
              id="elemDesc"
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

      <h3 class="u-text-xl u-font-semibold u-mb-3">Liste des éléments</h3>
      <ul class="u-space-y-2">
        <li
          v-for="element in elements"
          :key="element.id"
          class="u-flex u-justify-between u-items-center u-p-3 u-bg-white u-border u-border-gray-200 u-rounded"
        >
          <span>{{ element.name }} - {{ element.description }}</span>
          <button
            @click="deleteElement(element.id)"
            class="u-px-3 u-py-1 u-bg-red-500 u-text-white u-rounded u-text-sm u-hover:bg-red-600"
          >
            Supprimer
          </button>
        </li>
      </ul>
    </section>

    <!-- Section Gestion des utilisateurs -->
    <section class="u-mb-8 u-p-4 u-border u-border-gray-300 u-rounded">
      <h2 class="u-text-2xl u-font-semibold u-mb-4">Utilisateurs de l'environnement</h2>
      <ul class="u-space-y-2">
        <li
          v-for="user in users"
          :key="user.id"
          class="u-flex u-justify-between u-items-center u-p-3 u-bg-white u-border u-border-gray-200 u-rounded"
        >
          <span>{{ user.email }} - {{ user.role }}</span>
          <button
            @click="editUserRights(user)"
            class="u-px-3 u-py-1 u-bg-yellow-500 u-text-white u-rounded u-text-sm u-hover:bg-yellow-600"
          >
            Modifier droits
          </button>
        </li>
      </ul>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getEnvironment, updateEnvironment, deleteEnvironment } from '@/services/environmentService'
import { listElements, createElement as createElementService, deleteElement as deleteElementService } from '@/services/elementService'
import { listEnvironmentUsers } from '@/services/environmentUserService'
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

interface User {
  id: number
  email: string
  role: string
}

const route = useRoute()
const router = useRouter()
const notificationStore = useNotificationStore()
const envId = Number(route.params.envId)
const environment = ref<Environment>({ id: 0, name: '' })
const envName = ref('')

// Gestion des éléments
const elements = ref<Element[]>([])
const showElementForm = ref(false)
const newElement = ref({ name: '', description: '' })

// Gestion des utilisateurs de l'environnement
const users = ref<User[]>([])

const fetchEnvironment = async () => {
  try {
    const response = await getEnvironment(envId)
    environment.value = response.data.data
    envName.value = environment.value.name
  } catch (error) {
    notificationStore.addNotification({
      type: 'error',
      message: 'Erreur lors de la récupération de l\'environnement'
    })
  }
}

const updateEnv = async () => {
  try {
    await updateEnvironment(envId, { name: envName.value })
    await fetchEnvironment()
    notificationStore.addNotification({
      type: 'success',
      message: 'Environnement mis à jour avec succès'
    })
  } catch (error) {
    notificationStore.addNotification({
      type: 'error',
      message: 'Erreur lors de la mise à jour de l\'environnement'
    })
  }
}

const deleteEnv = async () => {
  try {
    await deleteEnvironment(envId)
    notificationStore.addNotification({
      type: 'success',
      message: 'Environnement supprimé avec succès'
    })
    router.push({ name: 'Dashboard' })
  } catch (error) {
    notificationStore.addNotification({
      type: 'error',
      message: 'Erreur lors de la suppression de l\'environnement'
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
      message: 'Erreur lors de la récupération des éléments'
    })
  }
}

const toggleElementForm = () => {
  showElementForm.value = !showElementForm.value
}

const createElement = async () => {
  try {
    await createElementService(envId, newElement.value)
    newElement.value = { name: '', description: '' }
    showElementForm.value = false
    fetchElements()
    notificationStore.addNotification({
      type: 'success',
      message: 'Élément créé avec succès'
    })
  } catch (error) {
    notificationStore.addNotification({
      type: 'error',
      message: 'Erreur lors de la création de l\'élément'
    })
  }
}

const deleteElement = async (elementId: number) => {
  try {
    await deleteElementService(elementId)
    fetchElements()
    notificationStore.addNotification({
      type: 'success',
      message: 'Élément supprimé avec succès'
    })
  } catch (error) {
    notificationStore.addNotification({
      type: 'error',
      message: 'Erreur lors de la suppression de l\'élément'
    })
  }
}

const fetchUsers = async () => {
  try {
    const response = await listEnvironmentUsers(envId, {})
    users.value = response.data.data
  } catch (error) {
    notificationStore.addNotification({
      type: 'error',
      message: 'Erreur lors de la récupération des utilisateurs'
    })
  }
}

const editUserRights = (user: User) => {
  notificationStore.addNotification({
    type: 'info',
    message: 'Fonction de modification des droits non implémentée'
  })
}

onMounted(() => {
  fetchEnvironment()
  fetchElements()
  fetchUsers()
})
</script>
