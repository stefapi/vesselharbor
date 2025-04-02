<!-- src/views/Users/UsersView.vue -->
<template>
  <div>
    <h1>Gestion Globale des Utilisateurs</h1>

    <!-- Filtre par email -->
    <div>
      <input type="text" v-model="filterEmail" placeholder="Rechercher par email" @input="applyFilter" />
    </div>

    <!-- Bouton pour afficher/masquer le formulaire de création -->
    <button @click="toggleForm">{{ showForm ? 'Annuler' : 'Créer un utilisateur' }}</button>

    <!-- Formulaire de création -->
    <div v-if="showForm && !editingUser">
      <UserForm mode="create" @success="onFormSuccess" />
    </div>

    <!-- Tableau listant les utilisateurs -->
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

    <!-- Pagination -->
    <div>
      <p>Total : {{ usersStore.total }}</p>
      <button :disabled="usersStore.currentPage === 1" @click="prevPage">Précédent</button>
      <span>Page {{ usersStore.currentPage }}</span>
      <button :disabled="usersStore.users.length < usersStore.perPage" @click="nextPage">Suivant</button>
    </div>

    <!-- Formulaire d'édition -->
    <div v-if="editingUser">
      <h2>Modifier l'utilisateur</h2>
      <UserForm mode="edit" :initialData="editingUser" @success="onFormSuccess" />
      <button @click="cancelEdit">Annuler</button>
    </div>

    <!-- Modal pour la gestion des groupes assignés à un utilisateur -->
    <div v-if="showGroupManager" class="modal-overlay">
      <div class="modal">
        <h2>Gestion des Groupes pour {{ managingUser.email }}</h2>
        <!-- Pour superadmin, on passe environmentId = null pour récupérer tous les groupes -->
        <UserGroupsManager :userId="managingUser.id" :environmentId="null" />
        <button @click="closeGroupManager">Fermer</button>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import UserForm from '@/components/UserForm.vue';
import { useUsersStore } from '@/store/users';
import { deleteUser as deleteUserService } from '@/services/userService';
import { useNotificationStore } from '@/store/notifications';
import UserGroupsManager from '@/components/UserGroupsManager.vue';

export default defineComponent({
  components: { UserForm, UserGroupsManager },
  setup() {
    const usersStore = useUsersStore();
    const notificationStore = useNotificationStore();
    const filterEmail = ref('');
    const showForm = ref(false);
    const editingUser = ref(null as any);
    const managingUser = ref(null as any);
    const showGroupManager = ref(false);

    // Chargement initial des utilisateurs
    const fetchUsers = async () => {
      await usersStore.fetchUsers();
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

