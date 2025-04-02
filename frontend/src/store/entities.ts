// src/store/entities.ts
import { defineStore } from 'pinia';
import api from '@/services/api.ts';

interface Environment {
  id: number;
  name: string;
  // Autres propriétés de l'environnement si nécessaire
}

export const useEnvironmentsStore = defineStore('environments', {
  state: () => ({
    environments: [] as Environment[],
    total: 0,
    currentPage: 1,
    perPage: 10,
    filters: {
      name: '',
    },
  }),
  actions: {
    async fetchEnvironments() {
      try {
        const params = {
          skip: (this.currentPage - 1) * this.perPage,
          limit: this.perPage,
          name: this.filters.name,
        };
        const response = await api.get('/environments', { params });
        // Adaptez la structure en fonction du retour de votre API
        this.environments = response.data.data;
        this.total = response.data.total;
      } catch (error) {
        throw error;
      }
    },
  },
});

