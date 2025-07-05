import type * as Types from './types.ts'

/**
 * Renvoie toutes les fonctions si l'utilisateur a les droits requis.
 */
export async function listerlesfonctionsfunctions() {
  return api.get('/functions')
}

/**
 * Renvoie les informations d'une fonction spécifique.
 * @param function_id function_id parameter
 */
export async function recupererunefonction(function_id: number) {
  return api.get(`/functions/${function_id}`)
}
