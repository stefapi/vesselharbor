// src/store/auth.ts
import { defineStore } from 'pinia'
import { login as loginService, refresh } from '@/services/authService.ts'
import { getUser } from '@/services/authService.ts'
import type { User } from '@/types/user.ts' // Importation du type partagé

interface Credentials {
  username: string
  password: string
}

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null as User | null,
    isAuthenticated: false,
    accessToken: localStorage.getItem('authToken') || '',
    refreshToken: localStorage.getItem('refreshToken') || '',
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
      if (this.accessToken) {
        console.log('Renewing session')
        try {
          await this.renewSession()
          console.log('Session renewed')
        } catch (error) {
          console.error('Error renewing session:', error)
          this.logout()
        }
      }
      this.isInitialized = true
    },

    async login(credentials: Credentials) {
      try {
        const response = await loginService(credentials)
        // Supposons que la réponse contient access_token et refresh_token
        this.accessToken = response.data.data.access_token
        this.refreshToken = response.data.data.refresh_token
        localStorage.setItem('authToken', response.data.data.access_token)
        localStorage.setItem('refreshToken', response.data.data.refresh_token)
        await this.renewSession()
      } catch (error) {
        this.logout()
        throw error
      }
    },

    async renewSession() {
      try {
        // Appel à l'endpoint '/me' pour récupérer les informations de l'utilisateur.
        // On passe le token d'accès dans l'en-tête Authorization.
        //const response = await api.get('/me', {
        //  headers: { Authorization: `Bearer ${this.accessToken}` },
        //});

        // Si le refreshToken est vide, on ne peut pas rafraîchir la session
        if (!this.refreshToken || this.refreshToken === 'undefined'|| this.renewOngoing) {
          this.logout()
          this.renewOngoing = false
          throw new Error('Session expired - No refresh token available')
        }
        this.renewOngoing = true
        const response = await getUser()
        this.user = response.data
        this.isAuthenticated = true
      } catch (error) {
        // En cas d'erreur, on essaie de rafraîchir le token.
        if (this.isAuthenticated) {
          await this.refreshTokenAction()
        }
        // Si l'échec persiste, on déconnecte l'utilisateur.
        if (!this.isAuthenticated) {
          this.logout()
          this.renewOngoing = false
          throw error
        }
      }
      this.renewOngoing = false
    },

    async refreshTokenAction() {
      try {
        // Appel à l'endpoint '/refresh-token' en fournissant le refresh token.
        const response = await refresh()
        this.accessToken = response.data.access_token
        localStorage.setItem('authToken', response.data.access_token)
      } catch (error) {
        this.logout()
        throw error
      }
    },

    logout() {
      localStorage.removeItem('authToken')
      localStorage.removeItem('refreshToken')
      this.user = null
      this.isAuthenticated = false
      this.accessToken = ''
      this.refreshToken = ''
    },
  },
})
