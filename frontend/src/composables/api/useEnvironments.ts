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
  listenvironments,
  createanenvironment,
  environmentdetails,
  updateanenvironment,
  deleteanenvironment,
  listphysicalhostsofanenvironmentenvironments,
  generatearandomname,
  userslinkedtoanenvironment,
  listelementsofanenvironmentenvironments,
  listenvironmenttagsenvironments,
  addatagtoanenvironment,
  removeatagfromanenvironment,
  listnetworksofanenvironmentenvironments,
  listvirtualmachinesofanenvironmentenvironments,
  liststoragepoolsofanenvironmentenvironments,
  listvolumesofanenvironmentenvironments,
  listdomainsofanenvironmentenvironments,
  listcontainernodesofanenvironmentenvironments,
  listcontainerclustersofanenvironmentenvironments,
  liststacksofanenvironmentenvironments,
  listapplicationsofanenvironmentenvironments
} from '@/api/environments'
import type { EnvironmentCreate } from '@/api/types'

/**
 * Interface pour un environnement (basée sur les réponses API)
 */
export interface Environment {
  id: number
  name: string
  description?: string
  organization_id: number
  created_at: string
  updated_at: string
}

/**
 * Interface pour un utilisateur d'environnement
 */
export interface EnvironmentUser {
  id: number
  email: string
  first_name?: string
  last_name?: string
  is_active: boolean
}

/**
 * Interface pour les éléments d'environnement
 */
export interface EnvironmentElement {
  id: number
  name: string
  type: string
  description?: string
  status?: string
}

/**
 * Interface pour les hôtes physiques
 */
export interface PhysicalHost {
  id: number
  name: string
  ip_address?: string
  status?: string
}

/**
 * Composable pour la gestion des environnements
 * Fournit un état réactif et des méthodes pour la gestion complète des environnements
 */
