import api from '@/services/api';

/**
 * Récupère la liste des utilisateurs associés à un environnement donné.
 * On suppose que l'API possède un endpoint pour récupérer les utilisateurs d'un environnement.
 * @param environmentId L'identifiant de l'environnement.
 * @param params Paramètres optionnels pour filtrer ou paginer la liste.
 */
export async function listEnvironmentUsers(environmentId: number, params: any = {}) {
  return api.get(`/environment/${environmentId}/users`, { params });
}

/**
 * Met à jour les droits ou les affectations d'un utilisateur dans un environnement.
 * Par exemple, cela peut permettre de modifier le rôle ou d'autres droits spécifiques.
 * @param environmentId L'identifiant de l'environnement.
 * @param userId L'identifiant de l'utilisateur.
 * @param rights Un objet contenant les nouvelles affectations/droits à appliquer.
 */
export async function updateUserEnvironmentRights(environmentId: number, userId: number, rights: any) {
  return api.put(`/environment/${environmentId}/users/${userId}`, rights);
}
