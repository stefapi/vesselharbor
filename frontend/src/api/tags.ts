import type * as Types from './types.ts'

/**
 * Renvoie la liste de tous les tags si l'utilisateur a les droits sur leur organisation.
 */
export async function listertouslestags() {
  return api.get('/tags')
}

/**
 * Crée un nouveau tag. L'utilisateur doit avoir les droits sur une organisation spécifique.
 * @param data Request data
 */
export async function creeruntag(data: Types.TagCreate) {
  return api.post('/tags', data)
}

/**
 * Renvoie les informations d'un tag spécifique si l'utilisateur a les droits requis.
 * @param tag_id tag_id parameter
 */
export async function recupereruntag(tag_id: number) {
  return api.get(`/tags/${tag_id}`)
}

/**
 * Supprime un tag s'il est autorisé.
 * @param tag_id tag_id parameter
 */
export async function supprimeruntag(tag_id: number) {
  return api.delete(`/tags/${tag_id}`)
}

/**
 * Renvoie les groupes associés à un tag.
 * @param tag_id tag_id parameter
 */
export async function groupesliesauntag(tag_id: number) {
  return api.get(`/tags/${tag_id}/groups`)
}

/**
 * Renvoie les utilisateurs associés à un tag.
 * @param tag_id tag_id parameter
 */
export async function utilisateursliesauntag(tag_id: number) {
  return api.get(`/tags/${tag_id}/users`)
}

/**
 * Renvoie les policies associées à un tag.
 * @param tag_id tag_id parameter
 */
export async function policieslieesauntag(tag_id: number) {
  return api.get(`/tags/${tag_id}/policies`)
}

/**
 * Renvoie les éléments associés à un tag.
 * @param tag_id tag_id parameter
 */
export async function elementsliesauntag(tag_id: number) {
  return api.get(`/tags/${tag_id}/elements`)
}

/**
 * Renvoie les environnements associés à un tag.
 * @param tag_id tag_id parameter
 */
export async function environnementsliesauntag(tag_id: number) {
  return api.get(`/tags/${tag_id}/environments`)
}
