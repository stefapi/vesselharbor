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

import { ref, computed, readonly } from 'vue'
import { useAsyncState } from '@vueuse/core'
import {
  listorganizations,
  createorganization,
  organizationdetails,
  updateorganization,
  deleteorganization,
  addusertoorganization,
  removeuserfromorganization,
  listorganizationtagsorganizations,
  listorganizationpoliciesorganizations,
  listorganizationgroupsorganizations,
  listorganizationenvironmentsorganizations,
  listorganizationusersorganizations,
  listorganizationelementsorganizations
} from '@/api/organizations'
import type { OrganizationCreate, OrganizationUpdate } from '@/api/types'

/**
 * Interface pour une organisation (basée sur les réponses API)
 */
export interface Organization {
  id: number
  name: string
  description?: string
  created_at: string
  updated_at: string
}

/**
 * Interface pour un utilisateur d'organisation
 */
export interface OrganizationUser {
  id: number
  email: string
  first_name?: string
  last_name?: string
  is_active: boolean
}

/**
 * Interface pour les éléments d'organisation
 */
export interface OrganizationElement {
  id: number
  name: string
  type: string
  description?: string
}

/**
 * Composable pour la gestion des organisations
 * Fournit un état réactif et des méthodes pour la gestion complète des organisations
 */
