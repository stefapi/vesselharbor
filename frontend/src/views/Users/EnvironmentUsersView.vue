<!-- src/views/Users/EnvironmentUsersView.vue -->
<template>
  <div class="u-p-6">
    <h1 class="u-text-2xl u-font-bold u-mb-4">Utilisateurs de l'Environnement {{ environmentId }}</h1>

    <div class="u-mb-4">
      <input v-model="filterEmail" type="text" placeholder="Rechercher par email" class="u-px-3 u-py-2 u-border u-border-gray-300 u-rounded u-w-64" @input="applyFilter" />
    </div>

    <button class="u-px-4 u-py-2 u-bg-blue-500 u-text-white u-rounded u-hover:bg-blue-600 u-mb-4" @click="toggleForm">
      {{ showForm ? 'Annuler' : 'Créer un utilisateur' }}
    </button>

    <div v-if="showForm && !editingUser" class="u-mb-4">
      <UserForm mode="create" @success="onFormSuccess" />
    </div>

    <table class="u-w-full u-border-collapse u-mt-4">
      <thead>
        <tr class="u-bg-gray-100">
          <th class="u-border u-border-gray-300 u-px-2 u-py-2 u-text-left">ID</th>
          <th class="u-border u-border-gray-300 u-px-2 u-py-2 u-text-left">Email</th>
          <th class="u-border u-border-gray-300 u-px-2 u-py-2 u-text-left">Superadmin</th>
          <th class="u-border u-border-gray-300 u-px-2 u-py-2 u-text-left">Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in usersStore.users" :key="user.id" class="u-hover:bg-gray-50">
          <td class="u-border u-border-gray-300 u-px-2 u-py-2">{{ user.id }}</td>
          <td class="u-border u-border-gray-300 u-px-2 u-py-2">{{ user.email }}</td>
          <td class="u-border u-border-gray-300 u-px-2 u-py-2">
            {{ user.is_superadmin ? 'Oui' : 'Non' }}
          </td>
          <td class="u-border u-border-gray-300 u-px-2 u-py-2">
            <button class="u-px-2 u-py-1 u-bg-yellow-500 u-text-white u-rounded u-text-sm u-mr-2 u-hover:bg-yellow-600" @click="editUser(user)">Modifier</button>
            <button class="u-px-2 u-py-1 u-bg-red-500 u-text-white u-rounded u-text-sm u-mr-2 u-hover:bg-red-600" @click="deleteUser(user.id)">Supprimer</button>
            <button class="u-px-2 u-py-1 u-bg-green-500 u-text-white u-rounded u-text-sm u-hover:bg-green-600" @click="manageGroups(user)">Gérer Groupes</button>
          </td>
        </tr>
      </tbody>
    </table>

    <div class="u-mt-4 u-flex u-items-center u-gap-4">
      <p>Total : {{ usersStore.total }}</p>
      <button :disabled="usersStore.currentPage === 1" class="u-px-3 u-py-1 u-bg-gray-500 u-text-white u-rounded u-disabled:opacity-50 u-disabled:cursor-not-allowed u-hover:bg-gray-600" @click="prevPage">
        Précédent
      </button>
      <span class="u-font-medium">Page {{ usersStore.currentPage }}</span>
      <button :disabled="usersStore.users.length < usersStore.perPage" class="u-px-3 u-py-1 u-bg-gray-500 u-text-white u-rounded u-disabled:opacity-50 u-disabled:cursor-not-allowed u-hover:bg-gray-600" @click="nextPage">
        Suivant
      </button>
    </div>

    <div v-if="editingUser" class="u-mt-6 u-p-4 u-border u-border-gray-300 u-rounded">
      <h2 class="u-text-xl u-font-bold u-mb-4">Modifier l'utilisateur</h2>
      <UserForm mode="edit" :initialData="editingUser" @success="onFormSuccess" />
      <button class="u-px-4 u-py-2 u-bg-gray-500 u-text-white u-rounded u-mt-4 u-hover:bg-gray-600" @click="cancelEdit">Annuler</button>
    </div>

    <!-- Modal pour la gestion des groupes -->
    <div v-if="showGroupManager" class="u-fixed u-top-0 u-left-0 u-right-0 u-bottom-0 u-bg-black u-bg-opacity-50 u-flex u-justify-center u-items-center">
      <div class="u-bg-white u-p-4 u-rounded-lg u-w-4/5 u-max-w-2xl">
        <h2 class="u-text-xl u-font-bold u-mb-4">Gestion des Groupes pour {{ managingUser?.email }}</h2>
        <UserGroupsManager v-if="managingUser?.id" :userId="managingUser.id" :environmentId="environmentId" />
        <button class="u-px-4 u-py-2 u-bg-gray-500 u-text-white u-rounded u-mt-4 u-hover:bg-gray-600" @click="closeGroupManager">Fermer</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRoute } from 'vue-router'
import UserForm from '@/components/business/Users/UserForm.vue'
import { useUsersStore } from '@/store/users'
import { deleteauser } from '@/api'
import { useNotificationStore } from '@/store/notifications'
import UserGroupsManager from '@/components/business/Users/UserGroupsManager.vue'
import type { User } from '@/types/user'

const route = useRoute()
const environmentId = Number(route.params.envId)
const usersStore = useUsersStore()
const notificationStore = useNotificationStore()
const filterEmail = ref('')
const showForm = ref(false)
const editingUser = ref<User | null>(null)
const managingUser = ref<User | null>(null)
const showGroupManager = ref(false)

const fetchUsers = async () => {
  await usersStore.fetchUsers()
  // Ici, vous pouvez filtrer par environnement si l'API le supporte
}

fetchUsers()

const applyFilter = () => {
  usersStore.filters.email = filterEmail.value
  usersStore.currentPage = 1
  fetchUsers()
}

const prevPage = () => {
  if (usersStore.currentPage > 1) {
    usersStore.currentPage--
    fetchUsers()
  }
}

const nextPage = () => {
  usersStore.currentPage++
  fetchUsers()
}

const deleteUser = async (userId: number) => {
  try {
    await deleteauser(userId)
    notificationStore.addNotification({
      type: 'success',
      message: 'Utilisateur supprimé avec succès',
    })
    fetchUsers()
  } catch (error) {
    notificationStore.addNotification({
      type: 'error',
      message: "Erreur lors de la suppression de l'utilisateur",
    })
  }
}

const editUser = (user: User) => {
  editingUser.value = user
}

const cancelEdit = () => {
  editingUser.value = null
}

const onFormSuccess = () => {
  editingUser.value = null
  showForm.value = false
  fetchUsers()
}

const toggleForm = () => {
  showForm.value = !showForm.value
}

const manageGroups = (user: User) => {
  managingUser.value = user
  showGroupManager.value = true
}

const closeGroupManager = () => {
  showGroupManager.value = false
}
</script>