export function useEnvironments() {
  // État réactif principal
  const environments = ref<Environment[]>([])
  const currentEnvironment = ref<Environment | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  // État pour les relations et éléments
  const environmentUsers = ref<EnvironmentUser[]>([])
  const environmentTags = ref<any[]>([])
  const environmentElements = ref<EnvironmentElement[]>([])
  const physicalHosts = ref<PhysicalHost[]>([])

  // État pour les différents types d'éléments
  const networks = ref<any[]>([])
  const virtualMachines = ref<any[]>([])
  const storagePools = ref<any[]>([])
  const volumes = ref<any[]>([])
  const domains = ref<any[]>([])
  const containerNodes = ref<any[]>([])
  const containerClusters = ref<any[]>([])
  const stacks = ref<any[]>([])
  const applications = ref<any[]>([])

  // États de chargement
  const loadingUsers = ref(false)
  const loadingTags = ref(false)
  const loadingElements = ref(false)
  const loadingHosts = ref(false)
  const loadingNetworks = ref(false)
  const loadingVMs = ref(false)
  const loadingStorage = ref(false)
  const loadingVolumes = ref(false)
  const loadingDomains = ref(false)
  const loadingContainers = ref(false)
  const loadingStacks = ref(false)
  const loadingApps = ref(false)

  // Computed properties
  const environmentCount = computed(() => environments.value.length)
  const currentEnvironmentId = computed(() => currentEnvironment.value?.id ?? null)
  const currentEnvironmentName = computed(() => currentEnvironment.value?.name ?? '')

  /**
   * Récupère tous les environnements accessibles à l'utilisateur
   */
  const { execute: fetchEnvironments, isLoading: isFetching } = useAsyncState(
    async () => {
      const response = await listenvironments()
      environments.value = response.data
      return response.data
    },
    [],
    { immediate: false }
  )

  /**
   * Récupère les détails d'un environnement spécifique
   */
  const fetchEnvironment = async (environmentId: number) => {
    loading.value = true
    try {
      const response = await environmentdetails(environmentId)
      currentEnvironment.value = response.data
      return response.data
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Erreur lors de la récupération de l\'environnement'
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Crée un nouvel environnement
   */
  const createNewEnvironment = async (environmentData: EnvironmentCreate) => {
    loading.value = true
    try {
      const response = await createanenvironment(environmentData)
      environments.value.push(response.data)
      return response.data
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Erreur lors de la création de l\'environnement'
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Met à jour un environnement existant
   */
  const updateExistingEnvironment = async (environmentId: number, environmentData: EnvironmentCreate) => {
    loading.value = true
    try {
      const response = await updateanenvironment(environmentId, environmentData)
      const index = environments.value.findIndex(env => env.id === environmentId)
      if (index !== -1) {
        environments.value[index] = response.data
      }
      if (currentEnvironment.value?.id === environmentId) {
        currentEnvironment.value = response.data
      }
      return response.data
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Erreur lors de la mise à jour de l\'environnement'
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Supprime un environnement
   */
  const deleteExistingEnvironment = async (environmentId: number) => {
    loading.value = true
    try {
      await deleteanenvironment(environmentId)
      environments.value = environments.value.filter(env => env.id !== environmentId)
      if (currentEnvironment.value?.id === environmentId) {
        currentEnvironment.value = null
      }
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Erreur lors de la suppression de l\'environnement'
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Génère un nom aléatoire pour un environnement
   */
  const generateRandomName = async () => {
    try {
      const response = await generatearandomname()
      return response.data
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Erreur lors de la génération du nom'
      throw err
    }
  }

  /**
   * Récupère les utilisateurs liés à un environnement
   */
  const fetchEnvironmentUsers = async (environmentId: number) => {
    loadingUsers.value = true
    try {
      const response = await userslinkedtoanenvironment(environmentId)
      environmentUsers.value = response.data
      return response.data
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Erreur lors de la récupération des utilisateurs'
      throw err
    } finally {
      loadingUsers.value = false
    }
  }

  /**
   * Récupère les tags d'un environnement
   */
  const fetchEnvironmentTags = async (environmentId: number) => {
    loadingTags.value = true
    try {
      const response = await listenvironmenttagsenvironments(environmentId)
      environmentTags.value = response.data
      return response.data
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Erreur lors de la récupération des tags'
      throw err
    } finally {
      loadingTags.value = false
    }
  }

  /**
   * Ajoute un tag à un environnement
   */
  const addTagToEnvironment = async (environmentId: number, tagId: number) => {
    loadingTags.value = true
    try {
      await addatagtoanenvironment(environmentId, tagId)
      // Rafraîchir la liste des tags
      await fetchEnvironmentTags(environmentId)
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Erreur lors de l\'ajout du tag'
      throw err
    } finally {
      loadingTags.value = false
    }
  }

  /**
   * Retire un tag d'un environnement
   */
  const removeTagFromEnvironment = async (environmentId: number, tagId: number) => {
    loadingTags.value = true
    try {
      await removeatagfromanenvironment(environmentId, tagId)
      environmentTags.value = environmentTags.value.filter(t => t.id !== tagId)
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Erreur lors de la suppression du tag'
      throw err
    } finally {
      loadingTags.value = false
    }
  }

  /**
   * Récupère tous les éléments d'un environnement
   */
  const fetchEnvironmentElements = async (environmentId: number) => {
    loadingElements.value = true
    try {
      const response = await listelementsofanenvironmentenvironments(environmentId)
      environmentElements.value = response.data
      return response.data
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Erreur lors de la récupération des éléments'
      throw err
    } finally {
      loadingElements.value = false
    }
  }

  /**
   * Récupère les hôtes physiques d'un environnement
   */
  const fetchPhysicalHosts = async (environmentId: number) => {
    loadingHosts.value = true
    try {
      const response = await listphysicalhostsofanenvironmentenvironments(environmentId)
      physicalHosts.value = response.data
      return response.data
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Erreur lors de la récupération des hôtes physiques'
      throw err
    } finally {
      loadingHosts.value = false
    }
  }

  /**
   * Récupère les réseaux d'un environnement
   */
  const fetchNetworks = async (environmentId: number) => {
    loadingNetworks.value = true
    try {
      const response = await listnetworksofanenvironmentenvironments(environmentId)
      networks.value = response.data
      return response.data
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Erreur lors de la récupération des réseaux'
      throw err
    } finally {
      loadingNetworks.value = false
    }
  }

  /**
   * Récupère les machines virtuelles d'un environnement
   */
  const fetchVirtualMachines = async (environmentId: number) => {
    loadingVMs.value = true
    try {
      const response = await listvirtualmachinesofanenvironmentenvironments(environmentId)
      virtualMachines.value = response.data
      return response.data
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Erreur lors de la récupération des VMs'
      throw err
    } finally {
      loadingVMs.value = false
    }
  }

  /**
   * Récupère les pools de stockage d'un environnement
   */
  const fetchStoragePools = async (environmentId: number) => {
    loadingStorage.value = true
    try {
      const response = await liststoragepoolsofanenvironmentenvironments(environmentId)
      storagePools.value = response.data
      return response.data
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Erreur lors de la récupération des pools de stockage'
      throw err
    } finally {
      loadingStorage.value = false
    }
  }

  /**
   * Récupère les applications d'un environnement
   */
  const fetchApplications = async (environmentId: number) => {
    loadingApps.value = true
    try {
      const response = await listapplicationsofanenvironmentenvironments(environmentId)
      applications.value = response.data
      return response.data
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Erreur lors de la récupération des applications'
      throw err
    } finally {
      loadingApps.value = false
    }
  }

  /**
   * Efface les erreurs
   */
  const clearError = () => {
    error.value = null
  }

  /**
   * Réinitialise l'état de l'environnement courant
   */
  const clearCurrentEnvironment = () => {
    currentEnvironment.value = null
    environmentUsers.value = []
    environmentTags.value = []
    environmentElements.value = []
    physicalHosts.value = []
    networks.value = []
    virtualMachines.value = []
    storagePools.value = []
    volumes.value = []
    domains.value = []
    containerNodes.value = []
    containerClusters.value = []
    stacks.value = []
    applications.value = []
  }

  return {
    // État principal (readonly pour éviter les modifications directes)
    environments: readonly(environments),
    currentEnvironment: readonly(currentEnvironment),
    loading: readonly(loading),
    error: readonly(error),
    isFetching,

    // État des relations et éléments
    environmentUsers: readonly(environmentUsers),
    environmentTags: readonly(environmentTags),
    environmentElements: readonly(environmentElements),
    physicalHosts: readonly(physicalHosts),
    networks: readonly(networks),
    virtualMachines: readonly(virtualMachines),
    storagePools: readonly(storagePools),
    volumes: readonly(volumes),
    domains: readonly(domains),
    containerNodes: readonly(containerNodes),
    containerClusters: readonly(containerClusters),
    stacks: readonly(stacks),
    applications: readonly(applications),

    // États de chargement
    loadingUsers: readonly(loadingUsers),
    loadingTags: readonly(loadingTags),
    loadingElements: readonly(loadingElements),
    loadingHosts: readonly(loadingHosts),
    loadingNetworks: readonly(loadingNetworks),
    loadingVMs: readonly(loadingVMs),
    loadingStorage: readonly(loadingStorage),
    loadingVolumes: readonly(loadingVolumes),
    loadingDomains: readonly(loadingDomains),
    loadingContainers: readonly(loadingContainers),
    loadingStacks: readonly(loadingStacks),
    loadingApps: readonly(loadingApps),

    // Computed properties
    environmentCount,
    currentEnvironmentId,
    currentEnvironmentName,

    // Actions CRUD principales
    fetchEnvironments,
    fetchEnvironment,
    createNewEnvironment,
    updateExistingEnvironment,
    deleteExistingEnvironment,
    generateRandomName,

    // Actions pour les utilisateurs et tags
    fetchEnvironmentUsers,
    fetchEnvironmentTags,
    addTagToEnvironment,
    removeTagFromEnvironment,

    // Actions pour les éléments et infrastructure
    fetchEnvironmentElements,
    fetchPhysicalHosts,
    fetchNetworks,
    fetchVirtualMachines,
    fetchStoragePools,
    fetchApplications,

    // Utilitaires
    clearError,
    clearCurrentEnvironment
  }
}
