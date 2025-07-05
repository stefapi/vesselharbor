import type * as Types from './types.ts'

/**
 * Récupère la liste complète de tous les groupes dans le système (réservé aux superadmins)
 */
export async function listertouslesgroupesgroups() {
  return api.get('/groups')
}

/**
 * Récupère les détails d'un groupe spécifique par son identifiant
 * @param group_id group_id parameter
 */
export async function detaildungroupe(group_id: number) {
  return api.get(`/groups/${group_id}`)
}

/**
 * Met à jour les informations d'un groupe existant
 * @param group_id group_id parameter
 */
export async function mettreajourungroupe(group_id: number, data: Types.GroupUpdate) {
  return api.put(`/groups/${group_id}`, data)
}

/**
 * Supprime un groupe existant et toutes ses associations
 * @param group_id group_id parameter
 */
export async function supprimerungroupe(group_id: number) {
  return api.delete(`/groups/${group_id}`)
}

/**
 * Crée un nouveau groupe dans l'organisation spécifiée
 * @param organization_id organization_id parameter
 */
export async function creerungroupe(organization_id: number, data: Types.GroupCreate) {
  return api.post(`/groups/${organization_id}`, data)
}

/**
 * Récupère tous les groupes appartenant à une organisation spécifique
 * @param org_id org_id parameter
 */
export async function listerlesgroupesduneorganisationgroups(org_id: number) {
  return api.get(`/groups/organization/${org_id}`)
}

/**
 * Récupère la liste de tous les utilisateurs appartenant à un groupe spécifique
 * @param group_id group_id parameter
 */
export async function listerlesutilisateursdungroupegroups(group_id: number) {
  return api.get(`/groups/${group_id}/users`)
}

/**
 * Ajoute un utilisateur spécifique à un groupe
 * @param group_id group_id parameter
 * @param user_id user_id parameter
 */
export async function associerunutilisateur(group_id: number, user_id: number) {
  return api.post(`/groups/${group_id}/users/${user_id}`)
}

/**
 * Retire un utilisateur spécifique d'un groupe
 * @param group_id group_id parameter
 * @param user_id user_id parameter
 */
export async function retirerunutilisateur(group_id: number, user_id: number) {
  return api.delete(`/groups/${group_id}/users/${user_id}`)
}

/**
 * Récupère la liste de toutes les politiques associées à un groupe spécifique
 * @param group_id group_id parameter
 */
export async function listerlespoliciesdungroupegroups(group_id: number) {
  return api.get(`/groups/${group_id}/policy`)
}

/**
 * Associe une politique spécifique à un groupe
 * @param group_id group_id parameter
 */
export async function associerunepolicy(group_id: number) {
  return api.post(`/groups/${group_id}/policy`)
}

/**
 * Retire une politique spécifique d'un groupe
 * @param group_id group_id parameter
 * @param policy_id policy_id parameter
 */
export async function retirerunepolicy(group_id: number, policy_id: number) {
  return api.delete(`/groups/${group_id}/policy/${policy_id}`)
}

/**
 * Récupère la liste de tous les tags associés à un groupe spécifique
 * @param group_id group_id parameter
 */
export async function listerlestagsdungroupegroups(group_id: number) {
  return api.get(`/groups/${group_id}/tags`)
}

/**
 * Associe un tag spécifique à un groupe
 * @param group_id group_id parameter
 * @param tag_id tag_id parameter
 */
export async function ajouteruntagaungroupe(group_id: number, tag_id: number) {
  return api.post(`/groups/${group_id}/tags/${tag_id}`)
}

/**
 * Retire un tag spécifique d'un groupe
 * @param group_id group_id parameter
 * @param tag_id tag_id parameter
 */
export async function retireruntagdungroupe(group_id: number, tag_id: number) {
  return api.delete(`/groups/${group_id}/tags/${tag_id}`)
}
