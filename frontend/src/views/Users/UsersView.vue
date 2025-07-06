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
      <users-table :users="usersStore.users" @edit="editUser" @delete="confirmDelete" @manage-groups="manageGroups" @toggle-superadmin="handleToggleSuperadmin" />

      <!-- Pagination custom -->
      <users-pagination :total="usersStore.total" :per-page="usersStore.perPage" :current-page="usersStore.currentPage" @page-change="handlePageChange" />

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

// Services & stores
import { deleteauser, modifysuperadminstatus } from '@/api'
import { useNotificationStore } from '@/store/notifications'
import { useUsersStore } from '@/store/users'
import { useAuthStore } from '@/store/auth'

// Stores et router
const usersStore = useUsersStore()
const notificationStore = useNotificationStore()
const router = useRouter()

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
  // Rediriger vers la vue détaillée de l'utilisateur
  router.push(`/users/${user.id}`)
}
const onFormSuccess = () => {
  closeDrawer()
  fetchUsers()
}

// Suppression avec boîte de confirmation
const confirmDelete = async (userId: number) => {
  // Importer le store d'authentification pour vérifier l'utilisateur courant
  const authStore = useAuthStore()

  // Empêcher la suppression de soi-même
  if (authStore.user && authStore.user.id === userId) {
    notificationStore.addNotification({
      type: 'warning',
      message: 'Vous ne pouvez pas supprimer votre propre compte',
    })
    return
  }

  // Trouver l'utilisateur à supprimer
  const userToDelete = usersStore.users.find((u) => u.id === userId)

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

    // Procéder à la suppression
    await deleteauser(userId)
    notificationStore.addNotification({
      type: 'success',
      message: 'Utilisateur supprimé avec succès',
    })
    fetchUsers()
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

    // Appel API
    await modifysuperadminstatus(user.id, { is_superadmin: isSuperadmin })

    // Notification de succès
    notificationStore.addNotification({
      type: 'success',
      message: `Statut superadmin mis à jour pour ${user.email}`,
    })

    // Rafraîchir la liste
    fetchUsers()
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
