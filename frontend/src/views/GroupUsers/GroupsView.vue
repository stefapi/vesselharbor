<!-- src/views/GroupUsers/GroupsView.vue -->
<template>
  <div class="u-p-6">
    <h1 class="u-text-3xl u-font-bold u-mb-6">Gestion des Groupes</h1>

    <!-- Loading indicator -->
    <div v-if="groupsStore.loading" class="u-mb-4">
      <p class="u-text-gray-600">Chargement des groupes...</p>
    </div>

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
    <button @click="toggleForm" class="u-px-4 u-py-2 u-bg-blue-500 u-text-white u-rounded u-hover:bg-blue-600 u-mb-4">
      {{ showForm ? 'Annuler' : 'Créer un groupe' }}
    </button>

    <!-- Formulaire de création -->
    <div v-if="showForm && !editingGroup" class="u-mb-6">
      <GroupForm @success="onFormSuccess" />
    </div>

    <!-- Tableau listant les groupes -->
    <div v-if="!groupsStore.loading">
      <table class="u-w-full u-border-collapse u-mt-4">
        <thead>
          <tr class="u-bg-gray-100">
            <th class="u-border u-border-gray-300 u-px-4 u-py-2 u-text-left">ID</th>
            <th class="u-border u-border-gray-300 u-px-4 u-py-2 u-text-left">Nom</th>
            <th class="u-border u-border-gray-300 u-px-4 u-py-2 u-text-left">Description</th>
            <th class="u-border u-border-gray-300 u-px-4 u-py-2 u-text-left">Organisation</th>
            <th class="u-border u-border-gray-300 u-px-4 u-py-2 u-text-left">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="group in groupsStore.paginatedGroups" :key="group.id" class="u-hover:bg-gray-50">
            <td class="u-border u-border-gray-300 u-px-4 u-py-2">{{ group.id }}</td>
            <td class="u-border u-border-gray-300 u-px-4 u-py-2">{{ group.name }}</td>
            <td class="u-border u-border-gray-300 u-px-4 u-py-2">{{ group.description }}</td>
            <td class="u-border u-border-gray-300 u-px-4 u-py-2">{{ group.organization_id }}</td>
            <td class="u-border u-border-gray-300 u-px-4 u-py-2">
              <div class="u-space-x-2">
                <button @click="editGroup(group)" class="u-px-2 u-py-1 u-bg-yellow-500 u-text-white u-rounded u-text-sm u-hover:bg-yellow-600">Modifier</button>
                <button @click="deleteGroupAction(group.id)" class="u-px-2 u-py-1 u-bg-red-500 u-text-white u-rounded u-text-sm u-hover:bg-red-600">Supprimer</button>
                <button @click="manageUsers(group)" class="u-px-2 u-py-1 u-bg-blue-500 u-text-white u-rounded u-text-sm u-hover:bg-blue-600">Gérer Utilisateurs</button>
                <button @click="managePolicies(group)" class="u-px-2 u-py-1 u-bg-green-500 u-text-white u-rounded u-text-sm u-hover:bg-green-600">Gérer Politiques</button>
                <button @click="manageTags(group)" class="u-px-2 u-py-1 u-bg-purple-500 u-text-white u-rounded u-text-sm u-hover:bg-purple-600">Gérer Tags</button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- Pagination -->
      <div class="u-mt-4 u-flex u-items-center u-gap-4">
        <p>Total : {{ groupsStore.filteredGroups.length }} groupes</p>
        <button :disabled="groupsStore.currentPage === 1" @click="prevPage" class="u-px-3 u-py-1 u-bg-gray-500 u-text-white u-rounded u-disabled:opacity-50 u-disabled:cursor-not-allowed u-hover:bg-gray-600">
          Précédent
        </button>
        <span class="u-font-medium">Page {{ groupsStore.currentPage }} / {{ groupsStore.totalPages }}</span>
        <button
          :disabled="groupsStore.currentPage >= groupsStore.totalPages"
          @click="nextPage"
          class="u-px-3 u-py-1 u-bg-gray-500 u-text-white u-rounded u-disabled:opacity-50 u-disabled:cursor-not-allowed u-hover:bg-gray-600"
        >
          Suivant
        </button>
      </div>
    </div>

    <!-- Formulaire d'édition -->
    <div v-if="editingGroup" class="u-mt-6 u-p-4 u-border u-border-gray-300 u-rounded">
      <h2 class="u-text-xl u-font-bold u-mb-4">Modifier le groupe</h2>
      <GroupForm :initialData="editingGroup" @success="onFormSuccess" />
      <button @click="cancelEdit" class="u-px-4 u-py-2 u-bg-gray-500 u-text-white u-rounded u-mt-4 u-hover:bg-gray-600">Annuler</button>
    </div>

    <!-- Modal pour la gestion des utilisateurs du groupe -->
    <div v-if="showUserManager" class="u-fixed u-top-0 u-left-0 u-right-0 u-bottom-0 u-bg-black u-bg-opacity-50 u-flex u-justify-center u-items-center">
      <div class="u-bg-white u-p-6 u-rounded-lg u-w-4/5 u-max-w-4xl">
        <h2 class="u-text-xl u-font-bold u-mb-4">Gérer les utilisateurs du groupe "{{ managingGroup?.name }}"</h2>
        <GroupUsersManager :groupId="managingGroup?.id" />
        <button @click="closeUserManager" class="u-px-4 u-py-2 u-bg-gray-500 u-text-white u-rounded u-mt-4 u-hover:bg-gray-600">Fermer</button>
      </div>
    </div>

    <!-- Modal pour la gestion des politiques du groupe -->
    <div v-if="showPolicyManager" class="u-fixed u-top-0 u-left-0 u-right-0 u-bottom-0 u-bg-black u-bg-opacity-50 u-flex u-justify-center u-items-center">
      <div class="u-bg-white u-p-6 u-rounded-lg u-w-4/5 u-max-w-4xl">
        <h2 class="u-text-xl u-font-bold u-mb-4">Gérer les politiques du groupe "{{ managingGroup?.name }}"</h2>
        <GroupPoliciesManager :groupId="managingGroup?.id" />
        <button @click="closePolicyManager" class="u-px-4 u-py-2 u-bg-gray-500 u-text-white u-rounded u-mt-4 u-hover:bg-gray-600">Fermer</button>
      </div>
    </div>

    <!-- Modal pour la gestion des tags du groupe -->
    <div v-if="showTagManager" class="u-fixed u-top-0 u-left-0 u-right-0 u-bottom-0 u-bg-black u-bg-opacity-50 u-flex u-justify-center u-items-center">
      <div class="u-bg-white u-p-6 u-rounded-lg u-w-4/5 u-max-w-4xl">
        <h2 class="u-text-xl u-font-bold u-mb-4">Gérer les tags du groupe "{{ managingGroup?.name }}"</h2>
        <GroupTagsManager :groupId="managingGroup?.id" />
        <button @click="closeTagManager" class="u-px-4 u-py-2 u-bg-gray-500 u-text-white u-rounded u-mt-4 u-hover:bg-gray-600">Fermer</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import GroupForm from '@/components/business/Groups/GroupForm.vue'
