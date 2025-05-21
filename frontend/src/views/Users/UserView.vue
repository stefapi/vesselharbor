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
          <el-card class="u-mb-4">
            <template #header>
              <div class="u-flex u-items-center u-justify-between">
                <h2 class="u-text-lg u-font-bold">Informations utilisateur</h2>
              </div>
            </template>
            <div v-if="user">
              <el-descriptions :column="1" border>
                <el-descriptions-item label="ID">{{ user.id }}</el-descriptions-item>
                <el-descriptions-item label="Email">{{ user.email }}</el-descriptions-item>
                <el-descriptions-item label="Superadmin">
                  <el-tag :type="user.is_superadmin ? 'success' : 'info'">
                    {{ user.is_superadmin ? 'Oui' : 'Non' }}
                  </el-tag>
                </el-descriptions-item>
              </el-descriptions>
            </div>
            <div v-else class="u-text-center u-py-4">
              <el-skeleton :rows="3" animated />
            </div>
          </el-card>
        </el-col>

        <!-- Groupes de l'utilisateur -->
        <el-col :span="12">
          <el-card>
            <template #header>
              <div class="u-flex u-items-center u-justify-between">
                <h2 class="u-text-lg u-font-bold">Groupes</h2>
                <el-button type="primary" size="small" @click="showAddGroupDialog = true">
                  Ajouter un groupe
                </el-button>
              </div>
            </template>
            <div v-if="userGroups.length > 0">
              <el-table :data="userGroups" style="width: 100%">
                <el-table-column prop="name" label="Nom du groupe" />
                <el-table-column prop="environment_name" label="Environnement">
                  <template #default="{ row }">
                    {{ row.environment_name || 'Global' }}
                  </template>
                </el-table-column>
                <el-table-column label="Actions" width="100" align="center">
                  <template #default="{ row }">
                    <el-button
                      type="danger"
                      size="small"
                      icon
                      @click="removeGroupFromUser(row.id)"
                    >
                      <i-mdi-delete />
                    </el-button>
                  </template>
                </el-table-column>
              </el-table>
            </div>
            <div v-else class="u-text-center u-py-4">
              <p>Aucun groupe assigné à cet utilisateur.</p>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </el-main>

    <!-- Dialog pour ajouter un groupe -->
    <el-dialog
      v-model="showAddGroupDialog"
      title="Ajouter un groupe"
      width="500px"
    >
      <el-form>
        <el-form-item label="Groupe">
          <el-select v-model="selectedGroup" placeholder="Sélectionner un groupe" style="width: 100%">
            <el-option
              v-for="group in availableGroups"
              :key="group.id"
              :label="group.name + (group.environment_name ? ` (${group.environment_name})` : ' (Global)')"
              :value="group.id"
            />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showAddGroupDialog = false">Annuler</el-button>
          <el-button type="primary" @click="addGroupToUser" :disabled="!selectedGroup">
            Ajouter
          </el-button>
        </span>
      </template>
    </el-dialog>
  </el-container>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessageBox } from 'element-plus'
import { getUserGroups, getUser, addUserToGroup, removeUserFromGroup, listGroups } from '@/services/userService'
import { useNotificationStore } from '@/store/notifications'

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
