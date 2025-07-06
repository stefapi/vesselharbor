// src/store/groups.ts
import { defineStore } from 'pinia'
import { listAllGroups, type Group } from '@/services/groupService'

export const useGroupsStore = defineStore('groups', {
  state: () => ({
    groups: [] as Group[],
    total: 0,
    currentPage: 1,
    perPage: 10,
    filters: {
      name: '',
    },
    loading: false,
  }),
  getters: {
    filteredGroups: (state) => {
      if (!state.filters.name) return state.groups
      return state.groups.filter(group =>
        group.name.toLowerCase().includes(state.filters.name.toLowerCase())
      )
    },
    paginatedGroups(state) {
      const filtered = this.filteredGroups
      const start = (state.currentPage - 1) * state.perPage
      const end = start + state.perPage
      return filtered.slice(start, end)
    },
    totalPages(state) {
      return Math.ceil(this.filteredGroups.length / state.perPage)
    }
  },
  actions: {
    async fetchGroups() {
      try {
        this.loading = true
        const response = await listAllGroups()
        this.groups = response.data.data
        this.total = response.data.data.length
      } catch (error) {
        throw error
      } finally {
        this.loading = false
      }
    },
    setFilter(name: string) {
      this.filters.name = name
      this.currentPage = 1 // Reset to first page when filtering
    },
    setPage(page: number) {
      this.currentPage = page
    },
    reset() {
      this.groups = []
      this.total = 0
      this.currentPage = 1
      this.filters.name = ''
      this.loading = false
    },
  },
})