import { useGroupsStore } from '@/store/group'
import { deleteGroup as deleteGroupService, type Group } from '@/services/groupService'
import { useNotificationStore } from '@/store/notifications'

// Import placeholder components (these would need to be created)
// import GroupUsersManager from '@/components/business/Groups/GroupUsersManager.vue'
// import GroupPoliciesManager from '@/components/business/Groups/GroupPoliciesManager.vue'
// import GroupTagsManager from '@/components/business/Groups/GroupTagsManager.vue'

const groupsStore = useGroupsStore()
const notificationStore = useNotificationStore()

const filterName = ref('')
const showForm = ref(false)
const editingGroup = ref<Group | null>(null)
const managingGroup = ref<Group | null>(null)
const showUserManager = ref(false)
const showPolicyManager = ref(false)
const showTagManager = ref(false)

const fetchGroups = async () => {
  try {
    await groupsStore.fetchGroups()
  } catch (error) {
    notificationStore.addNotification({
      type: 'error',
      message: 'Erreur lors du chargement des groupes',
    })
  }
}

const applyFilter = () => {
  groupsStore.setFilter(filterName.value)
}

const prevPage = () => {
  if (groupsStore.currentPage > 1) {
    groupsStore.setPage(groupsStore.currentPage - 1)
  }
}

const nextPage = () => {
  if (groupsStore.currentPage < groupsStore.totalPages) {
    groupsStore.setPage(groupsStore.currentPage + 1)
  }
}

const deleteGroupAction = async (groupId: number) => {
  if (!confirm('Êtes-vous sûr de vouloir supprimer ce groupe ?')) {
    return
  }

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

// Gestion des utilisateurs du groupe
const manageUsers = (group: Group) => {
  managingGroup.value = group
  showUserManager.value = true
}

const closeUserManager = () => {
  showUserManager.value = false
  managingGroup.value = null
}

// Gestion des politiques du groupe
const managePolicies = (group: Group) => {
  managingGroup.value = group
  showPolicyManager.value = true
}

const closePolicyManager = () => {
  showPolicyManager.value = false
  managingGroup.value = null
}

// Gestion des tags du groupe
const manageTags = (group: Group) => {
  managingGroup.value = group
  showTagManager.value = true
}

const closeTagManager = () => {
  showTagManager.value = false
  managingGroup.value = null
}

// Chargement initial
onMounted(() => {
  fetchGroups()
})
</script>
