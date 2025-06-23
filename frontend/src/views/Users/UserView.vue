<template>
  <el-container>
    <!-- En-tête principal -->
    <el-header class="u-flex u-items-center u-justify-between u-py-4 u-border-b">
      <div class="u-flex u-items-center">
        <router-link to="/users" class="u-mr-4">
          <el-button icon>
            <i-mdi-arrow-left class="u-text-xl" />
          </el-button>
        </router-link>
        <h1 class="u-text-2xl u-font-bold">Détails de l'utilisateur</h1>
      </div>
    </el-header>

    <!-- Contenu principal -->
    <el-main class="u-p-4 u-bg-gray-50 dark:u-bg-gray-900">
      <el-row :gutter="20">
        <!-- Informations utilisateur -->
        <el-col :span="12">
          <UserInfoCard :user="user" />
        </el-col>

        <!-- Groupes de l'utilisateur -->
        <el-col :span="12">
          <UserGroupsCard
            :userGroups="userGroups"
            @showAddGroupDialog="showAddGroupDialog = true"
            @removeGroup="removeGroupFromUser"
          />
        </el-col>
      </el-row>
    </el-main>

    <!-- Dialog pour ajouter un groupe -->
    <AddGroupDialog
      v-model="showAddGroupDialog"
      :availableGroups="availableGroups"
      v-model:selectedGroup="selectedGroup"
      @addGroup="addGroupToUser"
    />
  </el-container>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessageBox } from 'element-plus'
import { getUserGroups, getUser, addUserToGroup, removeUserFromGroup, listGroups } from '@/services/userService'
import { useNotificationStore } from '@/store/notifications'
import UserInfoCard from '@/components/Users/UserInfoCard.vue'
import UserGroupsCard from '@/components/Users/UserGroupsCard.vue'
import AddGroupDialog from '@/components/Users/AddGroupDialog.vue'

const route = useRoute()
const router = useRouter()
const notificationStore = useNotificationStore()

// État local
const user = ref<any>(null)
const userGroups = ref<any[]>([])
const availableGroups = ref<any[]>([])
const showAddGroupDialog = ref(false)
const selectedGroup = ref<number | null>(null)

// Récupérer l'ID de l'utilisateur depuis les paramètres de route
const userId = Number(route.params.id)

// Charger les données de l'utilisateur
const fetchUserData = async () => {
  try {
    // Récupérer les détails de l'utilisateur
    const userResponse = await getUser(userId)
    user.value = userResponse.data

    // Récupérer les groupes de l'utilisateur
    const userGroupsResponse = await getUserGroups(userId)
    userGroups.value = userGroupsResponse.data.map((group: any) => ({
      id: group.id,
      name: group.name,
      environment_name: group.environment ? group.environment.name : null
    }))

    // Récupérer tous les groupes disponibles
    const groupsResponse = await listGroups()
    const allGroups = groupsResponse.data.map((group: any) => ({
      id: group.id,
      name: group.name,
      environment_name: group.environment ? group.environment.name : null
    }))

    // Filtrer pour ne garder que les groupes auxquels l'utilisateur n'appartient pas déjà
    availableGroups.value = allGroups.filter(
      group => !userGroups.value.some(ug => ug.id === group.id)
    )
  } catch (error) {
    notificationStore.addNotification({
      type: 'error',
      message: "Erreur lors du chargement des données de l'utilisateur"
    })
    router.push('/users')
  }
}

// Ajouter un groupe à l'utilisateur
const addGroupToUser = async () => {
  if (!selectedGroup.value) return

  try {
    // Appel API pour ajouter l'utilisateur au groupe
    await addUserToGroup(userId, selectedGroup.value)

    // Mettre à jour l'interface utilisateur
    const groupToAdd = availableGroups.value.find(g => g.id === selectedGroup.value)
    if (groupToAdd) {
      userGroups.value.push(groupToAdd)
      availableGroups.value = availableGroups.value.filter(g => g.id !== selectedGroup.value)
      notificationStore.addNotification({
        type: 'success',
        message: "Groupe ajouté avec succès"
      })
    }

    showAddGroupDialog.value = false
    selectedGroup.value = null
  } catch (error) {
    notificationStore.addNotification({
      type: 'error',
      message: "Erreur lors de l'ajout du groupe"
    })
  }
}

// Supprimer un groupe de l'utilisateur
const removeGroupFromUser = async (groupId: number) => {
  try {
    await ElMessageBox.confirm(
      'Êtes-vous sûr de vouloir retirer ce groupe de l\'utilisateur ?',
      'Confirmation',
      {
        confirmButtonText: 'Oui',
        cancelButtonText: 'Annuler',
        type: 'warning'
      }
    )

    // Appel API pour retirer l'utilisateur du groupe
    await removeUserFromGroup(userId, groupId)

    // Mettre à jour l'interface utilisateur
    const removedGroup = userGroups.value.find(g => g.id === groupId)
    userGroups.value = userGroups.value.filter(g => g.id !== groupId)

    if (removedGroup) {
      availableGroups.value.push(removedGroup)
    }

    notificationStore.addNotification({
      type: 'success',
      message: "Groupe retiré avec succès"
    })
  } catch (error) {
    // Si c'est une erreur de l'API et non une annulation de l'utilisateur
    if (error && error !== 'cancel') {
      notificationStore.addNotification({
        type: 'error',
        message: "Erreur lors du retrait du groupe"
      })
    }
    // Sinon, l'utilisateur a simplement annulé l'opération
  }
}

// Charger les données au montage du composant
onMounted(fetchUserData)
</script>
