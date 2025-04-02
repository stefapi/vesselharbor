// src/store/groups.ts
import { defineStore } from 'pinia';
import { listGroups } from '@/services/groupService.ts';

export interface Group {
  id: number;
  name: string;
  description: string;
  // Vous pouvez ajouter d'autres propriétés si nécessaire
}

export const useGroupsStore = defineStore('groups', {
  state: () => ({
    groups: [] as Group[],
    total: 0,
    currentPage: 1,
    perPage: 10,
    filters: {
      name: '',
    },
  }),
  actions: {
    async fetchGroups(environmentId: number) {
      try {
        const params = {
          skip: (this.currentPage - 1) * this.perPage,
          limit: this.perPage,
          name: this.filters.name,
        };
        const response = await listGroups(environmentId, params);
        this.groups = response.data.data;
        this.total = response.data.total;
      } catch (error) {
        throw error;
      }
    },
    reset() {
      this.groups = [];
      this.total = 0;
      this.currentPage = 1;
      this.filters.name = '';
    },
  },
});

