// src/services/groupService.ts
import api from '@/services/api';

/**
 * Crée un nouveau groupe dans l'environnement spécifié.
 * @param environmentId L'identifiant de l'environnement.
 * @param group Un objet contenant le nom et la description du groupe.
 */
export async function createGroup(environmentId: number, group: { name: string; description: string }) {
  return api.post(`/groups/${environmentId}`, group);
}

/**
 * Liste les groupes d'un environnement avec support des filtres et de la pagination.
 * @param environmentId L'identifiant de l'environnement.
 * @param params Paramètres (skip, limit, nom, etc.).
 */
export async function listGroups(environmentId: number, params: any = {}) {
  return api.get(`/groups/environment/${environmentId}`, { params });
}

/**
 * Met à jour les informations d'un groupe existant.
 * @param groupId L'identifiant du groupe.
 * @param group Un objet contenant le nom et la description mis à jour.
 */
export async function updateGroup(groupId: number, group: { name: string; description: string }) {
  return api.put(`/groups/${groupId}`, group);
}

/**
 * Supprime un groupe.
 * @param groupId L'identifiant du groupe à supprimer.
 */
export async function deleteGroup(groupId: number) {
  return api.delete(`/groups/${groupId}`);
}

/**
 * Affecte un utilisateur à un groupe.
 * @param groupId L'identifiant du groupe.
 * @param userId L'identifiant de l'utilisateur.
 */
export async function assignUserToGroup(groupId: number, userId: number) {
  return api.post(`/groups/${groupId}/users/${userId}`);
}

/**
 * Retire un utilisateur d'un groupe.
 * @param groupId L'identifiant du groupe.
 * @param userId L'identifiant de l'utilisateur.
 */
export async function removeUserFromGroup(groupId: number, userId: number) {
  return api.delete(`/groups/${groupId}/users/${userId}`);
}

/**
 * Liste tous les groupes (pour superadmin).
 */
export async function listAllGroups(params: any = {}) {
  return api.get('/groups', { params });
}

/**
 * Gère les fonctions d’un groupe
 */
// Ajoute une fonction à un groupe
export async function addFunctionToGroup(groupId: number, func: { name: string; description: string }) {
  return api.post(`/groups/${groupId}/functions`, func);
}

// Retire une fonction d’un groupe
export async function removeFunctionFromGroup(groupId: number, functionId: number) {
  return api.delete(`/groups/${groupId}/functions/${functionId}`);
}

// Récupère les fonctions assignées à un groupe
export async function getGroupFunctions(groupId: number) {
  // On suppose que l’API renvoie dans la réponse la liste des fonctions assignées
  return api.get(`/groups/${groupId}/functions`);
}

// Récupère la liste des fonctions disponibles depuis l’API
export async function getAvailableFunctions() {
  return api.get('/functions'); // On suppose que cet endpoint existe
}