export function useOrganizations() {
  // État réactif principal
  const organizations = ref<Organization[]>([])
  const currentOrganization = ref<Organization | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  // État pour les relations
  const organizationUsers = ref<OrganizationUser[]>([])
  const organizationTags = ref<any[]>([])
  const organizationPolicies = ref<any[]>([])
  const organizationGroups = ref<any[]>([])
  const organizationEnvironments = ref<any[]>([])
  const organizationElements = ref<OrganizationElement[]>([])

  const loadingUsers = ref(false)
  const loadingTags = ref(false)
  const loadingPolicies = ref(false)
  const loadingGroups = ref(false)
  const loadingEnvironments = ref(false)
  const loadingElements = ref(false)

  // Computed properties
  const organizationCount = computed(() => organizations.value.length)
  const currentOrganizationId = computed(() => currentOrganization.value?.id ?? null)
  const currentOrganizationName = computed(() => currentOrganization.value?.name ?? '')

  /**
   * Récupère toutes les organisations accessibles à l'utilisateur
   */
  const { execute: fetchOrganizations, isLoading: isFetching } = useAsyncState(
    async () => {
      const response = await listorganizations()
      organizations.value = response.data
      return response.data
    },
    [],
    { immediate: false }
  )

  /**
   * Récupère les détails d'une organisation spécifique
   */
  const fetchOrganization = async (orgId: number) => {
    loading.value = true
    try {
      const response = await organizationdetails(orgId)
      currentOrganization.value = response.data
      return response.data
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Erreur lors de la récupération de l\'organisation'
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Crée une nouvelle organisation
   */
  const createNewOrganization = async (organizationData: OrganizationCreate) => {
    loading.value = true
    try {
      const response = await createorganization(organizationData)
      organizations.value.push(response.data)
      return response.data
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Erreur lors de la création de l\'organisation'
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Met à jour une organisation existante
   */
  const updateExistingOrganization = async (orgId: number, organizationData: OrganizationUpdate) => {
    loading.value = true
    try {
      const response = await updateorganization(orgId, organizationData)
      const index = organizations.value.findIndex(org => org.id === orgId)
      if (index !== -1) {
        organizations.value[index] = response.data
      }
      if (currentOrganization.value?.id === orgId) {
        currentOrganization.value = response.data
      }
      return response.data
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Erreur lors de la mise à jour de l\'organisation'
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Supprime une organisation
   */
  const deleteExistingOrganization = async (orgId: number) => {
    loading.value = true
    try {
      await deleteorganization(orgId)
      organizations.value = organizations.value.filter(org => org.id !== orgId)
      if (currentOrganization.value?.id === orgId) {
        currentOrganization.value = null
      }
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Erreur lors de la suppression de l\'organisation'
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Récupère les utilisateurs d'une organisation
   */
  const fetchOrganizationUsers = async (orgId: number) => {
    loadingUsers.value = true
    try {
      const response = await listorganizationusersorganizations(orgId)
      organizationUsers.value = response.data
      return response.data
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Erreur lors de la récupération des utilisateurs'
      throw err
    } finally {
      loadingUsers.value = false
    }
  }

  /**
   * Ajoute un utilisateur à une organisation
   */
  const addUserToOrganization = async (orgId: number, userId: number) => {
    loadingUsers.value = true
    try {
      await addusertoorganization(orgId, userId)
      // Rafraîchir la liste des utilisateurs
      await fetchOrganizationUsers(orgId)
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Erreur lors de l\'ajout de l\'utilisateur'
      throw err
    } finally {
      loadingUsers.value = false
    }
  }

  /**
   * Retire un utilisateur d'une organisation
   */
  const removeUserFromOrganization = async (orgId: number, userId: number) => {
    loadingUsers.value = true
    try {
      await removeuserfromorganization(orgId, userId)
      organizationUsers.value = organizationUsers.value.filter(u => u.id !== userId)
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Erreur lors de la suppression de l\'utilisateur'
      throw err
    } finally {
      loadingUsers.value = false
    }
  }

  /**
   * Récupère les tags d'une organisation
   */
  const fetchOrganizationTags = async (orgId: number) => {
    loadingTags.value = true
    try {
      const response = await listorganizationtagsorganizations(orgId)
      organizationTags.value = response.data
      return response.data
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Erreur lors de la récupération des tags'
      throw err
    } finally {
      loadingTags.value = false
    }
  }

  /**
   * Récupère les politiques d'une organisation
   */
  const fetchOrganizationPolicies = async (orgId: number) => {
    loadingPolicies.value = true
    try {
      const response = await listorganizationpoliciesorganizations(orgId)
      organizationPolicies.value = response.data
      return response.data
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Erreur lors de la récupération des politiques'
      throw err
    } finally {
      loadingPolicies.value = false
    }
  }

  /**
   * Récupère les groupes d'une organisation
   */
  const fetchOrganizationGroups = async (orgId: number) => {
    loadingGroups.value = true
    try {
      const response = await listorganizationgroupsorganizations(orgId)
      organizationGroups.value = response.data
      return response.data
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Erreur lors de la récupération des groupes'
      throw err
    } finally {
      loadingGroups.value = false
    }
  }

  /**
   * Récupère les environnements d'une organisation
   */
  const fetchOrganizationEnvironments = async (orgId: number) => {
    loadingEnvironments.value = true
    try {
      const response = await listorganizationenvironmentsorganizations(orgId)
      organizationEnvironments.value = response.data
      return response.data
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Erreur lors de la récupération des environnements'
      throw err
    } finally {
      loadingEnvironments.value = false
    }
  }

  /**
   * Récupère tous les éléments d'une organisation
   */
  const fetchOrganizationElements = async (orgId: number) => {
    loadingElements.value = true
    try {
      const response = await listorganizationelementsorganizations(orgId)
      organizationElements.value = response.data
      return response.data
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Erreur lors de la récupération des éléments'
      throw err
    } finally {
      loadingElements.value = false
    }
  }

  /**
   * Efface les erreurs
   */
  const clearError = () => {
    error.value = null
  }

  /**
   * Réinitialise l'état de l'organisation courante
   */
  const clearCurrentOrganization = () => {
    currentOrganization.value = null
    organizationUsers.value = []
    organizationTags.value = []
    organizationPolicies.value = []
    organizationGroups.value = []
    organizationEnvironments.value = []
    organizationElements.value = []
  }

  return {
    // État principal (readonly pour éviter les modifications directes)
    organizations: readonly(organizations),
    currentOrganization: readonly(currentOrganization),
    loading: readonly(loading),
    error: readonly(error),
    isFetching,

    // État des relations
    organizationUsers: readonly(organizationUsers),
    organizationTags: readonly(organizationTags),
    organizationPolicies: readonly(organizationPolicies),
    organizationGroups: readonly(organizationGroups),
    organizationEnvironments: readonly(organizationEnvironments),
    organizationElements: readonly(organizationElements),
    loadingUsers: readonly(loadingUsers),
    loadingTags: readonly(loadingTags),
    loadingPolicies: readonly(loadingPolicies),
    loadingGroups: readonly(loadingGroups),
    loadingEnvironments: readonly(loadingEnvironments),
    loadingElements: readonly(loadingElements),

    // Computed properties
    organizationCount,
    currentOrganizationId,
    currentOrganizationName,

    // Actions CRUD principales
    fetchOrganizations,
    fetchOrganization,
    createNewOrganization,
    updateExistingOrganization,
    deleteExistingOrganization,

    // Actions pour les utilisateurs
    fetchOrganizationUsers,
    addUserToOrganization,
    removeUserFromOrganization,

    // Actions pour les relations
    fetchOrganizationTags,
    fetchOrganizationPolicies,
    fetchOrganizationGroups,
    fetchOrganizationEnvironments,
    fetchOrganizationElements,

    // Utilitaires
    clearError,
    clearCurrentOrganization
  }
}
