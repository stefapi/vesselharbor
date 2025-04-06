// src/services/userService.ts
import api from '@/services/api.ts';

/**
 * Authentifie un utilisateur.
 */
export async function login(credentials: { username: string; password: string }) {
  const formData = new URLSearchParams();
  formData.append('username', credentials.username);
  formData.append('password', credentials.password);
  formData.append('grant_type', 'password');
  formData.append('client_id', 'fastapi');
  formData.append('client_secret', 'dfs');
  formData.append('scope', ''); // Scope vide ou valeurs séparées par des espaces

  return api.post('/login', formData, {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded', // Indispensable
    },
  });
}

/**
 * Récupère les informations de l'utilisateur connecté.
 */
export async function getUser() {
  const authStore = useAuthStore();
  return api.get(`/me`, {
          headers: { Authorization: `Bearer ${authStore.accessToken}` },
        });

}

/**
 * Envoie une demande de changement de mot de passe.
 */
export async function reset_password_request(email: string) {
  await api.post('/users/reset_password_request', { email});
}

/**
 * Change le mot de passe d'un utilisateur à partir d'un token
 */
export async function reset_password(token: string, new_password: string) {
  await api.post('/users/reset_password', {
      token,
      new_password
    });
}


/**
 * Rafraîchit le token d'accès à partir du refresh token stocké.
 */
export async function refresh() {
  const authStore = useAuthStore();
  const refreshToken = authStore.refreshToken;
  return await api.post('/refresh-token', { refresh_token: refreshToken });
}
