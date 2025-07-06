<!-- src/components/UserGroupsManager.vue -->
<template>
  <el-card class="u-mt-4">
    <div class="u-space-y-6">
      <div>
        <h2 class="u-text-lg u-font-semibold u-mb-4">Groupes assignés</h2>
        <div class="u-space-y-2">
          <el-card v-for="group in assignedGroups" :key="group.id" class="u-bg-gray-50" shadow="never">
            <div class="u-flex u-justify-between u-items-center">
              <span class="u-font-medium">{{ group.name }}</span>
              <el-button type="danger" size="small" @click="removeGroup(group.id)"> Retirer </el-button>
            </div>
          </el-card>
          <el-empty v-if="assignedGroups.length === 0" description="Aucun groupe assigné" :image-size="60" />
        </div>
      </div>

      <div>
        <h2 class="u-text-lg u-font-semibold u-mb-4">Ajouter un groupe</h2>
        <div class="u-flex u-gap-2">
          <el-select v-model="selectedGroupId" placeholder="Sélectionnez un groupe" class="u-flex-1">
            <el-option v-for="group in availableGroups" :key="group.id" :label="group.name" :value="group.id" />
          </el-select>
          <el-button type="primary" @click="assignGroup" :disabled="!selectedGroupId"> Ajouter </el-button>
        </div>
      </div>
    </div>
  </el-card>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { usergroups } from '@/api'
import { listorganizationgroups, listallgroups, assignuser, removeuser } from '@/api'
import { useNotificationStore } from '@/store/notifications'

interface Group {
  id: number
  name: string
  description?: string
}

interface Props {
  userId: number
  /**
   * Pour un admin d'environnement, passer l'ID de l'environnement.
   * Pour un superadmin, cette valeur peut être null afin de récupérer tous les groupes.
   */
  environmentId?: number | null
}

const props = withDefaults(defineProps<Props>(), {
  environmentId: null,
})

const assignedGroups = ref<Group[]>([])
const availableGroups = ref<Group[]>([])
const selectedGroupId = ref<number | ''>('')
const notificationStore = useNotificationStore()

// Charge les groupes assignés à l'utilisateur
const fetchAssignedGroups = async () => {
  try {
    const response = await usergroups(props.userId)
    assignedGroups.value = response.data
  } catch (error) {
    notificationStore.addNotification({
      type: 'error',
      message: 'Erreur lors du chargement des groupes assignés',
    })
  }
}

// Charge les groupes disponibles
const fetchAvailableGroups = async () => {
  try {
    if (props.environmentId !== null) {
      const response = await listorganizationgroups(props.environmentId!)
      availableGroups.value = response.data
    } else {
      const response = await listallgroups()
      availableGroups.value = response.data
    }
  } catch (error) {
    notificationStore.addNotification({
      type: 'error',
      message: 'Erreur lors du chargement des groupes disponibles',
    })
  }
}

// Affecte un groupe à l'utilisateur
const assignGroup = async () => {
  if (!selectedGroupId.value) return
  try {
    await assignuser(selectedGroupId.value as number, props.userId)
    notificationStore.addNotification({
      type: 'success',
      message: 'Groupe assigné avec succès',
    })
    selectedGroupId.value = ''
    await fetchAssignedGroups()
  } catch (error) {
    notificationStore.addNotification({
      type: 'error',
      message: "Erreur lors de l'assignation du groupe",
    })
  }
}

// Retire un groupe de l'utilisateur
const removeGroup = async (groupId: number) => {
  try {
    await removeuser(groupId, props.userId)
    notificationStore.addNotification({
      type: 'success',
      message: 'Groupe retiré avec succès',
    })
    await fetchAssignedGroups()
  } catch (error) {
    notificationStore.addNotification({
      type: 'error',
      message: 'Erreur lors du retrait du groupe',
    })
  }
}

onMounted(() => {
  fetchAssignedGroups()
  fetchAvailableGroups()
})
</script>
