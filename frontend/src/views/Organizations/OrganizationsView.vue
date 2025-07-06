<!--
  - Copyright (c) 2025.  VesselHarbor
  -
  - ____   ____                          .__    ___ ___             ___.
  - \   \ /   /____   ______ ______ ____ |  |  /   |   \_____ ______\_ |__   ___________
  -  \   Y   // __ \ /  ___//  ___// __ \|  | /    ~    \__  \\_  __ \ __ \ /  _ \_  __ \
  -   \     /\  ___/ \___ \ \___ \\  ___/|  |_\    Y    // __ \|  | \/ \_\ (  <_> )  | \/
  -    \___/  \___  >____  >____  >\___  >____/\___|_  /(____  /__|  |___  /\____/|__|
  -               \/     \/     \/     \/            \/      \/          \/
  -
  -
  - MIT License
  -
  - Permission is hereby granted, free of charge, to any person obtaining a copy
  - of this software and associated documentation files (the "Software"), to deal
  - in the Software without restriction, including without limitation the rights
  - to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
  - copies of the Software, and to permit persons to whom the Software is
  - furnished to do so, subject to the following conditions:
  -
  - The above copyright notice and this permission notice shall be included in all
  - copies or substantial portions of the Software.
  -
  - THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
  - IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
  - FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
  - AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
  - LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
  - OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
  - SOFTWARE.
  -
  -->

<!-- src/views/Organizations/OrganizationsView.vue -->
<template>
  <div class="u-p-6">
    <h1 class="u-text-3xl u-font-bold u-mb-6">Gestion des Organisations</h1>

    <!-- Loading indicator -->
    <div v-if="organizationsStore.loading" class="u-mb-4">
      <p class="u-text-gray-600">Chargement des organisations...</p>
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
      {{ showForm ? 'Annuler' : 'Créer une organisation' }}
    </button>

    <!-- Formulaire de création -->
    <div v-if="showForm && !editingOrganization" class="u-mb-6">
      <OrganizationForm @success="onFormSuccess" />
    </div>

    <!-- Tableau listant les organisations -->
    <div v-if="!organizationsStore.loading">
      <table class="u-w-full u-border-collapse u-mt-4">
        <thead>
          <tr class="u-bg-gray-100">
            <th class="u-border u-border-gray-300 u-px-4 u-py-2 u-text-left">ID</th>
            <th class="u-border u-border-gray-300 u-px-4 u-py-2 u-text-left">Nom</th>
            <th class="u-border u-border-gray-300 u-px-4 u-py-2 u-text-left">Description</th>
            <th class="u-border u-border-gray-300 u-px-4 u-py-2 u-text-left">Utilisateurs</th>
            <th class="u-border u-border-gray-300 u-px-4 u-py-2 u-text-left">Environnements</th>
            <th class="u-border u-border-gray-300 u-px-4 u-py-2 u-text-left">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="organization in organizationsStore.paginatedOrganizations" :key="organization.id" class="u-hover:bg-gray-50">
            <td class="u-border u-border-gray-300 u-px-4 u-py-2">{{ organization.id }}</td>
            <td class="u-border u-border-gray-300 u-px-4 u-py-2">{{ organization.name }}</td>
            <td class="u-border u-border-gray-300 u-px-4 u-py-2">{{ organization.description || '-' }}</td>
            <td class="u-border u-border-gray-300 u-px-4 u-py-2">{{ organization.users?.length || 0 }}</td>
            <td class="u-border u-border-gray-300 u-px-4 u-py-2">{{ organization.environments?.length || 0 }}</td>
            <td class="u-border u-border-gray-300 u-px-4 u-py-2">
              <el-dropdown trigger="click" @command="(cmd) => handleCommand(cmd, organization)">
                <el-button text>
                  <i-mdi-dots-vertical class="u-text-xl" />
                </el-button>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item command="edit">
                      <i-mdi-pencil class="u-mr-1" /> Modifier
                    </el-dropdown-item>
                    <el-dropdown-item command="delete">
                      <i-mdi-delete class="u-mr-1" /> Supprimer
                    </el-dropdown-item>
                    <el-dropdown-item command="manage-users">
                      <i-mdi-account-multiple class="u-mr-1" /> Gérer Utilisateurs
                    </el-dropdown-item>
                    <el-dropdown-item command="manage-groups">
                      <i-mdi-account-group class="u-mr-1" /> Gérer Groupes
                    </el-dropdown-item>
                    <el-dropdown-item command="manage-environments">
                      <i-mdi-earth class="u-mr-1" /> Gérer Environnements
                    </el-dropdown-item>
                  </el-dropdown-menu>
                </template>
              </el-dropdown>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- Pagination -->
      <div class="u-mt-4 u-flex u-items-center u-gap-4">
        <p>Total : {{ organizationsStore.filteredOrganizations.length }} organisations</p>
        <button :disabled="organizationsStore.currentPage === 1" @click="prevPage" class="u-px-3 u-py-1 u-bg-gray-500 u-text-white u-rounded u-disabled:opacity-50 u-disabled:cursor-not-allowed u-hover:bg-gray-600">
          Précédent
        </button>
        <span class="u-font-medium">Page {{ organizationsStore.currentPage }} / {{ organizationsStore.totalPages }}</span>
        <button
          :disabled="organizationsStore.currentPage >= organizationsStore.totalPages"
          @click="nextPage"
          class="u-px-3 u-py-1 u-bg-gray-500 u-text-white u-rounded u-disabled:opacity-50 u-disabled:cursor-not-allowed u-hover:bg-gray-600"
        >
          Suivant
        </button>
      </div>
    </div>

    <!-- Formulaire d'édition -->
    <div v-if="editingOrganization" class="u-mt-6 u-p-4 u-border u-border-gray-300 u-rounded">
      <h2 class="u-text-xl u-font-bold u-mb-4">Modifier l'organisation</h2>
      <OrganizationForm :initialData="editingOrganization" @success="onFormSuccess" />
      <button @click="cancelEdit" class="u-px-4 u-py-2 u-bg-gray-500 u-text-white u-rounded u-mt-4 u-hover:bg-gray-600">Annuler</button>
    </div>

    <!-- Confirmation de suppression -->
    <div v-if="deletingOrganization" class="u-mt-6 u-p-4 u-border u-border-red-300 u-rounded u-bg-red-50">
      <h2 class="u-text-xl u-font-bold u-mb-4 u-text-red-700">Confirmer la suppression</h2>
      <p class="u-mb-4 u-text-gray-700">
        Êtes-vous sûr de vouloir supprimer l'organisation <strong>"{{ deletingOrganization.name }}"</strong> ?
        Cette action est irréversible.
      </p>
      <div class="u-flex u-gap-4">
        <button @click="confirmDelete" class="u-px-4 u-py-2 u-bg-red-500 u-text-white u-rounded u-hover:bg-red-600">
          Confirmer la suppression
        </button>
        <button @click="cancelDelete" class="u-px-4 u-py-2 u-bg-gray-500 u-text-white u-rounded u-hover:bg-gray-600">
          Annuler
        </button>
      </div>
    </div>

    <!-- Modal pour la gestion des utilisateurs de l'organisation -->
    <div v-if="showUserManager" class="u-fixed u-top-0 u-left-0 u-right-0 u-bottom-0 u-bg-black u-bg-opacity-50 u-flex u-justify-center u-items-center">
      <div class="u-bg-white u-p-6 u-rounded-lg u-w-4/5 u-max-w-4xl">
        <h2 class="u-text-xl u-font-bold u-mb-4">Gérer les utilisateurs de l'organisation "{{ managingOrganization?.name }}"</h2>
        <OrganizationUsersManager :organizationId="managingOrganization?.id" />
        <button @click="closeUserManager" class="u-px-4 u-py-2 u-bg-gray-500 u-text-white u-rounded u-mt-4 u-hover:bg-gray-600">Fermer</button>
      </div>
    </div>

    <!-- Modal pour la gestion des groupes de l'organisation -->
    <div v-if="showGroupManager" class="u-fixed u-top-0 u-left-0 u-right-0 u-bottom-0 u-bg-black u-bg-opacity-50 u-flex u-justify-center u-items-center">
      <div class="u-bg-white u-p-6 u-rounded-lg u-w-4/5 u-max-w-4xl">
        <h2 class="u-text-xl u-font-bold u-mb-4">Gérer les groupes de l'organisation "{{ managingOrganization?.name }}"</h2>
        <OrganizationGroupsManager :organizationId="managingOrganization?.id" />
        <button @click="closeGroupManager" class="u-px-4 u-py-2 u-bg-gray-500 u-text-white u-rounded u-mt-4 u-hover:bg-gray-600">Fermer</button>
      </div>
    </div>

    <!-- Modal pour la gestion des environnements de l'organisation -->
    <div v-if="showEnvironmentManager" class="u-fixed u-top-0 u-left-0 u-right-0 u-bottom-0 u-bg-black u-bg-opacity-50 u-flex u-justify-center u-items-center">
      <div class="u-bg-white u-p-6 u-rounded-lg u-w-4/5 u-max-w-4xl">
        <h2 class="u-text-xl u-font-bold u-mb-4">Gérer les environnements de l'organisation "{{ managingOrganization?.name }}"</h2>
        <OrganizationEnvironmentsManager :organizationId="managingOrganization?.id" />
        <button @click="closeEnvironmentManager" class="u-px-4 u-py-2 u-bg-gray-500 u-text-white u-rounded u-mt-4 u-hover:bg-gray-600">Fermer</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useOrganizationsStore } from '@/store/organization'
