// src/store/users.ts
import { defineStore } from 'pinia'
import type { User } from '@/types' // Importation du type partagé
import { listusers } from '@/api'

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
        const response = await listusers()
        // Adaptation selon la structure du retour de l'API
        this.users = response.data.data || response.data
        this.total = response.data.total || response.data.length
      } catch (error) {
        throw error
      }
    },
    reset() {
      this.users = []
      this.total = 0
      this.currentPage = 1
      this.filters.email = ''
    },
  },
})
