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
  listAllGroups,
  getGroup,
  createGroup,
  updateGroup,
  deleteGroup,
  getGroupUsers,
  addUserToGroup,
  removeUserFromGroup,
  getGroupPolicies,
  addPolicyToGroup,
  removePolicyFromGroup,
  getGroupTags,
  addTagToGroup,
  removeTagFromGroup
} from '@/services/groupService'
import type { Group, GroupCreate, GroupUpdate, User, Policy, Tag } from '@/services/groupService'

/**
 * Composable pour la gestion des groupes
 * Fournit un état réactif et des méthodes pour la gestion complète des groupes
 */
export function useGroups() {
  // État réactif principal
  const groups = ref<Group[]>([])
  const currentGroup = ref<Group | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  // État pour les relations
  const groupUsers = ref<User[]>([])
  const groupPolicies = ref<Policy[]>([])
  const groupTags = ref<Tag[]>([])
  const loadingUsers = ref(false)
  const loadingPolicies = ref(false)
  const loadingTags = ref(false)

  // Computed properties
  const groupCount = computed(() => groups.value.length)
  const activeGroups = computed(() => groups.value.filter(group => group.name)) // Tous les groupes avec un nom
  const currentGroupId = computed(() => currentGroup.value?.id ?? null)

  /**
   * Récupère tous les groupes
   */
  const { execute: fetchGroups, isLoading: isFetching } = useAsyncState(
    async () => {
      const response = await listAllGroups()
      groups.value = response.data.data
      return response.data.data
    },
    [],
    { immediate: false }
  )

  /**
   * Récupère un groupe spécifique par ID
   */
  const fetchGroup = async (groupId: number) => {
    loading.value = true
    try {
      const response = await getGroup(groupId)
      currentGroup.value = response.data.data
      return response.data.data
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Erreur lors de la récupération du groupe'
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Crée un nouveau groupe
   */
  const createNewGroup = async (organizationId: number, groupData: GroupCreate) => {
    loading.value = true
    try {
      const response = await createGroup(organizationId, groupData)
      groups.value.push(response.data.data)
      return response.data.data
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Erreur lors de la création du groupe'
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Met à jour un groupe existant
   */
  const updateExistingGroup = async (groupId: number, groupData: GroupUpdate) => {
    loading.value = true
    try {
      const response = await updateGroup(groupId, groupData)
      const index = groups.value.findIndex(g => g.id === groupId)
      if (index !== -1) {
        groups.value[index] = response.data.data
      }
      if (currentGroup.value?.id === groupId) {
        currentGroup.value = response.data.data
      }
      return response.data.data
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Erreur lors de la mise à jour du groupe'
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Supprime un groupe
   */
  const deleteExistingGroup = async (groupId: number) => {
    loading.value = true
    try {
      await deleteGroup(groupId)
      groups.value = groups.value.filter(g => g.id !== groupId)
      if (currentGroup.value?.id === groupId) {
        currentGroup.value = null
      }
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Erreur lors de la suppression du groupe'
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Récupère les utilisateurs d'un groupe
   */
  const fetchGroupUsers = async (groupId: number) => {
    loadingUsers.value = true
    try {
      const response = await getGroupUsers(groupId)
      groupUsers.value = response.data.data
      return response.data.data
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Erreur lors de la récupération des utilisateurs'
      throw err
    } finally {
      loadingUsers.value = false
    }
  }

  /**
   * Ajoute un utilisateur à un groupe
   */
  const addUserToGroupAction = async (groupId: number, userId: number) => {
    loadingUsers.value = true
    try {
      await addUserToGroup(groupId, userId)
      // Rafraîchir la liste des utilisateurs
      await fetchGroupUsers(groupId)
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Erreur lors de l\'ajout de l\'utilisateur'
      throw err
    } finally {
      loadingUsers.value = false
    }
  }

  /**
   * Retire un utilisateur d'un groupe
   */
  const removeUserFromGroupAction = async (groupId: number, userId: number) => {
    loadingUsers.value = true
    try {
      await removeUserFromGroup(groupId, userId)
      groupUsers.value = groupUsers.value.filter(u => u.id !== userId)
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Erreur lors de la suppression de l\'utilisateur'
      throw err
    } finally {
      loadingUsers.value = false
    }
  }

  /**
   * Récupère les politiques d'un groupe
   */
  const fetchGroupPolicies = async (groupId: number) => {
    loadingPolicies.value = true
    try {
      const response = await getGroupPolicies(groupId)
      groupPolicies.value = response.data.data
      return response.data.data
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Erreur lors de la récupération des politiques'
      throw err
    } finally {
      loadingPolicies.value = false
    }
  }

  /**
   * Ajoute une politique à un groupe
   */
  const addPolicyToGroupAction = async (groupId: number, policyId: number) => {
    loadingPolicies.value = true
    try {
      await addPolicyToGroup(groupId, policyId)
      // Rafraîchir la liste des politiques
      await fetchGroupPolicies(groupId)
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Erreur lors de l\'ajout de la politique'
      throw err
    } finally {
      loadingPolicies.value = false
    }
  }

  /**
   * Retire une politique d'un groupe
   */
  const removePolicyFromGroupAction = async (groupId: number, policyId: number) => {
    loadingPolicies.value = true
    try {
      await removePolicyFromGroup(groupId, policyId)
      groupPolicies.value = groupPolicies.value.filter(p => p.id !== policyId)
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Erreur lors de la suppression de la politique'
      throw err
    } finally {
      loadingPolicies.value = false
    }
  }

  /**
   * Récupère les tags d'un groupe
   */
  const fetchGroupTags = async (groupId: number) => {
    loadingTags.value = true
    try {
      const response = await getGroupTags(groupId)
      groupTags.value = response.data.data
      return response.data.data
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Erreur lors de la récupération des tags'
      throw err
    } finally {
      loadingTags.value = false
    }
  }

  /**
   * Ajoute un tag à un groupe
   */
  const addTagToGroupAction = async (groupId: number, tagId: number) => {
    loadingTags.value = true
    try {
      await addTagToGroup(groupId, tagId)
      // Rafraîchir la liste des tags
      await fetchGroupTags(groupId)
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Erreur lors de l\'ajout du tag'
      throw err
    } finally {
      loadingTags.value = false
    }
  }

  /**
   * Retire un tag d'un groupe
   */
  const removeTagFromGroupAction = async (groupId: number, tagId: number) => {
    loadingTags.value = true
    try {
      await removeTagFromGroup(groupId, tagId)
      groupTags.value = groupTags.value.filter(t => t.id !== tagId)
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Erreur lors de la suppression du tag'
      throw err
    } finally {
      loadingTags.value = false
    }
  }

  /**
   * Efface les erreurs
   */
  const clearError = () => {
    error.value = null
  }

  /**
   * Réinitialise l'état du groupe courant
   */
  const clearCurrentGroup = () => {
    currentGroup.value = null
    groupUsers.value = []
    groupPolicies.value = []
    groupTags.value = []
  }

  return {
    // État principal (readonly pour éviter les modifications directes)
    groups: readonly(groups),
    currentGroup: readonly(currentGroup),
    loading: readonly(loading),
    error: readonly(error),
    isFetching,

    // État des relations
    groupUsers: readonly(groupUsers),
    groupPolicies: readonly(groupPolicies),
    groupTags: readonly(groupTags),
    loadingUsers: readonly(loadingUsers),
    loadingPolicies: readonly(loadingPolicies),
    loadingTags: readonly(loadingTags),

    // Computed properties
    groupCount,
    activeGroups,
    currentGroupId,

    // Actions CRUD principales
    fetchGroups,
    fetchGroup,
    createNewGroup,
    updateExistingGroup,
    deleteExistingGroup,

    // Actions pour les utilisateurs
    fetchGroupUsers,
    addUserToGroupAction,
    removeUserFromGroupAction,

    // Actions pour les politiques
    fetchGroupPolicies,
    addPolicyToGroupAction,
    removePolicyFromGroupAction,

    // Actions pour les tags
    fetchGroupTags,
    addTagToGroupAction,
    removeTagFromGroupAction,

    // Utilitaires
    clearError,
    clearCurrentGroup
  }
}
