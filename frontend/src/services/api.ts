import axios, { type AxiosError, type AxiosInstance, type AxiosRequestConfig, type InternalAxiosRequestConfig, type AxiosResponse } from 'axios'
import { useAuthStore } from '@/store/auth.ts'
import { useNotificationStore } from '@/store/notifications.ts'
import { getCachedResponse, setCachedResponse } from './useOfflineCache.ts'
import { queueOfflineAction } from './offlineQueue.ts'
import { useOfflineSyncStore } from '@/store/offlineSync.ts'
import { isOfflineSyncEnabled } from '@/utils/env.ts'

// Étend les options d'axios
declare module 'axios' {
  interface AxiosRequestConfig {
    _retry?: boolean
  }
}

interface ApiError {
  message: string
  status?: number
  data?: unknown
}

const api: AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  withCredentials: true,
  timeout: 5000,
  timeoutErrorMessage: 'La requête a pris trop de temps, veuillez réessayer',
  headers: {
    'Content-Type': 'application/json',
  },
})

let isRefreshing = false
let failedRequests: (() => void)[] = []

api.interceptors.response.use(
  async (response: AxiosResponse) => {
    if (isOfflineSyncEnabled && response.config.method === 'get' && response.config.url) {
      await setCachedResponse(response.config.url, response.data)
    }

    return response
  },

  async (error: AxiosError) => {
    const originalRequest = error.config as InternalAxiosRequestConfig & { _retry?: boolean }
    const authStore = useAuthStore()
    const notificationStore = useNotificationStore()
    const syncStore = useOfflineSyncStore()

    const isOfflineOrTimeout = error.code === 'ECONNABORTED' || !error.response

    if (isOfflineSyncEnabled && isOfflineOrTimeout) {
      // ✅ Fallback GET
      if (originalRequest?.method === 'get' && originalRequest?.url) {
        const cached = await getCachedResponse(originalRequest.url)
        if (cached) {
          notificationStore.addNotification({
            type: 'info',
            message: 'Contenu chargé depuis le cache offline',
          })

          return {
            data: cached,
            status: 200,
            statusText: 'OfflineCache',
            headers: {},
            config: originalRequest,
          }
        }
      }

      // ✅ File d’attente pour mutations
      if (['post', 'put', 'delete'].includes(originalRequest?.method || '') && originalRequest?.url) {
        const method = originalRequest.method as 'post' | 'put' | 'delete'
        const url = originalRequest.url
        const data = originalRequest.data ? JSON.parse(originalRequest.data) : undefined

        await queueOfflineAction({
          method,
          url,
          data,
          timestamp: Date.now(),
        })

        await syncStore.updatePendingCount()

        notificationStore.addNotification({
          type: 'info',
          message: 'Action enregistrée pour envoi ultérieur (offline)',
        })

        return {
          data: { queued: true },
          status: 202,
          statusText: 'OfflineQueued',
          headers: {},
          config: originalRequest,
        }
      }
    }

    // ✅ Gestion du refresh token
    if (error.response?.status === 401 && !originalRequest?._retry) {
      if (isRefreshing) {
        return new Promise<AxiosResponse>((resolve) => {
          failedRequests.push(() => resolve(api(originalRequest)))
        })
      }

      isRefreshing = true
      originalRequest._retry = true

      try {
        await authStore.refreshTokenAction()
        isRefreshing = false
        failedRequests.forEach((cb) => cb())
        failedRequests = []

        return api(originalRequest)
      } catch (refreshError) {
        authStore.logout()
        notificationStore.addNotification({
          type: 'error',
          message: 'Session expirée - Veuillez vous reconnecter',
        })

        return Promise.reject({
          message: 'Session expirée - Veuillez vous reconnecter',
          status: 401,
        })
      }
    }

    const errorMessage = (error.response?.data as any)?.message || 'Erreur de communication avec le serveur'

    if (error.response?.status != 400) {
      notificationStore.addNotification({
        type: 'error',
        message: errorMessage,
      })
    }

    return Promise.reject({
      message: errorMessage,
      status: error.response?.status,
      data: error.response?.data,
    } as ApiError)
  }
)

// ✅ Helpers
export const isAxiosError = (error: unknown): error is AxiosError => typeof error === 'object' && error !== null && 'isAxiosError' in error && (error as AxiosError).isAxiosError

// ✅ Méthodes typées
export const apiGet = <T>(url: string, config?: AxiosRequestConfig) => api.get<T>(url, config)
export const apiPost = <T>(url: string, data?: unknown, config?: AxiosRequestConfig) => api.post<T>(url, data, config)
export const apiPut = <T>(url: string, data?: unknown, config?: AxiosRequestConfig) => api.put<T>(url, data, config)
export const apiDelete = <T>(url: string, config?: AxiosRequestConfig) => api.delete<T>(url, config)

export default api
export type { ApiError }
