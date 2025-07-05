import type * as Types from './types.ts'

/**
 * Returns a 200 OK status code if the service is running. Used for Kubernetes/Docker health checks.
 */
export async function healthCheck() {
  return api.get('/health/')
}
