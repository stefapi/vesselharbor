<template>
  <el-container>
    <!-- En-tête principal -->
    <el-header class="u-flex u-items-center u-justify-between u-py-4 u-border-b">
      <h1 class="u-text-2xl u-font-bold">Gestion Globale des Utilisateurs</h1>
    </el-header>

    <!-- Contenu principal -->
    <el-main class="u-p-4 u-bg-gray-50 dark:u-bg-gray-900">
      <!-- Barre de recherche + bouton de création -->
      <user-filters
        :filter-email="filterEmail"
        :is-form-open="showForm || editingUser"
        @filter="onFilterChange"
        @toggle-form="toggleForm"
      />

      <!-- Tableau -->
      <users-table
        :users="usersStore.users"
        @edit="editUser"
        @delete="confirmDelete"
        @manage-groups="manageGroups"
      />

      <!-- Pagination custom -->
      <users-pagination
        :total="usersStore.total"
        :per-page="usersStore.perPage"
        :current-page="usersStore.currentPage"
        @page-change="handlePageChange"
      />

      <!-- Drawer création / édition -->
      <user-form-drawer
        :visible="showForm || !!editingUser"
        :editing-user="editingUser"
        @close="closeDrawer"
        @success="onFormSuccess"
      />

      <!-- Dialog groupes -->
      <UserGroupsDialog
        :visible="showGroupManager"
        :user="managingUser"
        @close="closeGroupManager"
      />
    </el-main>
  </el-container>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ElMessageBox } from 'element-plus'

// Composants
import UserFilters from '@/components/Users/UserFilters.vue'
import UserFormDrawer from '@/components/Users/UserFormDrawer.vue'
import UserGroupsDialog from '@/components/Users/UserGroupsDialog.vue'
import UsersPagination from '@/components/Users/UsersPagination.vue'
import UsersTable from '@/components/Users/UsersTable.vue'

// Services & stores
import { deleteUser as deleteUserService } from '@/services/userService'
import { useNotificationStore } from '@/store/notifications'
import { useUsersStore } from '@/store/users'

// Stores
const usersStore = useUsersStore()
const notificationStore = useNotificationStore()

// State local
const filterEmail = ref('')
const showForm = ref(false)
const editingUser = ref<any>(null)
const managingUser = ref<any>(null)
const showGroupManager = ref(false)

// Fetch initial
const fetchUsers = async () => {
  await usersStore.fetchUsers()
}
fetchUsers()

// Gestion des filtres
const onFilterChange = (email: string) => {
  filterEmail.value = email
  usersStore.filters.email = email
  usersStore.currentPage = 1
  fetchUsers()
}

// Pagination
const handlePageChange = (page: number) => {
  usersStore.currentPage = page
  fetchUsers()
}

// Formulaire
const toggleForm = () => {
  showForm.value = !showForm.value
}
const closeDrawer = () => {
  showForm.value = false
  editingUser.value = null
}

// Édition
const editUser = (user: any) => {
  editingUser.value = user
  showForm.value = true
}
const onFormSuccess = () => {
  closeDrawer()
  fetchUsers()
}

// Suppression avec boîte de confirmation
const confirmDelete = async (userId: number) => {
  try {
    await ElMessageBox.confirm(
      'Êtes-vous sûr de vouloir supprimer cet utilisateur ?',
      'Confirmation',
      {
        confirmButtonText: 'Supprimer',
        cancelButtonText: 'Annuler',
        type: 'warning' as const // ✅ Correction ici : type explicite
      }
    )
    await deleteUserService(userId)
    notificationStore.addNotification({ type: 'success', message: 'Utilisateur supprimé avec succès' })
    fetchUsers()
  } catch {
    notificationStore.addNotification({ type: 'error', message: "Erreur lors de la suppression de l'utilisateur" })
  }
}

// Gestion des groupes
const manageGroups = (user: any) => {
  managingUser.value = user
  showGroupManager.value = true
}
const closeGroupManager = () => {
  showGroupManager.value = false
  managingUser.value = null
}
</script>
