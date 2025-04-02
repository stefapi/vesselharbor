// src/services/api.ts
import axios from 'axios';
import { useAuthStore } from '@/store/auth.ts';
import { useNotificationStore } from '@/store/notifications.ts';

// Configuration de base avec timeout
const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  withCredentials: true,
  timeout: 5000, // 5 secondes de timeout
  timeoutErrorMessage: 'La requête a pris trop de temps, veuillez réessayer',
});

// Intercepteur pour gérer les erreurs de manière centralisée
api.interceptors.response.use(
  (response) => response.data, // Retourne directement les données pour simplification
  async (error) => {
    const notificationStore = useNotificationStore();
    const authStore = useAuthStore();

    // Gestion des erreurs réseau/timeout
    if (error.code === 'ECONNABORTED' || !error.response) {
      notificationStore.addNotification({
        type: 'error',
        message: 'Serveur indisponible ou connexion lente'
      });
      return Promise.reject(error);
    }

    // Gestion des erreurs HTTP
    const { status, data } = error.response;

    if (status === 401) {
      try {
        await authStore.renewSession();
        return api.request(error.config); // Retry la requête originale
      } catch (renewError) {
        authStore.logout();
        notificationStore.addNotification({
          type: 'error',
          message: 'Session expirée, veuillez vous reconnecter'
        });
      }
    } else {
      const message = data?.detail || `Erreur serveur (${status})`;
      notificationStore.addNotification({ type: 'error', message });
    }

    return Promise.reject(error);
  }
);

// Fonction helper pour les requêtes courantes
export const apiGet = (url: string, params = {}) => api.get(url, { params });
export const apiPost = (url: string, data = {}) => api.post(url, data);
export const apiPut = (url: string, data = {}) => api.put(url, data);
export const apiDelete = (url: string) => api.delete(url);

export default api;
