// src/store/auth.ts
import { defineStore } from 'pinia';
import api from '@/services/api';

interface UserAssignment {
  group: {
    environment_id: number;
    functions: { name: string }[];
  };
}

export interface User {
  id: number;
  email: string;
  is_superadmin: boolean;
  user_assignments?: UserAssignment[];
  // Autres propriétés éventuelles…
}

interface Credentials {
  username: string;
  password: string;
}

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null as User | null,
    isAuthenticated: false,
  }),
  getters: {
    // Renvoie la liste des environnements pour lesquels l'utilisateur a le rôle d'admin
    environmentAdminIds: (state): number[] => {
      if (!state.user || !state.user.user_assignments) return [];
      return state.user.user_assignments
        .filter(assignment => assignment.group &&
          assignment.group.functions &&
          assignment.group.functions.some(func => func.name === 'admin'))
        .map(assignment => assignment.group.environment_id);
    },
    // Vérifie si l'utilisateur est admin pour un environnement donné
    isEnvironmentAdmin: (state) => {
      return (envId: number): boolean => {
        return state.user?.is_superadmin || state.user?.user_assignments?.some(assignment => {
          const group = assignment.group;
          return group &&
            group.environment_id === envId &&
            group.functions &&
            group.functions.some(func => func.name === 'admin');
        }) || false;
      };
    },
  },
  actions: {
    async login(credentials: Credentials) {
      try {
        const response = await api.post('/login', credentials);
        // Supposons que l'API renvoie un objet "user" dans response.data
        this.user = response.data.user;
        this.isAuthenticated = true;
      } catch (error) {
        throw error;
      }
    },
    logout() {
      // Optionnel: appel à un endpoint logout si nécessaire
      this.user = null;
      this.isAuthenticated = false;
    },
    async renewSession() {
      try {
        const response = await api.get('/renew-session');
        this.user = response.data.user;
        this.isAuthenticated = true;
      } catch (error) {
        this.logout();
      }
    },
  },
});

