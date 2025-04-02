// src/store/users.ts
import { defineStore } from 'pinia';
import { listUsers } from '@/services/userService.ts';

export interface User {
  id: number;
  email: string;
  is_superadmin: boolean;
  // Vous pouvez ajouter d'autres propriétés selon le retour de l'API
}

export const useUsersStore = defineStore('users', {
  state: () => ({
    users: [] as User[],
    total: 0,
    currentPage: 1,
    perPage: 10,
    filters: {
      email: '',
    },
  }),
  actions: {
    async fetchUsers() {
      try {
        const params = {
          skip: (this.currentPage - 1) * this.perPage,
          limit: this.perPage,
          email: this.filters.email,
        };
        const response = await listUsers(params);
        // Adaptation selon la structure du retour de l'API
        this.users = response.data.data;
        this.total = response.data.total;
      } catch (error) {
        throw error;
      }
    },
    reset() {
      this.users = [];
      this.total = 0;
      this.currentPage = 1;
      this.filters.email = '';
    },
  },
});

