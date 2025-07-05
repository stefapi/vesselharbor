import type * as Types from './types.ts'

/**
 * Returns the list of all tags if the user has permissions on their organization.
 */
export async function listalltags() {
  return api.get('/tags')
}

/**
 * Creates a new tag. The user must have permissions on a specific organization.
 * @param data Request data
 */
export async function createatag(data: Types.TagCreate) {
  return api.post('/tags', data)
}

/**
 * Returns information for a specific tag if the user has required permissions.
 * @param tag_id tag_id parameter
 */
export async function getatagtags(tag_id: number) {
  return api.get(`/tags/${tag_id}`)
}

/**
 * Deletes a tag if authorized.
 * @param tag_id tag_id parameter
 */
export async function deleteatag(tag_id: number) {
  return api.delete(`/tags/${tag_id}`)
}

/**
 * Returns groups associated with a tag.
 * @param tag_id tag_id parameter
 */
export async function groupslinkedtoatag(tag_id: number) {
  return api.get(`/tags/${tag_id}/groups`)
}

/**
 * Returns users associated with a tag.
 * @param tag_id tag_id parameter
 */
export async function userslinkedtoatag(tag_id: number) {
  return api.get(`/tags/${tag_id}/users`)
}

/**
 * Returns policies associated with a tag.
 * @param tag_id tag_id parameter
 */
export async function policieslinkedtoatag(tag_id: number) {
  return api.get(`/tags/${tag_id}/policies`)
}

/**
 * Returns elements associated with a tag.
 * @param tag_id tag_id parameter
 */
export async function elementslinkedtoatag(tag_id: number) {
  return api.get(`/tags/${tag_id}/elements`)
}

/**
 * Returns environments associated with a tag.
 * @param tag_id tag_id parameter
 */
export async function environmentslinkedtoatag(tag_id: number) {
  return api.get(`/tags/${tag_id}/environments`)
}
