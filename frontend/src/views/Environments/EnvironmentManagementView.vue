<!-- src/views/Environments/EnvironmentManagementView.vue -->
<template>
  <div>
    <h1>Gestion de l'Environnement : {{ environment.name }}</h1>
    
    <!-- Section Modification de l'environnement -->
    <section>
      <h2>Modifier l'environnement</h2>
      <form @submit.prevent="updateEnv">
        <div>
          <label for="envName">Nom de l'environnement</label>
          <input type="text" id="envName" v-model="envName" />
        </div>
        <button type="submit">Mettre à jour</button>
      </form>
      <button @click="deleteEnv" class="delete-btn">Supprimer l'environnement</button>
    </section>
    
    <hr />

    <!-- Section Gestion des éléments -->
    <section>
      <h2>Gestion des éléments</h2>
      <button @click="toggleElementForm">{{ showElementForm ? 'Annuler' : 'Créer un élément' }}</button>
      <div v-if="showElementForm">
        <form @submit.prevent="createElement">
          <div>
            <label for="elemName">Nom de l'élément</label>
            <input type="text" id="elemName" v-model="newElement.name" />
          </div>
          <div>
            <label for="elemDesc">Description</label>
            <input type="text" id="elemDesc" v-model="newElement.description" />
          </div>
          <button type="submit">Créer l'élément</button>
        </form>
      </div>
      <h3>Liste des éléments</h3>
      <ul>
        <li v-for="element in elements" :key="element.id">
          {{ element.name }} - {{ element.description }}
          <button @click="deleteElement(element.id)">Supprimer</button>
        </li>
      </ul>
    </section>
    
    <hr />

    <!-- Section Gestion des utilisateurs -->
    <section>
      <h2>Utilisateurs de l'environnement</h2>
      <ul>
        <li v-for="user in users" :key="user.id">
          {{ user.email }} - {{ user.role }} 
          <button @click="editUserRights(user)">Modifier droits</button>
        </li>
      </ul>
    </section>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { getEnvironment, updateEnvironment, deleteEnvironment } from '@/services/environmentService';
import { listElements, createElement as createElementService, deleteElement as deleteElementService } from '@/services/elementService';
import { listEnvironmentUsers, updateUserEnvironmentRights } from '@/services/environmentUserService'; // Hypothétique
export default defineComponent({
  name: 'EnvironmentManagementView',
  setup() {
    const route = useRoute();
    const router = useRouter();
    const envId = Number(route.params.envId);
    const environment = ref({ name: '' });
    const envName = ref('');
    
    // Gestion des éléments
    const elements = ref([] as any[]);
    const showElementForm = ref(false);
    const newElement = ref({ name: '', description: '' });
    
    // Gestion des utilisateurs de l'environnement
    const users = ref([] as any[]);
    
    const fetchEnvironment = async () => {
      try {
        const response = await getEnvironment(envId);
        environment.value = response.data.data;
        envName.value = environment.value.name;
      } catch (error) {
        console.error("Erreur lors de la récupération de l'environnement", error);
      }
    };

    const updateEnv = async () => {
      try {
        await updateEnvironment(envId, { name: envName.value });
        await fetchEnvironment();
        alert("Environnement mis à jour");
      } catch (error) {
        console.error("Erreur lors de la mise à jour", error);
      }
    };

    const deleteEnv = async () => {
      try {
        await deleteEnvironment(envId);
        alert("Environnement supprimé");
        router.push({ name: 'Dashboard' });
      } catch (error) {
        console.error("Erreur lors de la suppression", error);
      }
    };

    const fetchElements = async () => {
      try {
        const response = await listElements(envId, {});
        elements.value = response.data.data;
      } catch (error) {
        console.error("Erreur lors de la récupération des éléments", error);
      }
    };

    const toggleElementForm = () => {
      showElementForm.value = !showElementForm.value;
    };

    const createElement = async () => {
      try {
        await createElementService(envId, newElement.value);
        newElement.value = { name: '', description: '' };
        showElementForm.value = false;
        fetchElements();
      } catch (error) {
        console.error("Erreur lors de la création de l'élément", error);
      }
    };

    const deleteElement = async (elementId: number) => {
      try {
        await deleteElementService(elementId);
        fetchElements();
      } catch (error) {
        console.error("Erreur lors de la suppression de l'élément", error);
      }
    };

    const fetchUsers = async () => {
      try {
        // Supposons l'existence d'un endpoint pour lister les utilisateurs d'un environnement
        const response = await listEnvironmentUsers(envId, {});
        users.value = response.data.data;
      } catch (error) {
        console.error("Erreur lors de la récupération des utilisateurs", error);
      }
    };

    const editUserRights = (user: any) => {
      // Ici, on pourrait ouvrir une modal ou rediriger vers une page dédiée pour modifier les droits de l'utilisateur
      alert("Fonction de modification des droits non implémentée");
    };

    onMounted(() => {
      fetchEnvironment();
      fetchElements();
      fetchUsers();
    });

    return {
      environment,
      envName,
      updateEnv,
      deleteEnv,
      elements,
      showElementForm,
      toggleElementForm,
      newElement,
      createElement,
      deleteElement,
      users,
      editUserRights,
    };
  },
});
</script>

<style scoped>
/* Styles basiques pour la gestion de l'environnement */
section {
  margin-bottom: 2rem;
}
</style>

