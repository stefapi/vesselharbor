<!-- src/views/Environments/EnvironmentsView.vue -->
<template>
  <div>
    <h1>Environnement : {{ environment.name }}</h1>

    <!-- Section de gestion de l'environnement accessible uniquement si l'utilisateur peut gérer -->
    <div v-if="canManage">
      <section>
        <h2>Modifier l'environnement</h2>
        <form @submit.prevent="updateEnv">
          <label for="envName">Nom de l'environnement</label>
          <input id="envName" type="text" v-model="envName" />
          <button type="submit">Mettre à jour</button>
        </form>
        <button @click="deleteEnv" class="delete-btn">Supprimer l'environnement</button>
      </section>
      <hr />
      <section>
        <h2>Gestion des éléments</h2>
        <button @click="toggleElementForm">
          {{ showElementForm ? 'Annuler' : 'Créer un élément' }}
        </button>
        <div v-if="showElementForm">
          <form @submit.prevent="createElement">
            <div>
              <label for="elemName">Nom de l'élément</label>
              <input id="elemName" type="text" v-model="newElement.name" />
            </div>
            <div>
              <label for="elemDesc">Description</label>
              <input id="elemDesc" type="text" v-model="newElement.description" />
            </div>
            <button type="submit">Créer l'élément</button>
          </form>
        </div>
      </section>
    </div>

    <!-- Section de consultation (accessible à tous) -->
    <section>
      <h2>Liste des éléments</h2>
      <div v-if="elements.length === 0">
        <p>Aucun élément disponible dans cet environnement.</p>
      </div>
      <ul v-else>
        <li v-for="element in elements" :key="element.id">
          {{ element.name }} - {{ element.description }}
          <!-- Si l'utilisateur peut gérer, on affiche le bouton de suppression -->
          <button v-if="canManage" @click="deleteElement(element.id)">Supprimer</button>
        </li>
      </ul>
    </section>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { getEnvironment, updateEnvironment, deleteEnvironment } from '@/services/environmentService';
import { listElements, createElement as createElementService, deleteElement as deleteElementService } from '@/services/elementService';
import { useAuthStore } from '@/store/auth';

export default defineComponent({
  name: 'EnvironmentsView',
  setup() {
    const route = useRoute();
    const router = useRouter();
    const authStore = useAuthStore();
    const envId = Number(route.params.envId);

    // Données de l'environnement
    const environment = ref({ name: '' });
    const envName = ref('');

    // Liste des éléments de l'environnement
    const elements = ref([] as any[]);
    const showElementForm = ref(false);
    const newElement = ref({ name: '', description: '' });

    // Détermine si l'utilisateur a le droit de gérer l'environnement
    const canManage = computed(() => {
      return authStore.user?.is_superadmin || authStore.isEnvironmentAdmin(envId);
    });

    // Récupère les informations de l'environnement
    const fetchEnvironment = async () => {
      try {
        const response = await getEnvironment(envId);
        environment.value = response.data.data;
        envName.value = environment.value.name;
      } catch (error) {
        console.error("Erreur lors de la récupération de l'environnement", error);
      }
    };

    // Récupère la liste des éléments
    const fetchElements = async () => {
      try {
        const response = await listElements(envId, {});
        elements.value = response.data.data;
      } catch (error) {
        console.error("Erreur lors de la récupération des éléments", error);
      }
    };

    // Met à jour le nom de l'environnement
    const updateEnv = async () => {
      try {
        await updateEnvironment(envId, { name: envName.value });
        await fetchEnvironment();
        alert("Environnement mis à jour");
      } catch (error) {
        console.error("Erreur lors de la mise à jour de l'environnement", error);
      }
    };

    // Supprime l'environnement et redirige vers le dashboard
    const deleteEnv = async () => {
      try {
        await deleteEnvironment(envId);
        alert("Environnement supprimé");
        router.push({ name: 'Dashboard' });
      } catch (error) {
        console.error("Erreur lors de la suppression de l'environnement", error);
      }
    };

    // Gestion des éléments
    const toggleElementForm = () => {
      showElementForm.value = !showElementForm.value;
    };

    const createElement = async () => {
      try {
        await createElementService(envId, newElement.value);
        newElement.value = { name: '', description: '' };
        showElementForm.value = false;
        await fetchElements();
      } catch (error) {
        console.error("Erreur lors de la création de l'élément", error);
      }
    };

    const deleteElement = async (elementId: number) => {
      try {
        await deleteElementService(elementId);
        await fetchElements();
      } catch (error) {
        console.error("Erreur lors de la suppression de l'élément", error);
      }
    };

    onMounted(() => {
      fetchEnvironment();
      fetchElements();
    });

    return {
      environment,
      envName,
      elements,
      showElementForm,
      newElement,
      updateEnv,
      deleteEnv,
      toggleElementForm,
      createElement,
      deleteElement,
      canManage,
    };
  },
});
</script>

<style scoped>
h1 {
  margin-bottom: 1rem;
}
section {
  margin-top: 1.5rem;
}
.delete-btn {
  background-color: #dc3545;
  color: #fff;
  border: none;
  padding: 0.5rem 1rem;
  cursor: pointer;
  margin-top: 0.5rem;
}
input {
  margin-right: 0.5rem;
  padding: 0.3rem;
}
button {
  margin-top: 0.5rem;
  padding: 0.4rem 0.8rem;
}
</style>

