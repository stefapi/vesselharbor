// src/services/userService.ts
import api from '@/services/api.ts';

/**
 * Crée un nouvel utilisateur.
 * Le payload doit contenir l'email et le mot de passe.
 */
export async function createUser(user: { email: string; password: string }) {
  return api.post('/users', user);
}


/**
 * Récupère la liste des utilisateurs.
 * On peut filtrer par email et utiliser la pagination.
 */
export async function listUsers(params: any = {}) {
  return api.get('/users', { params });
}

/**
 * Supprime un utilisateur.
 */
export async function deleteUser(userId: number) {
  return api.delete(`/users/${userId}`);
}

/**
 * Met à jour le statut superadmin d'un utilisateur.
 */
export async function updateSuperadmin(userId: number, isSuperadmin: boolean) {
  return api.put(`/users/${userId}/superadmin`, { is_superadmin: isSuperadmin });
}

/**
 * Permet de changer le mot de passe de l'utilisateur (self-update).
 */
export async function changePassword(userId: number, passwords: { old_password: string; new_password: string }) {
  return api.put(`/users/${userId}/password`, passwords);
}

/**
 * Récupère la liste des groupes assignés à un utilisateur.
 */
export async function getUserGroups(userId: number) {
  return api.get(`/users/${userId}/groups`);
}
