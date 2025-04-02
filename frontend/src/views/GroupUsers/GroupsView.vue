<!-- src/views/GroupsUsers/GroupsView.vue -->
<template>
  <div>
    <h1>Gestion des Groupes</h1>
    <!-- Filtre de recherche -->
    <div>
      <input
        type="text"
        v-model="filterName"
        placeholder="Rechercher par nom"
        @input="applyFilter"
      />
    </div>

    <!-- Bouton pour afficher/masquer le formulaire de création -->
    <button @click="toggleForm">
      {{ showForm ? 'Annuler' : 'Créer un groupe' }}
    </button>

    <!-- Formulaire de création -->
    <div v-if="showForm && !editingGroup">
      <GroupForm :environmentId="environmentId" @success="onFormSuccess" />
    </div>

    <!-- Tableau listant les groupes -->
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Nom</th>
          <th>Description</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="group in groupsStore.groups" :key="group.id">
          <td>{{ group.id }}</td>
          <td>{{ group.name }}</td>
          <td>{{ group.description }}</td>
          <td>
            <button @click="editGroup(group)">Modifier</button>
            <button @click="deleteGroup(group.id)">Supprimer</button>
            <button @click="manageFunctions(group)">Gérer Fonctions</button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- Pagination -->
    <div>
      <p>Total : {{ groupsStore.total }}</p>
      <button :disabled="groupsStore.currentPage === 1" @click="prevPage">
        Précédent
      </button>
      <span>Page {{ groupsStore.currentPage }}</span>
      <button
        :disabled="groupsStore.groups.length < groupsStore.perPage"
        @click="nextPage"
      >
        Suivant
      </button>
    </div>

    <!-- Formulaire d'édition -->
    <div v-if="editingGroup">
      <h2>Modifier le groupe</h2>
      <GroupForm
        :environmentId="environmentId"
        :initialData="editingGroup"
        @success="onFormSuccess"
      />
      <button @click="cancelEdit">Annuler</button>
    </div>

    <!-- Modal pour la gestion des fonctions du groupe -->
    <div v-if="showFunctionManager" class="modal-overlay">
      <div class="modal">
        <h2>Gérer les fonctions du groupe "{{ managingGroup.name }}"</h2>
        <GroupFunctionsManager :groupId="managingGroup.id" />
        <button @click="closeFunctionManager">Fermer</button>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import GroupForm from '@/components/GroupForm.vue';
import { useGroupsStore } from '@/store/groups';
import { deleteGroup as deleteGroupService } from '@/services/groupService';
import { useNotificationStore } from '@/store/notifications';
import GroupFunctionsManager from '@/components/GroupFunctionsManager.vue';

export default defineComponent({
  name: 'GroupsView',
  components: { GroupForm, GroupFunctionsManager },
  setup() {
    // Pour cet exemple, l'ID de l'environnement est fixé à 1 (adaptable dynamiquement)
    const environmentId = 1;
    const groupsStore = useGroupsStore();
    const notificationStore = useNotificationStore();

    const filterName = ref('');
    const showForm = ref(false);
    const editingGroup = ref(null as any);
    const managingGroup = ref(null as any);
    const showFunctionManager = ref(false);

    const fetchGroups = async () => {
      await groupsStore.fetchGroups(environmentId);
    };

    // Chargement initial
    fetchGroups();

    const applyFilter = () => {
      groupsStore.filters.name = filterName.value;
      groupsStore.currentPage = 1;
      fetchGroups();
    };

    const prevPage = () => {
      if (groupsStore.currentPage > 1) {
        groupsStore.currentPage--;
        fetchGroups();
      }
    };

    const nextPage = () => {
      groupsStore.currentPage++;
      fetchGroups();
    };

    const deleteGroup = async (groupId: number) => {
      try {
        await deleteGroupService(groupId);
        notificationStore.addNotification({
          type: 'success',
          message: 'Groupe supprimé avec succès',
        });
        fetchGroups();
      } catch (error) {
        notificationStore.addNotification({
          type: 'error',
          message: 'Erreur lors de la suppression du groupe',
        });
      }
    };

    const editGroup = (group: any) => {
      editingGroup.value = group;
    };

    const cancelEdit = () => {
      editingGroup.value = null;
    };

    const onFormSuccess = () => {
      editingGroup.value = null;
      showForm.value = false;
      fetchGroups();
    };

    const toggleForm = () => {
      showForm.value = !showForm.value;
    };

    // Ouvre la modal de gestion des fonctions pour le groupe sélectionné
    const manageFunctions = (group: any) => {
      managingGroup.value = group;
      showFunctionManager.value = true;
    };

    const closeFunctionManager = () => {
      showFunctionManager.value = false;
    };

    return {
      environmentId,
      groupsStore,
      filterName,
      showForm,
      editingGroup,
      applyFilter,
      prevPage,
      nextPage,
      deleteGroup,
      editGroup,
      cancelEdit,
      onFormSuccess,
      toggleForm,
      manageFunctions,
      managingGroup,
      showFunctionManager,
      closeFunctionManager,
    };
  },
});
</script>

<style scoped>
table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
}
th,
td {
  border: 1px solid #ccc;
  padding: 0.5rem;
}
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}
.modal {
  background: #fff;
  padding: 1rem;
  border-radius: 8px;
  width: 80%;
  max-width: 600px;
}
</style>

