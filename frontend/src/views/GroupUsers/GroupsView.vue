<!-- src/views/GroupsUsers/GroupsView.vue -->
<template>
  <div class="u-p-6">
    <h1 class="u-text-3xl u-font-bold u-mb-6">Gestion des Groupes</h1>

    <!-- Filtre de recherche -->
    <div class="u-mb-4">
      <input
        type="text"
        v-model="filterName"
        placeholder="Rechercher par nom"
        @input="applyFilter"
        class="u-px-3 u-py-2 u-border u-border-gray-300 u-rounded u-w-64 u-focus:outline-none u-focus:ring-2 u-focus:ring-blue-500"
      />
    </div>

    <!-- Bouton pour afficher/masquer le formulaire de création -->
    <button
      @click="toggleForm"
      class="u-px-4 u-py-2 u-bg-blue-500 u-text-white u-rounded u-hover:bg-blue-600 u-mb-4"
    >
      {{ showForm ? 'Annuler' : 'Créer un groupe' }}
    </button>

    <!-- Formulaire de création -->
    <div v-if="showForm && !editingGroup" class="u-mb-6">
      <GroupForm :environmentId="environmentId" @success="onFormSuccess" />
    </div>

    <!-- Tableau listant les groupes -->
    <table class="u-w-full u-border-collapse u-mt-4">
      <thead>
        <tr class="u-bg-gray-100">
          <th class="u-border u-border-gray-300 u-px-4 u-py-2 u-text-left">ID</th>
          <th class="u-border u-border-gray-300 u-px-4 u-py-2 u-text-left">Nom</th>
          <th class="u-border u-border-gray-300 u-px-4 u-py-2 u-text-left">Description</th>
          <th class="u-border u-border-gray-300 u-px-4 u-py-2 u-text-left">Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="group in groupsStore.groups" :key="group.id" class="u-hover:bg-gray-50">
          <td class="u-border u-border-gray-300 u-px-4 u-py-2">{{ group.id }}</td>
          <td class="u-border u-border-gray-300 u-px-4 u-py-2">{{ group.name }}</td>
          <td class="u-border u-border-gray-300 u-px-4 u-py-2">{{ group.description }}</td>
          <td class="u-border u-border-gray-300 u-px-4 u-py-2">
            <div class="u-space-x-2">
              <button
                @click="editGroup(group)"
                class="u-px-2 u-py-1 u-bg-yellow-500 u-text-white u-rounded u-text-sm u-hover:bg-yellow-600"
              >
                Modifier
              </button>
              <button
                @click="deleteGroup(group.id)"
                class="u-px-2 u-py-1 u-bg-red-500 u-text-white u-rounded u-text-sm u-hover:bg-red-600"
              >
                Supprimer
              </button>
              <button
                @click="manageFunctions(group)"
                class="u-px-2 u-py-1 u-bg-green-500 u-text-white u-rounded u-text-sm u-hover:bg-green-600"
              >
                Gérer Fonctions
              </button>
            </div>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- Pagination -->
    <div class="u-mt-4 u-flex u-items-center u-gap-4">
      <p>Total : {{ groupsStore.total }}</p>
      <button
        :disabled="groupsStore.currentPage === 1"
        @click="prevPage"
        class="u-px-3 u-py-1 u-bg-gray-500 u-text-white u-rounded u-disabled:opacity-50 u-disabled:cursor-not-allowed u-hover:bg-gray-600"
      >
        Précédent
      </button>
      <span class="u-font-medium">Page {{ groupsStore.currentPage }}</span>
      <button
        :disabled="groupsStore.groups.length < groupsStore.perPage"
        @click="nextPage"
        class="u-px-3 u-py-1 u-bg-gray-500 u-text-white u-rounded u-disabled:opacity-50 u-disabled:cursor-not-allowed u-hover:bg-gray-600"
      >
        Suivant
      </button>
    </div>

    <!-- Formulaire d'édition -->
    <div v-if="editingGroup" class="u-mt-6 u-p-4 u-border u-border-gray-300 u-rounded">
      <h2 class="u-text-xl u-font-bold u-mb-4">Modifier le groupe</h2>
      <GroupForm
        :environmentId="environmentId"
        :initialData="editingGroup"
        @success="onFormSuccess"
      />
      <button
        @click="cancelEdit"
        class="u-px-4 u-py-2 u-bg-gray-500 u-text-white u-rounded u-mt-4 u-hover:bg-gray-600"
      >
        Annuler
      </button>
    </div>

    <!-- Modal pour la gestion des fonctions du groupe -->
    <div
      v-if="showFunctionManager"
      class="u-fixed u-top-0 u-left-0 u-right-0 u-bottom-0 u-bg-black u-bg-opacity-50 u-flex u-justify-center u-items-center"
    >
      <div class="u-bg-white u-p-6 u-rounded-lg u-w-4/5 u-max-w-4xl">
        <h2 class="u-text-xl u-font-bold u-mb-4">
          Gérer les fonctions du groupe "{{ managingGroup?.name }}"
        </h2>
        <GroupFunctionsManager :groupId="managingGroup?.id" />
        <button
          @click="closeFunctionManager"
          class="u-px-4 u-py-2 u-bg-gray-500 u-text-white u-rounded u-mt-4 u-hover:bg-gray-600"
        >
          Fermer
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import GroupForm from '@/components/GroupForm.vue'
import { useGroupsStore } from '@/store/groups'
import { deleteGroup as deleteGroupService } from '@/services/groupService'
import { useNotificationStore } from '@/store/notifications'
import GroupFunctionsManager from '@/components/GroupFunctionsManager.vue'

interface Group {
  id: number
  name: string
  description: string
}

// Pour cet exemple, l'ID de l'environnement est fixé à 1 (adaptable dynamiquement)
const environmentId = 1
const groupsStore = useGroupsStore()
const notificationStore = useNotificationStore()

const filterName = ref('')
const showForm = ref(false)
const editingGroup = ref<Group | null>(null)
const managingGroup = ref<Group | null>(null)
const showFunctionManager = ref(false)

const fetchGroups = async () => {
  await groupsStore.fetchGroups(environmentId)
}

const applyFilter = () => {
  groupsStore.filters.name = filterName.value
  groupsStore.currentPage = 1
  fetchGroups()
}

const prevPage = () => {
  if (groupsStore.currentPage > 1) {
    groupsStore.currentPage--
    fetchGroups()
  }
}

const nextPage = () => {
  groupsStore.currentPage++
  fetchGroups()
}

const deleteGroup = async (groupId: number) => {
  try {
    await deleteGroupService(groupId)
    notificationStore.addNotification({
      type: 'success',
      message: 'Groupe supprimé avec succès',
    })
    fetchGroups()
  } catch (error) {
    notificationStore.addNotification({
      type: 'error',
      message: 'Erreur lors de la suppression du groupe',
    })
  }
}

const editGroup = (group: Group) => {
  editingGroup.value = group
}

const cancelEdit = () => {
  editingGroup.value = null
}

const onFormSuccess = () => {
  editingGroup.value = null
  showForm.value = false
  fetchGroups()
}

const toggleForm = () => {
  showForm.value = !showForm.value
}

// Ouvre la modal de gestion des fonctions pour le groupe sélectionné
const manageFunctions = (group: Group) => {
  managingGroup.value = group
  showFunctionManager.value = true
}

const closeFunctionManager = () => {
  showFunctionManager.value = false
}

// Chargement initial
onMounted(() => {
  fetchGroups()
})
</script>
