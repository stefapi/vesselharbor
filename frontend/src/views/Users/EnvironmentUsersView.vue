<!-- src/views/Users/EnvironmentUsersView.vue -->
<template>
  <div>
    <h1>Utilisateurs de l'Environnement {{ environmentId }}</h1>
    <div>
      <input type="text" v-model="filterEmail" placeholder="Rechercher par email" @input="applyFilter" />
    </div>
    <button @click="toggleForm">{{ showForm ? 'Annuler' : 'Créer un utilisateur' }}</button>
    <div v-if="showForm && !editingUser">
      <UserForm mode="create" @success="onFormSuccess" />
    </div>
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Email</th>
          <th>Superadmin</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in usersStore.users" :key="user.id">
          <td>{{ user.id }}</td>
          <td>{{ user.email }}</td>
          <td>{{ user.is_superadmin ? 'Oui' : 'Non' }}</td>
          <td>
            <button @click="editUser(user)">Modifier</button>
            <button @click="deleteUser(user.id)">Supprimer</button>
            <button @click="manageGroups(user)">Gérer Groupes</button>
          </td>
        </tr>
      </tbody>
    </table>
    <div>
      <p>Total : {{ usersStore.total }}</p>
      <button :disabled="usersStore.currentPage === 1" @click="prevPage">Précédent</button>
      <span>Page {{ usersStore.currentPage }}</span>
      <button :disabled="usersStore.users.length < usersStore.perPage" @click="nextPage">Suivant</button>
    </div>
    <div v-if="editingUser">
      <h2>Modifier l'utilisateur</h2>
      <UserForm mode="edit" :initialData="editingUser" @success="onFormSuccess" />
      <button @click="cancelEdit">Annuler</button>
    </div>
    <!-- Modal pour la gestion des groupes -->
    <div v-if="showGroupManager" class="modal-overlay">
      <div class="modal">
        <h2>Gestion des Groupes pour {{ managingUser.email }}</h2>
        <!-- Ici, on passe l'ID de l'environnement pour filtrer les groupes -->
        <UserGroupsManager :userId="managingUser.id" :environmentId="environmentId" />
        <button @click="closeGroupManager">Fermer</button>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import { useRoute } from 'vue-router';
import UserForm from '@/components/UserForm.vue';
import { useUsersStore } from '@/store/users';
import { deleteUser as deleteUserService } from '@/services/userService';
import { useNotificationStore } from '@/store/notifications';
import UserGroupsManager from '@/components/UserGroupsManager.vue';

export default defineComponent({
  components: { UserForm, UserGroupsManager },
  setup() {
    const route = useRoute();
    const environmentId = Number(route.params.envId);
    const usersStore = useUsersStore();
    const notificationStore = useNotificationStore();
    const filterEmail = ref('');
    const showForm = ref(false);
    const editingUser = ref(null as any);
    const managingUser = ref(null as any);
    const showGroupManager = ref(false);

    const fetchUsers = async () => {
      await usersStore.fetchUsers();
      // Ici, vous pouvez filtrer par environnement si l’API le supporte
    };
    fetchUsers();
    const applyFilter = () => {
      usersStore.filters.email = filterEmail.value;
      usersStore.currentPage = 1;
      fetchUsers();
    };
    const prevPage = () => {
      if (usersStore.currentPage > 1) {
        usersStore.currentPage--;
        fetchUsers();
      }
    };
    const nextPage = () => {
      usersStore.currentPage++;
      fetchUsers();
    };
    const deleteUser = async (userId: number) => {
      try {
        await deleteUserService(userId);
        notificationStore.addNotification({ type: 'success', message: "Utilisateur supprimé avec succès" });
        fetchUsers();
      } catch (error) {
        notificationStore.addNotification({ type: 'error', message: "Erreur lors de la suppression de l'utilisateur" });
      }
    };
    const editUser = (user: any) => {
      editingUser.value = user;
    };
    const cancelEdit = () => {
      editingUser.value = null;
    };
    const onFormSuccess = () => {
      editingUser.value = null;
      showForm.value = false;
      fetchUsers();
    };
    const toggleForm = () => {
      showForm.value = !showForm.value;
    };
    const manageGroups = (user: any) => {
      managingUser.value = user;
      showGroupManager.value = true;
    };
    const closeGroupManager = () => {
      showGroupManager.value = false;
    };

    return {
      environmentId,
      usersStore,
      filterEmail,
      showForm,
      editingUser,
      applyFilter,
      prevPage,
      nextPage,
      deleteUser,
      editUser,
      cancelEdit,
      onFormSuccess,
      toggleForm,
      manageGroups,
      managingUser,
      showGroupManager,
      closeGroupManager,
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
th, td {
  border: 1px solid #ccc;
  padding: 0.5rem;
}
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
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

