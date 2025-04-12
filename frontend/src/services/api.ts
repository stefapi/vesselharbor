// src/services/api.ts
import axios, {
  type AxiosError,
  type AxiosInstance,
  type AxiosRequestConfig,
  type InternalAxiosRequestConfig,
  type AxiosResponse,
  type AxiosRequestHeaders
} from 'axios';
import { useAuthStore } from '@/store/auth.ts';
import { useNotificationStore } from '@/store/notifications.ts';

// Déclaration des types étendus
declare module 'axios' {
  interface AxiosRequestConfig {
    _retry?: boolean;
  }
}

interface ApiError {
  message: string;
  status?: number;
  data?: unknown;
}

const api: AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  withCredentials: true,
  timeout: 5000,
  timeoutErrorMessage: 'La requête a pris trop de temps, veuillez réessayer',
  headers: {
    'Content-Type': 'application/json',
  },
});

let isRefreshing = false;
let failedRequests: (() => void)[] = [];

// Correction du typage de l'intercepteur de réponse
api.interceptors.response.use(
  (response: AxiosResponse) => response, // Conservation de la réponse Axios native
  async (error: AxiosError) => {
    const originalRequest = error.config as InternalAxiosRequestConfig & { _retry?: boolean };
    const authStore = useAuthStore();
    const notificationStore = useNotificationStore();

    // Gestion des erreurs réseau/timeout
    if (error.code === 'ECONNABORTED' || !error.response) {
      notificationStore.addNotification({
        type: 'error',
        message: error.message || 'Problème de connexion au serveur'
      });
      return Promise.reject(error);
    }

    if (error.response.status === 401 && !originalRequest?._retry) {
      if (isRefreshing) {
        return new Promise<AxiosResponse>((resolve) => {
          failedRequests.push(() => {
            resolve(api(originalRequest));
          });
        });
      }

      isRefreshing = true;
      originalRequest._retry = true;
      try {
        // Appel direct au refresh token
        await authStore.refreshTokenAction();

        isRefreshing = false;
        failedRequests.forEach(cb => cb());
        failedRequests = [];

        return api(originalRequest);
      } catch (refreshError) {
        authStore.logout();
        notificationStore.addNotification({
          type: 'error',
          message: 'Session expirée - Veuillez vous reconnecter'
        });
        return Promise.reject({
          message: 'Session expirée - Veuillez vous reconnecter',
          status: 401
        });
      }
    }

    // Gestion des erreurs standardisées
    const errorMessage = (error.response?.data as any)?.message
      || 'Erreur de communication avec le serveur';

    notificationStore.addNotification({
      type: 'error',
      message: errorMessage
    });

    return Promise.reject({
      message: errorMessage,
      status: error.response?.status,
      data: error.response?.data
    } as ApiError);
  }
);

export const isAxiosError = (error: unknown): error is AxiosError => {
  return typeof error === 'object'
    && error !== null
    && 'isAxiosError' in error
    && (error as AxiosError).isAxiosError;
};

// Helpers typés correctement
export const apiGet = <T>(url: string, config?: AxiosRequestConfig) =>
  api.get<T>(url, config);

export const apiPost = <T>(url: string, data?: unknown, config?: AxiosRequestConfig) =>
  api.post<T>(url, data, config);

export const apiPut = <T>(url: string, data?: unknown, config?: AxiosRequestConfig) =>
  api.put<T>(url, data, config);

export const apiDelete = <T>(url: string, config?: AxiosRequestConfig) =>
  api.delete<T>(url, config);

export default api;
export type { ApiError };
