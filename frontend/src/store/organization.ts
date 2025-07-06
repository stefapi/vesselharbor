/*
 * Copyright (c) 2025.  VesselHarbor
 *
 * ____   ____                          .__    ___ ___             ___.
 * \   \ /   /____   ______ ______ ____ |  |  /   |   \_____ ______\_ |__   ___________
 *  \   Y   // __ \ /  ___//  ___// __ \|  | /    ~    \__  \\_  __ \ __ \ /  _ \_  __ \
 *   \     /\  ___/ \___ \ \___ \\  ___/|  |_\    Y    // __ \|  | \/ \_\ (  <_> )  | \/
 *    \___/  \___  >____  >____  >\___  >____/\___|_  /(____  /__|  |___  /\____/|__|
 *               \/     \/     \/     \/            \/      \/          \/
 *
 *
 * MIT License
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 *
 */

// src/store/organization.ts
import { defineStore } from 'pinia'
import { listorganizations } from '@/api/organizations'
import type { OrganizationOut } from '@/api/types'

type Organization = OrganizationOut

export const useOrganizationsStore = defineStore('organizations', {
  state: () => ({
    organizations: [] as Organization[],
    total: 0,
    currentPage: 1,
    perPage: 10,
    filters: {
      name: '',
    },
    loading: false,
  }),
  getters: {
    filteredOrganizations: (state) => {
      if (!state.filters.name) return state.organizations
      return state.organizations.filter(organization =>
        organization.name.toLowerCase().includes(state.filters.name.toLowerCase())
      )
    },
    paginatedOrganizations(state) {
      const filtered = this.filteredOrganizations
      const start = (state.currentPage - 1) * state.perPage
      const end = start + state.perPage
      return filtered.slice(start, end)
    },
    totalPages(state) {
      return Math.ceil(this.filteredOrganizations.length / state.perPage)
    }
  },
  actions: {
    async fetchOrganizations() {
      try {
        this.loading = true
        const response = await listorganizations()
        this.organizations = response.data.data
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
      this.organizations = []
      this.total = 0
      this.currentPage = 1
      this.filters.name = ''
      this.loading = false
    },
  },
})