import { deleteorganization } from '@/api/organizations'
import type { OrganizationOut } from '@/api/types'
import { useNotificationStore } from '@/store/notifications'
import OrganizationForm from '@/components/business/Organizations/OrganizationForm.vue'
import OrganizationUsersManager from '@/components/business/Organizations/OrganizationUsersManager.vue'
import OrganizationGroupsManager from '@/components/business/Organizations/OrganizationGroupsManager.vue'
import OrganizationEnvironmentsManager from '@/components/business/Organizations/OrganizationEnvironmentsManager.vue'

const organizationsStore = useOrganizationsStore()
const notificationStore = useNotificationStore()

// State
const filterName = ref('')
const showForm = ref(false)
const editingOrganization = ref<OrganizationOut | null>(null)
const deletingOrganization = ref<OrganizationOut | null>(null)
const showUserManager = ref(false)
const showGroupManager = ref(false)
const showEnvironmentManager = ref(false)
const managingOrganization = ref<OrganizationOut | null>(null)

// Methods
const applyFilter = () => {
  organizationsStore.setFilter(filterName.value)
}

const toggleForm = () => {
  showForm.value = !showForm.value
  if (!showForm.value) {
    editingOrganization.value = null
  }
}

const onFormSuccess = () => {
  showForm.value = false
  editingOrganization.value = null
  organizationsStore.fetchOrganizations()
}

