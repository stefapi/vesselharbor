// src/services/authService.ts
import type { AxiosError } from 'axios'

import { authenticateauser, logout as apiLogout, renewtoken } from '@/api/root'

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
 */
export async function login(credentials: LoginCredentials) {
  return authenticateauser({
    username: credentials.username,
    password: credentials.password,
  })
}

/**
 * Déconnecte l'utilisateur
 */
export async function logout() {
  return apiLogout()
}

/**
 * Rafraîchit le token d'accès à partir du refresh token stocké.
 */
export async function refresh() {
  try {
    return await renewtoken()
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
