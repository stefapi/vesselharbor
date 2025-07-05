import type * as Types from './types.ts'

/**
 * Crée une nouvelle règle associée à une politique
 * @param data Request data
 */
export async function creeruneregle(data: Types.RuleCreate) {
  return api.post('/rules', data)
}

/**
 * Récupère les détails d'une règle spécifique
 * @param rule_id rule_id parameter
 */
export async function detailduneregle(rule_id: number) {
  return api.get(`/rules/${rule_id}`)
}

/**
 * Met à jour une règle existante
 * @param rule_id rule_id parameter
 */
export async function mettreajouruneregle(rule_id: number, data: Types.RuleUpdate) {
  return api.put(`/rules/${rule_id}`, data)
}

/**
 * Supprime une règle existante
 * @param rule_id rule_id parameter
 */
export async function supprimeruneregle(rule_id: number) {
  return api.delete(`/rules/${rule_id}`)
}