const editOrganization = (organization: OrganizationOut) => {
  editingOrganization.value = organization
  showForm.value = false
  deletingOrganization.value = null // Close delete confirmation if open
}

const cancelEdit = () => {
  editingOrganization.value = null
}

const deleteOrganizationAction = (organization: OrganizationOut) => {
  deletingOrganization.value = organization
  editingOrganization.value = null // Close edit form if open
}

const confirmDelete = async () => {
  if (!deletingOrganization.value) return

  try {
    await deleteorganization(deletingOrganization.value.id)
    organizationsStore.fetchOrganizations()
    deletingOrganization.value = null
  } catch (error) {
    console.error('Erreur lors de la suppression de l\'organisation:', error)
    notificationStore.addNotification({
      type: 'error',
      message: 'Erreur lors de la suppression de l\'organisation',
    })
  }
}

const cancelDelete = () => {
  deletingOrganization.value = null
}

const manageUsers = (organization: OrganizationOut) => {
  managingOrganization.value = organization
  showUserManager.value = true
}

const closeUserManager = () => {
  showUserManager.value = false
  managingOrganization.value = null
}

const manageGroups = (organization: OrganizationOut) => {
  managingOrganization.value = organization
  showGroupManager.value = true
}

const closeGroupManager = () => {
  showGroupManager.value = false
  managingOrganization.value = null
}

const manageEnvironments = (organization: OrganizationOut) => {
  managingOrganization.value = organization
  showEnvironmentManager.value = true
}

const closeEnvironmentManager = () => {
  showEnvironmentManager.value = false
  managingOrganization.value = null
}

const handleCommand = (command: string, organization: OrganizationOut) => {
  switch (command) {
    case 'edit':
      editOrganization(organization)
      break
    case 'delete':
      deleteOrganizationAction(organization)
      break
    case 'manage-users':
      manageUsers(organization)
      break
    case 'manage-groups':
      manageGroups(organization)
      break
    case 'manage-environments':
      manageEnvironments(organization)
      break
  }
}

const prevPage = () => {
  if (organizationsStore.currentPage > 1) {
    organizationsStore.setPage(organizationsStore.currentPage - 1)
  }
}

const nextPage = () => {
  if (organizationsStore.currentPage < organizationsStore.totalPages) {
    organizationsStore.setPage(organizationsStore.currentPage + 1)
  }
}

// Lifecycle
onMounted(() => {
  organizationsStore.fetchOrganizations()
})
</script>
