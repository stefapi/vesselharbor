// src/store/auth.ts
import { defineStore } from 'pinia'
import { logout as logoutService,login as loginService, refresh } from '@/services/authService.ts'
import { getUser } from '@/services/authService.ts'
import type { User } from '@/types/user.ts' // Importation du type partagé
import { useRouter } from 'vue-router'
import { clearAllOfflineData } from '@/services/clearOfflineData.ts'

interface Credentials {
  username: string
  password: string
}

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null as User | null,
    isAuthenticated: false,
    renewOngoing: false,
    isInitialized: false, // Flag d'initialisation
  }),
  getters: {
    // Renvoie la liste des environnements pour lesquels l'utilisateur a le rôle d'admin.
    // Si le groupe est global (environment_id === null), on considère que l'utilisateur est admin sur tous les environnements.
    environmentAdminIds: (state): number[] => {
      if (!state.user || !state.user.user_assignments) return []
      // On retourne uniquement les environnements définis dans les affectations spécifiques.
      const ids = state.user.user_assignments
        .filter((assignment) => assignment.group && assignment.group.functions && assignment.group.functions.some((func) => func.name === 'admin') && assignment.group.environment_id !== null)
        .map((assignment) => assignment.group.environment_id as number)
      // Si l'utilisateur possède une affectation avec un groupe global qui contient la fonction "admin", on peut retourner un flag spécial
      // ou bien considérer qu'il a accès à tous les environnements.
      return ids
    },
    // Vérifie si l'utilisateur est admin pour un environnement donné.
    isEnvironmentAdmin: (state) => {
      return (envId: number): boolean => {
        if (state.user?.is_superadmin) return true
        if (!state.user?.user_assignments) return false
        return state.user.user_assignments.some((assignment) => {
          const group = assignment.group
          if (!group || !group.functions) return false
          // Si le groupe est global (environment_id === null) ou s'il correspond à l'environnement demandé
          if (group.environment_id === null || group.environment_id === envId) {
            return group.functions.some((func) => func.name === 'admin')
          }
          return false
        })
      }
    },
  },
  actions: {
    // Méthode à appeler au démarrage de l'application pour recharger l'état
    async initialize() {
      try {
        await this.renewSession();
      } catch (error) {
        this.logout();
      }
      this.isInitialized = true;
    },

    async login(credentials: Credentials) {
      try {
        const response = await loginService(credentials)
        await this.renewSession()
      } catch (error) {
        this.logout()
        throw error
      }
    },

     async renewSession() {
      try {
        // On tente d'abord de rafraîchir le token avant de récupérer l'utilisateur
        await this.refreshTokenAction();
        const response = await getUser();
        this.user = response.data;
        this.isAuthenticated = true;
      } catch (error) {
        this.logout();
        throw error;
      }
    },

    async refreshTokenAction() {
      try {
        const response = await refresh();
      } catch (error) {
        this.logout();
        throw new Error('Échec du rafraîchissement du token');
      }
    },

    logout() {
      this.user = null
      this.isAuthenticated = false


      clearAllOfflineData()
      logoutService()
    },
  },
})
