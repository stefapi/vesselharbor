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
import { login as authLogin, logout as authLogout, refresh as authRefresh } from '@/services/authService'
import type { LoginCredentials, UserProfileData } from '@/services/authService'

/**
 * Composable pour la gestion de l'authentification
 * Fournit un état réactif et des méthodes pour l'authentification utilisateur
 */
export function useAuth() {
  // État réactif
  const user = ref<UserProfileData | null>(null)
  const isAuthenticated = ref(false)
  const loading = ref(false)
  const error = ref<string | null>(null)
  const token = ref<string | null>(null)

  // Computed properties
  const isSuperAdmin = computed(() => user.value?.is_superadmin ?? false)
  const userEmail = computed(() => user.value?.email ?? '')
  const userId = computed(() => user.value?.id ?? null)

  /**
   * Connecte un utilisateur avec ses identifiants
   */
  const login = async (credentials: LoginCredentials) => {
    loading.value = true
    error.value = null

    try {
      const response = await authLogin(credentials)

      if (response.data) {
        token.value = response.data.access_token
        isAuthenticated.value = true

        // Stocker le token dans localStorage pour la persistance
        if (response.data.access_token) {
          localStorage.setItem('auth_token', response.data.access_token)
        }

        // TODO: Récupérer le profil utilisateur après connexion
        // await fetchUserProfile()
      }

      return response.data
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Erreur lors de la connexion'
      isAuthenticated.value = false
      token.value = null
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Déconnecte l'utilisateur
   */
  const logout = async () => {
    loading.value = true

    try {
      await authLogout()
    } catch (err) {
      // On continue même si la déconnexion côté serveur échoue
      console.warn('Erreur lors de la déconnexion côté serveur:', err)
    } finally {
      // Nettoyer l'état local dans tous les cas
      user.value = null
      isAuthenticated.value = false
      token.value = null
      error.value = null
      localStorage.removeItem('auth_token')
      loading.value = false
    }
  }

  /**
   * Rafraîchit le token d'authentification
   */
  const { execute: refreshToken, isLoading: isRefreshing } = useAsyncState(
    async () => {
      const response = await authRefresh()
      if (response?.data?.access_token) {
        token.value = response.data.access_token
        localStorage.setItem('auth_token', response.data.access_token)
        isAuthenticated.value = true
      }
      return response
    },
    null,
    { immediate: false }
  )

  /**
   * Initialise l'état d'authentification depuis le localStorage
   */
  const initializeAuth = () => {
    const storedToken = localStorage.getItem('auth_token')
    if (storedToken) {
      token.value = storedToken
      isAuthenticated.value = true
      // TODO: Valider le token et récupérer le profil utilisateur
    }
  }

  /**
   * Vérifie si l'utilisateur a une permission spécifique
   */
  const hasPermission = (permission: string): boolean => {
    // TODO: Implémenter la logique de permissions
    // Pour l'instant, les super admins ont toutes les permissions
    return isSuperAdmin.value
  }

  /**
   * Efface les erreurs d'authentification
   */
  const clearError = () => {
    error.value = null
  }

  /**
   * Efface complètement l'état d'authentification
   */
  const clearAuth = () => {
    user.value = null
    isAuthenticated.value = false
    token.value = null
    error.value = null
    localStorage.removeItem('auth_token')
  }

  return {
    // État (readonly pour éviter les modifications directes)
    user: readonly(user),
    isAuthenticated: readonly(isAuthenticated),
    loading: readonly(loading),
    error: readonly(error),
    token: readonly(token),
    isRefreshing,

    // Computed properties
    isSuperAdmin,
    userEmail,
    userId,

    // Actions
    login,
    logout,
    refreshToken,
    initializeAuth,
    hasPermission,

    // Utilitaires
    clearError,
    clearAuth
  }
}
