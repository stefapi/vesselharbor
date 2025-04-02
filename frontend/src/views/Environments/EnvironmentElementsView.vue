<!-- src/views/Environments/EnvironmentElementsView.vue -->
<template>
  <div>
    <h1>Environnement : {{ environment.name }}</h1>
    <h2>Liste des éléments</h2>
    <div v-if="elements.length === 0">
      <p>Aucun élément disponible dans cet environnement.</p>
    </div>
    <ul v-else>
      <li v-for="element in elements" :key="element.id">
        {{ element.name }} - {{ element.description }}
      </li>
    </ul>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue';
import { getEnvironment } from '@/services/environmentService';
import { listElements } from '@/services/elementService'; // supposons que ce service existe
import { useRoute } from 'vue-router';

export default defineComponent({
  name: 'EnvironmentElementsView',
  setup() {
    const route = useRoute();
    const envId = Number(route.params.envId);
    const environment = ref({ name: '' });
    const elements = ref([] as any[]);
    
    const fetchEnvironment = async () => {
      try {
        const response = await getEnvironment(envId);
        environment.value = response.data.data;
      } catch (error) {
        console.error("Erreur lors de la récupération de l'environnement", error);
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

    onMounted(() => {
      fetchEnvironment();
      fetchElements();
    });

    return { environment, elements };
  },
});
</script>

