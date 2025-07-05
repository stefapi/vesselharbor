import type * as Types from './types.ts'

/**
 * Récupère la liste des organisations auxquelles l'utilisateur a accès
 */
export async function listerlesorganisationsorganizations() {
  return api.get('/organizations')
}

/**
 * Crée une nouvelle organisation et configure les groupes et politiques par défaut
 * @param data Request data
 */
export async function creeruneorganisation(data: Types.OrganizationCreate) {
  return api.post('/organizations', data)
}

/**
 * Récupère les détails d'une organisation spécifique
 * @param org_id org_id parameter
 */
export async function detailduneorganisation(org_id: number) {
  return api.get(`/organizations/${org_id}`)
}

/**
 * Met à jour les informations d'une organisation existante
 * @param org_id org_id parameter
 */
export async function mettreajouruneorganisation(org_id: number, data: Types.OrganizationUpdate) {
  return api.put(`/organizations/${org_id}`, data)
}

/**
 * Supprime une organisation existante et toutes ses données associées
 * @param org_id org_id parameter
 */
export async function supprimeruneorganisation(org_id: number) {
  return api.delete(`/organizations/${org_id}`)
}

/**
 * Ajoute un utilisateur spécifié à une organisation
 * @param org_id org_id parameter
 * @param user_id user_id parameter
 */
export async function ajouterunutilisateurauneorganisation(org_id: number, user_id: number) {
  return api.post(`/organizations/${org_id}/users/${user_id}`)
}

/**
 * Retire un utilisateur spécifié d'une organisation
 * @param org_id org_id parameter
 * @param user_id user_id parameter
 */
export async function retirerunutilisateurduneorganisation(org_id: number, user_id: number) {
  return api.delete(`/organizations/${org_id}/users/${user_id}`)
}

/**
 * Récupère tous les tags associés à une organisation
 * @param org_id org_id parameter
 */
export async function listerlestagsduneorganisationorganizations(org_id: number) {
  return api.get(`/organizations/${org_id}/tags`)
}

/**
 * Récupère toutes les politiques associées à une organisation
 * @param org_id org_id parameter
 */
export async function listerlespolitiquesduneorganisationorganizations(org_id: number) {
  return api.get(`/organizations/${org_id}/policies`)
}

/**
 * Récupère tous les groupes associés à une organisation
 * @param org_id org_id parameter
 */
export async function listerlesgroupesduneorganisationorganizations(org_id: number) {
  return api.get(`/organizations/${org_id}/groups`)
}

/**
 * Récupère tous les environnements associés à une organisation
 * @param org_id org_id parameter
 */
export async function listerlesenvironnementsduneorganisationorganizations(org_id: number) {
  return api.get(`/organizations/${org_id}/environments`)
}

/**
 * Récupère tous les utilisateurs ayant accès à une organisation spécifique.
 * @param org_id org_id parameter
 */
export async function listerlesutilisateursduneorganisationorganizations(org_id: number) {
  return api.get(`/organizations/${org_id}/users`)
}

/**
 * Récupère tous les éléments d'une organisation auxquels l'utilisateur a accès, avec pagination et filtrage par nom.
 * @param org_id org_id parameter
 */
export async function listerleselementsduneorganisationorganizations(org_id: number) {
  return api.get(`/organizations/${org_id}/elements`)
}
