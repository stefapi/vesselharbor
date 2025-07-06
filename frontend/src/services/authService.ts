// src/services/authService.ts
import type { AxiosError } from 'axios'
import { apiPost, apiGet } from './api'
import { authenticateauser } from '@/api/root'

export interface LoginCredentials {
  username: string
  password: string
}

export interface LoginResponseData {
  token_type: string
}

export interface UserProfileData {
  id: number
  email: string
  is_superadmin: boolean
  user_assignments?: any[]
  created_at?: string
  updated_at?: string
}

/**
 * Authentifie un utilisateur avec son email et mot de passe
 * Note: authenticateauser de api/root.ts ne peut pas être utilisé directement car:
 * - Il ne prend pas de paramètres pour les credentials
 * - Il manque l'import de l'objet 'api'
 * Utilise donc l'implémentation directe avec apiPost
 */
export async function login(credentials: LoginCredentials) {
  // TODO: Utiliser authenticateauser de api/root.ts quand il sera corrigé
  // pour accepter les credentials et avoir les imports nécessaires

  const formData = new FormData()
  formData.append('username', credentials.username)
  formData.append('password', credentials.password)

  return apiPost('/login', formData, {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
  })
}

/**
 * Déconnecte l'utilisateur
 */
export async function logout() {
  return apiPost('/logout')
}

/**
 * Rafraîchit le token d'accès à partir du refresh token stocké.
 */
export async function refresh() {
  try {
    return await apiPost('/refresh-token')
  } catch (error: unknown) {
    const axiosError = error as AxiosError
    // Si l'erreur est 400, on l'ignore silencieusement
    if (axiosError.response?.status === 400) {
      return null
    }
    // Sinon, on relance l'erreur
    throw error
  }
}

/**
 * Récupère le profil de l'utilisateur connecté
 */
export async function getCurrentUser() {
  return apiGet('/me')
}
