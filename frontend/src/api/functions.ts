import type * as Types from './types.ts'

/**
 * Returns all functions if the user has required permissions.
 */
export async function listfunctions() {
  return api.get('/functions')
}

/**
 * Returns information for a specific function.
 * @param function_id function_id parameter
 */
export async function getafunctionfunctions(function_id: number) {
  return api.get(`/functions/${function_id}`)
}
