import type * as Types from './types.ts'

/**
 * Liste les logs d'audit avec pagination et filtrage par action et user_id (accessible uniquement par superadmin).
 */
export async function listerleslogsdauditauditLogs() {
  return api.get('/audit-logs/')
}
