<template>
  <el-container>
    <!-- En-tête principal -->
    <el-header class="u-flex u-items-center u-justify-between u-py-4 u-border-b">
      <h1 class="u-text-2xl u-font-bold">Gestion Globale des Utilisateurs</h1>
    </el-header>

    <!-- Contenu principal -->
    <el-main class="u-p-4 u-bg-gray-50 dark:u-bg-gray-900">
      <!-- Barre de recherche + bouton de création -->
      <user-filters :filter-email="filterEmail" :is-form-open="showForm || !!editingUser" @filter="onFilterChange" @toggle-form="toggleForm" />

      <!-- Tableau -->
      <users-table :users="users" @edit="editUser" @delete="confirmDelete" @manage-groups="manageGroups" @toggle-superadmin="handleToggleSuperadmin" />

      <!-- Pagination custom -->
      <users-pagination :total="total" :per-page="perPage" :current-page="currentPage" @page-change="handlePageChange" />

      <!-- Drawer création / édition -->
      <user-form-drawer :visible="showForm || !!editingUser" :editing-user="editingUser" @close="closeDrawer" @success="onFormSuccess" />

      <!-- Dialog groupes -->
      <UserGroupsDialog :visible="showGroupManager" :user="managingUser" @close="closeGroupManager" />
    </el-main>
  </el-container>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessageBox } from 'element-plus'

// Composants
import UserFilters from '@/components/business/Users/UserFilters.vue'
import UserFormDrawer from '@/components/business/Users/UserFormDrawer.vue'
import UserGroupsDialog from '@/components/business/Users/UserGroupsDialog.vue'
import UsersPagination from '@/components/business/Users/UsersPagination.vue'
import UsersTable from '@/components/business/Users/UsersTable.vue'

// Use new composables instead of direct store access
const {
  users,
  loading,
  error,
  fetchUsers,
  deleteUser,
  updateUser,
  total,
  currentPage,
  perPage
} = useUsers()

const { user: currentUser, isAuthenticated } = useAuth()
const { canDelete, canUpdate } = usePermissions()
const notificationStore = useNotificationStore()
const router = useRouter()

// State local
const filterEmail = ref('')
const showForm = ref(false)
const editingUser = ref<any>(null)
const managingUser = ref<any>(null)
const showGroupManager = ref(false)

// Fetch initial data
fetchUsers()

// Gestion des filtres
const onFilterChange = (email: string) => {
  filterEmail.value = email
  // Use composable's built-in filtering if available, otherwise fetch with filter
  fetchUsers({ email })
}

// Pagination
const handlePageChange = (page: number) => {
  fetchUsers({ page })
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
  // Rediriger vers la vue détaillée de l'utilisateur
  router.push(`/users/${user.id}`)
}
const onFormSuccess = () => {
  closeDrawer()
  fetchUsers()
}

// Suppression avec boîte de confirmation
const confirmDelete = async (userId: number) => {
  // Empêcher la suppression de soi-même
  if (currentUser.value && currentUser.value.id === userId) {
    notificationStore.addNotification({
      type: 'warning',
      message: 'Vous ne pouvez pas supprimer votre propre compte',
    })
    return
  }

  // Vérifier les permissions
  if (!canDelete('USER')) {
    notificationStore.addNotification({
      type: 'error',
      message: 'Vous n\'avez pas les permissions pour supprimer des utilisateurs',
    })
    return
  }

  // Trouver l'utilisateur à supprimer
  const userToDelete = users.value.find((u) => u.id === userId)

  if (!userToDelete) {
    notificationStore.addNotification({
      type: 'error',
      message: 'Utilisateur introuvable',
    })
    return
  }

  try {
    // Message de confirmation spécial pour les superadmins
    if (userToDelete.is_superadmin) {
      await ElMessageBox.confirm(
        'Attention ! Vous êtes sur le point de supprimer un utilisateur avec des droits Superadmin. ' +
          'Cette action est irréversible et peut avoir des conséquences importantes sur la sécurité du système. ' +
          'Êtes-vous absolument sûr de vouloir continuer ?',
        'Confirmation - Suppression Superadmin',
        {
          confirmButtonText: 'Supprimer définitivement',
          cancelButtonText: 'Annuler',
          type: 'error',
          distinguishCancelAndClose: true,
        }
      )
    } else {
      // Message standard pour les utilisateurs normaux
      await ElMessageBox.confirm('Êtes-vous sûr de vouloir supprimer cet utilisateur ?', 'Confirmation', {
        confirmButtonText: 'Supprimer',
        cancelButtonText: 'Annuler',
        type: 'warning' as const,
      })
    }

    // Procéder à la suppression avec le composable
    await deleteUser(userId)
    notificationStore.addNotification({
      type: 'success',
      message: 'Utilisateur supprimé avec succès',
    })
  } catch (error) {
    // Ne pas afficher d'erreur si l'utilisateur a simplement annulé l'opération
    if (error !== 'cancel' && error !== 'close') {
      notificationStore.addNotification({
        type: 'error',
        message: "Erreur lors de la suppression de l'utilisateur",
      })
    }
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

// Gestion du statut superadmin
const handleToggleSuperadmin = async (user: any, isSuperadmin: boolean) => {
  // Vérifier les permissions
  if (!canUpdate('USER')) {
    notificationStore.addNotification({
      type: 'error',
      message: 'Vous n\'avez pas les permissions pour modifier le statut des utilisateurs',
    })
    return
  }

  try {
    const action = isSuperadmin ? 'promouvoir' : 'rétrograder'
    const status = isSuperadmin ? 'superadmin' : 'utilisateur normal'

    // Confirmation avant modification
    await ElMessageBox.confirm(
      `Êtes-vous sûr de vouloir ${action} "${user.email}" en tant que ${status} ?`,
      'Confirmation de modification',
      {
        confirmButtonText: 'Confirmer',
        cancelButtonText: 'Annuler',
        type: 'warning',
      }
    )

    // Utiliser le composable pour la mise à jour
    await updateUser(user.id, { is_superadmin: isSuperadmin })

    // Notification de succès
    notificationStore.addNotification({
      type: 'success',
      message: `Statut superadmin mis à jour pour ${user.email}`,
    })
  } catch (error) {
    // Ne pas afficher d'erreur si l'utilisateur a simplement annulé l'opération
    if (error !== 'cancel' && error !== 'close') {
      notificationStore.addNotification({
        type: 'error',
        message: 'Erreur lors de la modification du statut superadmin',
      })
    }
  }
}
</script>
