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
import { useAuth } from '@/composables/api/useAuth'

/**
 * Interface pour une permission
 */
export interface Permission {
  id: string
  name: string
  description?: string
  resource: string
  action: string
}

/**
 * Interface pour un rôle
 */
export interface Role {
  id: string
  name: string
  description?: string
  permissions: Permission[]
}

/**
 * Interface pour les règles de permissions
 */
export interface PermissionRule {
  resource: string
  action: string
  condition?: (context: PermissionContext) => boolean
}

/**
 * Interface pour le contexte de permission
 */
export interface PermissionContext {
  user: any
  resource?: any
  organization?: any
  environment?: any
  [key: string]: any
}

/**
 * Types d'actions prédéfinies
 */
export const ACTIONS = {
  CREATE: 'create',
  READ: 'read',
  UPDATE: 'update',
  DELETE: 'delete',
  MANAGE: 'manage',
  EXECUTE: 'execute',
  APPROVE: 'approve'
} as const

/**
 * Types de ressources prédéfinies
 */
export const RESOURCES = {
  USER: 'user',
  GROUP: 'group',
  ORGANIZATION: 'organization',
  ENVIRONMENT: 'environment',
  APPLICATION: 'application',
  CONTAINER: 'container',
  NETWORK: 'network',
  STORAGE: 'storage',
  POLICY: 'policy',
  TAG: 'tag',
  AUDIT: 'audit',
  SYSTEM: 'system'
} as const

/**
 * Permissions prédéfinies pour les super admins
 */
const SUPER_ADMIN_PERMISSIONS = [
  `${RESOURCES.SYSTEM}:${ACTIONS.MANAGE}`,
  `${RESOURCES.USER}:${ACTIONS.MANAGE}`,
  `${RESOURCES.ORGANIZATION}:${ACTIONS.MANAGE}`,
  `${RESOURCES.ENVIRONMENT}:${ACTIONS.MANAGE}`,
  `${RESOURCES.APPLICATION}:${ACTIONS.MANAGE}`,
  `${RESOURCES.POLICY}:${ACTIONS.MANAGE}`,
  `${RESOURCES.AUDIT}:${ACTIONS.READ}`
]

/**
 * Composable pour la gestion des permissions
 * Fournit une logique centralisée pour la vérification des droits et la gestion des permissions
 */
