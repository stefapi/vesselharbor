import type * as Types from './types.ts'

/**
 * Lists audit logs with pagination and filtering by action and user_id (accessible only by superadmin).
 */
export async function listauditlogsauditLogs() {
  return api.get('/audit-logs/')
}
