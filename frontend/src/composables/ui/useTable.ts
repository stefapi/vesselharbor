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

import { ref, computed, readonly, watch } from 'vue'
import { useStorage } from '@vueuse/core'

/**
 * Interface pour la configuration de tri
 */
export interface SortConfig {
  field: string
  direction: 'asc' | 'desc'
}

/**
 * Interface pour la configuration de pagination
 */
export interface PaginationConfig {
  page: number
  pageSize: number
  total: number
}

/**
 * Interface pour les filtres
 */
export interface FilterConfig {
  [key: string]: any
}

/**
 * Interface pour la configuration de la table
 */
export interface TableConfig {
  persistKey?: string // Clé pour persister l'état dans localStorage
  defaultPageSize?: number
  defaultSort?: SortConfig
  enableSelection?: boolean
  enableMultiSelection?: boolean
}

/**
 * Composable pour la gestion des tables avec pagination, tri, filtres et sélection
 * Fournit une logique réutilisable pour standardiser les tables de données
 */
export function useTable<T = any>(config: TableConfig = {}) {
  const {
    persistKey,
    defaultPageSize = 10,
    defaultSort,
    enableSelection = false,
    enableMultiSelection = false
  } = config

  // État de pagination
  const pagination = ref<PaginationConfig>({
    page: 1,
    pageSize: defaultPageSize,
    total: 0
  })

  // État de tri
  const sort = ref<SortConfig | null>(defaultSort || null)

  // État des filtres
  const filters = ref<FilterConfig>({})

  // État de sélection
  const selectedItems = ref<T[]>([])
  const selectedItem = ref<T | null>(null)

  // Recherche globale
  const searchQuery = ref('')

  // Persistance de l'état si une clé est fournie
  const persistedState = persistKey ? useStorage(`table-${persistKey}`, {
    pageSize: defaultPageSize,
    sort: defaultSort,
    filters: {}
  }) : null

  // Initialiser depuis l'état persisté
  if (persistedState?.value) {
    pagination.value.pageSize = persistedState.value.pageSize
    sort.value = persistedState.value.sort
    filters.value = persistedState.value.filters
  }

  // Computed properties
  const currentPage = computed(() => pagination.value.page)
  const pageSize = computed(() => pagination.value.pageSize)
  const totalItems = computed(() => pagination.value.total)
  const totalPages = computed(() => Math.ceil(totalItems.value / pageSize.value))
  const hasSelection = computed(() => selectedItems.value.length > 0)
  const selectedCount = computed(() => selectedItems.value.length)
  const isAllSelected = computed(() =>
    selectedItems.value.length > 0 && selectedItems.value.length === totalItems.value
  )

  // Pagination
  const setPage = (page: number) => {
    if (page >= 1 && page <= totalPages.value) {
      pagination.value.page = page
    }
  }

  const nextPage = () => {
    if (pagination.value.page < totalPages.value) {
      pagination.value.page++
    }
  }

  const prevPage = () => {
    if (pagination.value.page > 1) {
      pagination.value.page--
    }
  }

  const setPageSize = (size: number) => {
    pagination.value.pageSize = size
    pagination.value.page = 1 // Reset à la première page

    // Persister le changement
    if (persistedState) {
      persistedState.value.pageSize = size
    }
  }

  const setTotal = (total: number) => {
    pagination.value.total = total
  }

  // Tri
  const setSortField = (field: string) => {
    if (sort.value?.field === field) {
      // Inverser la direction si c'est le même champ
      sort.value.direction = sort.value.direction === 'asc' ? 'desc' : 'asc'
    } else {
      // Nouveau champ, commencer par asc
      sort.value = { field, direction: 'asc' }
    }

    // Reset à la première page lors du changement de tri
    pagination.value.page = 1

    // Persister le changement
    if (persistedState) {
      persistedState.value.sort = sort.value
    }
  }

  const clearSort = () => {
    sort.value = null
    if (persistedState) {
      persistedState.value.sort = null
    }
  }

  // Filtres
  const setFilter = (key: string, value: any) => {
    if (value === null || value === undefined || value === '') {
      delete filters.value[key]
    } else {
      filters.value[key] = value
    }

    // Reset à la première page lors du changement de filtre
    pagination.value.page = 1

    // Persister le changement
    if (persistedState) {
      persistedState.value.filters = filters.value
    }
  }

  const clearFilter = (key: string) => {
    delete filters.value[key]
    if (persistedState) {
      persistedState.value.filters = filters.value
    }
  }

  const clearAllFilters = () => {
    filters.value = {}
    searchQuery.value = ''
    pagination.value.page = 1
    if (persistedState) {
      persistedState.value.filters = {}
    }
  }

  const setSearchQuery = (query: string) => {
    searchQuery.value = query
    pagination.value.page = 1 // Reset à la première page lors de la recherche
  }

  // Sélection
  const selectItem = (item: T) => {
    if (!enableSelection) return

    if (enableMultiSelection) {
      const index = selectedItems.value.findIndex(selected =>
        JSON.stringify(selected) === JSON.stringify(item)
      )

      if (index > -1) {
        selectedItems.value.splice(index, 1)
      } else {
        selectedItems.value.push(item)
      }
    } else {
      selectedItem.value = item
      selectedItems.value = [item]
    }
  }

  const selectAll = (items: T[]) => {
    if (!enableSelection || !enableMultiSelection) return
    selectedItems.value = [...items]
  }

  const clearSelection = () => {
    selectedItems.value = []
    selectedItem.value = null
  }

  const isItemSelected = (item: T): boolean => {
    return selectedItems.value.some(selected =>
      JSON.stringify(selected) === JSON.stringify(item)
    )
  }

  // Réinitialisation complète
  const resetTable = () => {
    pagination.value = {
      page: 1,
      pageSize: defaultPageSize,
      total: 0
    }
    sort.value = defaultSort || null
    filters.value = {}
    searchQuery.value = ''
    clearSelection()

    if (persistedState) {
      persistedState.value = {
        pageSize: defaultPageSize,
        sort: defaultSort,
        filters: {}
      }
    }
  }

  // Utilitaires pour construire les paramètres de requête
  const getQueryParams = () => {
    const params: Record<string, any> = {
      page: pagination.value.page,
      pageSize: pagination.value.pageSize
    }

    if (sort.value) {
      params.sortField = sort.value.field
      params.sortDirection = sort.value.direction
    }

    if (searchQuery.value) {
      params.search = searchQuery.value
    }

    // Ajouter les filtres
    Object.entries(filters.value).forEach(([key, value]) => {
      params[key] = value
    })

    return params
  }

  return {
    // État (readonly pour éviter les modifications directes)
    pagination: readonly(pagination),
    sort: readonly(sort),
    filters: readonly(filters),
    selectedItems: readonly(selectedItems),
    selectedItem: readonly(selectedItem),
    searchQuery: readonly(searchQuery),

    // Computed properties
    currentPage,
    pageSize,
    totalItems,
    totalPages,
    hasSelection,
    selectedCount,
    isAllSelected,

    // Actions de pagination
    setPage,
    nextPage,
    prevPage,
    setPageSize,
    setTotal,

    // Actions de tri
    setSortField,
    clearSort,

    // Actions de filtrage
    setFilter,
    clearFilter,
    clearAllFilters,
    setSearchQuery,

    // Actions de sélection
    selectItem,
    selectAll,
    clearSelection,
    isItemSelected,

    // Utilitaires
    resetTable,
    getQueryParams
  }
}