export function usePermissions() {
  const { user, isAuthenticated, isSuperAdmin } = useAuth()

  // État réactif
  const userPermissions = ref<Permission[]>([])
  const userRoles = ref<Role[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  // Computed properties
  const hasAnyPermission = computed(() => {
    const permissions = Array.isArray(userPermissions.value) ? userPermissions.value : []
    return permissions.length > 0 || isSuperAdmin.value
  })
  const permissionsList = computed(() => {
    if (!Array.isArray(userPermissions.value)) {
      return []
    }
    return userPermissions.value.map(p => `${p.resource}:${p.action}`)
  })

  /**
   * Vérifie si l'utilisateur a une permission spécifique
   */
  const hasPermission = (permission: string, context?: PermissionContext): boolean => {
    if (!isAuthenticated.value) return false

    // Les super admins ont toutes les permissions
    if (isSuperAdmin.value) return true

    // Vérifier si la permission est dans la liste des permissions utilisateur
    const hasDirectPermission = permissionsList.value.includes(permission)
    if (hasDirectPermission) return true

    // Vérifier les permissions via les rôles
    const roles = Array.isArray(userRoles.value) ? userRoles.value : []
    const hasRolePermission = roles.some(role =>
      Array.isArray(role.permissions) ? role.permissions.some(p => `${p.resource}:${p.action}` === permission) : false
    )
    if (hasRolePermission) return true

    // TODO: Implémenter la vérification des règles conditionnelles
    // if (context) {
    //   return checkConditionalPermissions(permission, context)
    // }

    return false
  }

  /**
   * Vérifie si l'utilisateur a toutes les permissions spécifiées
   */
  const hasAllPermissions = (permissions: string[], context?: PermissionContext): boolean => {
    return permissions.every(permission => hasPermission(permission, context))
  }

  /**
   * Vérifie si l'utilisateur a au moins une des permissions spécifiées
   */
  const hasAnyOfPermissions = (permissions: string[], context?: PermissionContext): boolean => {
    return permissions.some(permission => hasPermission(permission, context))
  }

  /**
   * Vérifie si l'utilisateur peut effectuer une action sur une ressource
   */
  const canPerformAction = (resource: string, action: string, context?: PermissionContext): boolean => {
    const permission = `${resource}:${action}`
    return hasPermission(permission, context)
  }

  /**
   * Vérifie si l'utilisateur peut gérer (toutes actions) une ressource
   */
  const canManageResource = (resource: string, context?: PermissionContext): boolean => {
    return canPerformAction(resource, ACTIONS.MANAGE, context)
  }

  /**
   * Vérifie les permissions CRUD pour une ressource
   */
  const canCreate = (resource: string, context?: PermissionContext): boolean => {
    return canPerformAction(resource, ACTIONS.CREATE, context)
  }

  const canRead = (resource: string, context?: PermissionContext): boolean => {
    return canPerformAction(resource, ACTIONS.READ, context)
  }

  const canUpdate = (resource: string, context?: PermissionContext): boolean => {
    return canPerformAction(resource, ACTIONS.UPDATE, context)
  }

  const canDelete = (resource: string, context?: PermissionContext): boolean => {
    return canPerformAction(resource, ACTIONS.DELETE, context)
  }

  /**
   * Vérifie les permissions spécifiques aux ressources métier
   */
  const canManageUsers = (context?: PermissionContext): boolean => {
    return canManageResource(RESOURCES.USER, context) ||
           canPerformAction(RESOURCES.USER, ACTIONS.CREATE, context)
  }

  const canManageOrganizations = (context?: PermissionContext): boolean => {
    return canManageResource(RESOURCES.ORGANIZATION, context)
  }

  const canManageEnvironments = (context?: PermissionContext): boolean => {
    return canManageResource(RESOURCES.ENVIRONMENT, context)
  }

  const canViewAuditLogs = (context?: PermissionContext): boolean => {
    return canPerformAction(RESOURCES.AUDIT, ACTIONS.READ, context)
  }

  /**
   * Vérifie si l'utilisateur est propriétaire d'une ressource
   */
  const isResourceOwner = (resource: any, userIdField = 'user_id'): boolean => {
    if (!user.value || !resource) return false
    return resource[userIdField] === user.value.id
  }

  /**
   * Vérifie si l'utilisateur appartient à la même organisation qu'une ressource
   */
  const isSameOrganization = (resource: any, orgIdField = 'organization_id'): boolean => {
    if (!user.value || !resource) return false
    // TODO: Implémenter la logique de vérification d'organisation
    // return user.value.organization_id === resource[orgIdField]
    return true // Temporaire
  }

  /**
   * Filtre une liste d'éléments selon les permissions de lecture
   */
  const filterByReadPermission = <T>(items: T[], resourceType: string): T[] => {
    if (isSuperAdmin.value) return items

    return items.filter(item => {
      const context: PermissionContext = {
        user: user.value,
        resource: item
      }
      return canRead(resourceType, context)
    })
  }

  /**
   * Définit les permissions utilisateur (à appeler après connexion)
   */
  const setUserPermissions = (permissions: Permission[]) => {
    userPermissions.value = permissions
  }

  /**
   * Définit les rôles utilisateur (à appeler après connexion)
   */
  const setUserRoles = (roles: Role[]) => {
    userRoles.value = roles
  }

  /**
   * Efface les permissions et rôles (à appeler lors de la déconnexion)
   */
  const clearPermissions = () => {
    userPermissions.value = []
    userRoles.value = []
    error.value = null
  }

  /**
   * Récupère les permissions depuis l'API (à implémenter)
   */
  const fetchUserPermissions = async (): Promise<void> => {
    if (!isAuthenticated.value || !user.value) return

    loading.value = true
    try {
      // TODO: Implémenter l'appel API pour récupérer les permissions
      // const response = await getUserPermissions(user.value.id)
      // setUserPermissions(response.data.permissions)
      // setUserRoles(response.data.roles)

      // Pour l'instant, simuler des permissions basiques
      if (isSuperAdmin.value) {
        const superAdminPermissions: Permission[] = SUPER_ADMIN_PERMISSIONS.map(perm => {
          const [resource, action] = perm.split(':')
          return {
            id: perm,
            name: `${action} ${resource}`,
            resource,
            action
          }
        })
        setUserPermissions(superAdminPermissions)
      }
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Erreur lors de la récupération des permissions'
    } finally {
      loading.value = false
    }
  }

  /**
   * Utilitaire pour créer des permissions personnalisées
   */
  const createPermission = (resource: string, action: string, description?: string): string => {
    return `${resource}:${action}`
  }

  /**
   * Utilitaire pour parser une permission
   */
  const parsePermission = (permission: string): { resource: string; action: string } => {
    const [resource, action] = permission.split(':')
    return { resource, action }
  }

  return {
    // État (readonly pour éviter les modifications directes)
    userPermissions: readonly(userPermissions),
    userRoles: readonly(userRoles),
    loading: readonly(loading),
    error: readonly(error),

    // Computed properties
    hasAnyPermission,
    permissionsList,

    // Vérifications de permissions génériques
    hasPermission,
    hasAllPermissions,
    hasAnyOfPermissions,
    canPerformAction,
    canManageResource,

    // Vérifications CRUD
    canCreate,
    canRead,
    canUpdate,
    canDelete,

    // Vérifications spécifiques aux ressources
    canManageUsers,
    canManageOrganizations,
    canManageEnvironments,
    canViewAuditLogs,

    // Vérifications contextuelles
    isResourceOwner,
    isSameOrganization,

    // Utilitaires
    filterByReadPermission,
    setUserPermissions,
    setUserRoles,
    clearPermissions,
    fetchUserPermissions,
    createPermission,
    parsePermission,

    // Constantes
    ACTIONS,
    RESOURCES
  }
}
