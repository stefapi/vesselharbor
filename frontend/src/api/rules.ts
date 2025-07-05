import type * as Types from './types.ts'

/**
 * Creates a new rule associated with a policy
 * @param data Request data
 */
export async function createarule(data: Types.RuleCreate) {
  return api.post('/rules', data)
}

/**
 * Retrieves details of a specific rule
 * @param rule_id rule_id parameter
 */
export async function ruledetails(rule_id: number) {
  return api.get(`/rules/${rule_id}`)
}

/**
 * Updates an existing rule
 * @param rule_id rule_id parameter
 */
export async function updatearule(rule_id: number, data: Types.RuleUpdate) {
  return api.put(`/rules/${rule_id}`, data)
}

/**
 * Deletes an existing rule
 * @param rule_id rule_id parameter
 */
export async function deletearule(rule_id: number) {
  return api.delete(`/rules/${rule_id}`)
}
