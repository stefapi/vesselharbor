<!-- src/components/UserGroupsManager.vue -->
<template>
  <div class="user-groups-manager">
    <h2>Groupes assignés</h2>
    <ul>
      <li v-for="group in assignedGroups" :key="group.id">
        {{ group.name }}
        <button @click="removeGroup(group.id)">Retirer</button>
      </li>
    </ul>
    <h2>Ajouter un groupe</h2>
    <select v-model="selectedGroupId">
      <option value="" disabled>Sélectionnez un groupe</option>
      <option
        v-for="group in availableGroups"
        :key="group.id"
        :value="group.id"
      >
        {{ group.name }}
      </option>
    </select>
    <button @click="assignGroup" :disabled="!selectedGroupId">Ajouter</button>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue';
import { getUserGroups } from '@/services/userService';
import { listGroups, listAllGroups, assignUserToGroup, removeUserFromGroup } from '@/services/groupService';
import { useNotificationStore } from '@/store/notifications';

export default defineComponent({
  name: 'UserGroupsManager',
  props: {
    userId: {
      type: Number,
      required: true,
    },
    /**
     * Pour un admin d'environnement, passer l'ID de l'environnement.
     * Pour un superadmin, cette valeur peut être null afin de récupérer tous les groupes.
     */
    environmentId: {
      type: Number,
      default: null,
    },
  },
  setup(props) {
    const assignedGroups = ref([] as any[]);
    const availableGroups = ref([] as any[]);
    const selectedGroupId = ref<number | ''>('');
    const notificationStore = useNotificationStore();

    // Charge les groupes assignés à l'utilisateur
    const fetchAssignedGroups = async () => {
      try {
        const response = await getUserGroups(props.userId);
        assignedGroups.value = response.data.data;
      } catch (error) {
        notificationStore.addNotification({
          type: 'error',
          message: "Erreur lors du chargement des groupes assignés",
        });
      }
    };

    // Charge les groupes disponibles
    const fetchAvailableGroups = async () => {
      try {
        if (props.environmentId !== null) {
          const response = await listGroups(props.environmentId, {});
          availableGroups.value = response.data.data;
        } else {
          const response = await listAllGroups({});
          availableGroups.value = response.data.data;
        }
      } catch (error) {
        notificationStore.addNotification({
          type: 'error',
          message: "Erreur lors du chargement des groupes disponibles",
        });
      }
    };

    // Affecte un groupe à l'utilisateur
    const assignGroup = async () => {
      if (!selectedGroupId.value) return;
      try {
        await assignUserToGroup(selectedGroupId.value as number, props.userId);
        notificationStore.addNotification({
          type: 'success',
          message: "Groupe assigné avec succès",
        });
        await fetchAssignedGroups();
      } catch (error) {
        notificationStore.addNotification({
          type: 'error',
          message: "Erreur lors de l'assignation du groupe",
        });
      }
    };

    // Retire un groupe de l'utilisateur
    const removeGroup = async (groupId: number) => {
      try {
        await removeUserFromGroup(groupId, props.userId);
        notificationStore.addNotification({
          type: 'success',
          message: "Groupe retiré avec succès",
        });
        await fetchAssignedGroups();
      } catch (error) {
        notificationStore.addNotification({
          type: 'error',
          message: "Erreur lors du retrait du groupe",
        });
      }
    };

    onMounted(() => {
      fetchAssignedGroups();
      fetchAvailableGroups();
    });

    return {
      assignedGroups,
      availableGroups,
      selectedGroupId,
      assignGroup,
      removeGroup,
    };
  },
});
</script>

<style scoped>
.user-groups-manager {
  border: 1px solid #ccc;
  padding: 1rem;
  margin-top: 1rem;
}
</style>

