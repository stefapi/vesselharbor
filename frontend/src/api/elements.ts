import type * as Types from './types.ts'

/**
 * Crée un élément dans un environnement donné.
 * @param environment_id environment_id parameter
 */
export async function creerunelement(environment_id: number, data: Types.ElementCreate) {
  return api.post(`/elements/${environment_id}`, data)
}

/**
 * Renvoie les informations d'un élément spécifique.
 * @param element_id element_id parameter
 */
export async function recupererunelement(element_id: number) {
  return api.get(`/elements/${element_id}`)
}

/**
 * Modifie les informations d'un élément.
 * @param element_id element_id parameter
 */
export async function mettreajourunelement(element_id: number, data: Types.ElementUpdate) {
  return api.put(`/elements/${element_id}`, data)
}

/**
 * Supprime un élément donné.
 * @param element_id element_id parameter
 */
export async function supprimerunelement(element_id: number) {
  return api.delete(`/elements/${element_id}`)
}

/**
 * Récupère tous les tags associés à un élément.
 * @param element_id element_id parameter
 */
export async function listerlestagsdunelementelements(element_id: number) {
  return api.get(`/elements/${element_id}/tags`)
}

/**
 * Associe un tag existant à un élément.
 * @param element_id element_id parameter
 * @param tag_id tag_id parameter
 */
export async function ajouteruntagaunelement(element_id: number, tag_id: number) {
  return api.post(`/elements/${element_id}/tags/${tag_id}`)
}

/**
 * Retire l'association entre un tag et un élément.
 * @param element_id element_id parameter
 * @param tag_id tag_id parameter
 */
export async function retireruntagdunelement(element_id: number, tag_id: number) {
  return api.delete(`/elements/${element_id}/tags/${tag_id}`)
}
