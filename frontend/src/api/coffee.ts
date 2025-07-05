import type * as Types from './types.ts'

/**
 * Returns a 418 I'm a teapot status code, as per RFC 2324.
 */
export async function Imateapot() {
  return api.get('/coffee/')
}
