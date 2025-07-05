import type * as Types from './types.ts'

/**
 * Récupère la liste des policies pour une organisation donnée avec pagination.
 */
export async function listerlespolicies() {
  return api.get('/policies')
}

/**
 * Crée une nouvelle policy dans l'organisation spécifiée.
 * @param data Request data
 */
export async function creerunepolicy(data: Types.PolicyCreate) {
  return api.post('/policies', data)
}

/**
 * Récupère les détails d'une policy spécifique par son ID.
 * @param policy_id policy_id parameter
 */
export async function obtenirunepolicy(policy_id: number) {
  return api.get(`/policies/${policy_id}`)
}

/**
 * Modifie les informations d'une policy existante.
 * @param policy_id policy_id parameter
 */
export async function mettreajourunepolicy(policy_id: number, data: Types.PolicyUpdate) {
  return api.put(`/policies/${policy_id}`, data)
}

/**
 * Supprime définitivement une policy existante.
 * @param policy_id policy_id parameter
 */
export async function supprimerunepolicy(policy_id: number) {
  return api.delete(`/policies/${policy_id}`)
}

/**
 * Récupère la liste de tous les utilisateurs associés à une policy spécifique.
 * @param policy_id policy_id parameter
 */
export async function listerlesutilisateursdunepolicypolicies(policy_id: number) {
  return api.get(`/policies/${policy_id}/users`)
}

/**
 * Associe un utilisateur spécifique à une policy pour lui accorder les permissions définies.
 * @param policy_id policy_id parameter
 * @param user_id user_id parameter
 */
export async function ajouterunutilisateuraunepolicy(policy_id: number, user_id: number) {
  return api.post(`/policies/${policy_id}/users/${user_id}`)
}

/**
 * Dissocie un utilisateur d'une policy, lui retirant ainsi les permissions associées.
 * @param policy_id policy_id parameter
 * @param user_id user_id parameter
 */
export async function retirerunutilisateurdunepolicy(policy_id: number, user_id: number) {
  return api.delete(`/policies/${policy_id}/users/${user_id}`)
}

/**
 * Récupère la liste de tous les groupes associés à une policy spécifique.
 * @param policy_id policy_id parameter
 */
export async function listerlesgroupesdunepolicypolicies(policy_id: number) {
  return api.get(`/policies/${policy_id}/groups`)
}

/**
 * Associe un groupe à une policy, accordant ainsi les permissions définies à tous les membres du groupe.
 * @param policy_id policy_id parameter
 * @param group_id group_id parameter
 */
export async function ajouterungroupeaunepolicy(policy_id: number, group_id: number) {
  return api.post(`/policies/${policy_id}/groups/${group_id}`)
}

/**
 * Dissocie un groupe d'une policy, retirant ainsi les permissions associées à tous les membres du groupe.
 * @param policy_id policy_id parameter
 * @param group_id group_id parameter
 */
export async function retirerungroupedunepolicy(policy_id: number, group_id: number) {
  return api.delete(`/policies/${policy_id}/groups/${group_id}`)
}

/**
 * Récupère toutes les règles associées à une politique spécifique
 * @param policy_id policy_id parameter
 */
export async function listerlesreglesdunepolitiquepolicies(policy_id: number) {
  return api.get(`/policies/${policy_id}/rules`)
}

/**
 * Associe un tag à une policy, permettant d'appliquer la policy à tous les éléments portant ce tag.
 * @param policy_id policy_id parameter
 * @param tag_id tag_id parameter
 */
export async function ajouteruntagaunepolicy(policy_id: number, tag_id: number) {
  return api.post(`/policies/${policy_id}/tags/${tag_id}`)
}

/**
 * Dissocie un tag d'une policy, retirant ainsi l'application de la policy aux éléments portant ce tag.
 * @param policy_id policy_id parameter
 * @param tag_id tag_id parameter
 */
export async function retireruntagdunepolicy(policy_id: number, tag_id: number) {
  return api.delete(`/policies/${policy_id}/tags/${tag_id}`)
}
