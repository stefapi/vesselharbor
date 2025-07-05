import type * as Types from './types.ts'

/**
 * Retrieves the complete list of all groups in the system (reserved for superadmins)
 */
export async function listallgroups() {
  return api.get('/groups')
}

/**
 * Retrieves details of a specific group by its ID
 * @param group_id group_id parameter
 */
export async function groupdetails(group_id: number) {
  return api.get(`/groups/${group_id}`)
}

/**
 * Updates information for an existing group
 * @param group_id group_id parameter
 */
export async function updategroup(group_id: number, data: Types.GroupUpdate) {
  return api.put(`/groups/${group_id}`, data)
}

/**
 * Deletes an existing group and all its associations
 * @param group_id group_id parameter
 */
export async function deletegroup(group_id: number) {
  return api.delete(`/groups/${group_id}`)
}

/**
 * Creates a new group in the specified organization
 * @param organization_id organization_id parameter
 */
export async function creategroup(organization_id: number, data: Types.GroupCreate) {
  return api.post(`/groups/${organization_id}`, data)
}

/**
 * Retrieves all groups belonging to a specific organization
 * @param org_id org_id parameter
 */
export async function listorganizationgroups(org_id: number) {
  return api.get(`/groups/organization/${org_id}`)
}

/**
 * Retrieves all users belonging to a specific group
 * @param group_id group_id parameter
 */
export async function listgroupusersgroups(group_id: number) {
  return api.get(`/groups/${group_id}/users`)
}

/**
 * Adds a specific user to a group
 * @param group_id group_id parameter
 * @param user_id user_id parameter
 */
export async function assignuser(group_id: number, user_id: number) {
  return api.post(`/groups/${group_id}/users/${user_id}`)
}

/**
 * Removes a specific user from a group
 * @param group_id group_id parameter
 * @param user_id user_id parameter
 */
export async function removeuser(group_id: number, user_id: number) {
  return api.delete(`/groups/${group_id}/users/${user_id}`)
}

/**
 * Retrieves all policies associated with a specific group
 * @param group_id group_id parameter
 */
export async function listgrouppoliciesgroups(group_id: number) {
  return api.get(`/groups/${group_id}/policy`)
}

/**
 * Associates a specific policy with a group
 * @param group_id group_id parameter
 */
export async function assignpolicy(group_id: number) {
  return api.post(`/groups/${group_id}/policy`)
}

/**
 * Removes a specific policy from a group
 * @param group_id group_id parameter
 * @param policy_id policy_id parameter
 */
export async function removepolicy(group_id: number, policy_id: number) {
  return api.delete(`/groups/${group_id}/policy/${policy_id}`)
}

/**
 * Retrieves all tags associated with a specific group
 * @param group_id group_id parameter
 */
export async function listgrouptagsgroups(group_id: number) {
  return api.get(`/groups/${group_id}/tags`)
}

/**
 * Associates a specific tag with a group
 * @param group_id group_id parameter
 * @param tag_id tag_id parameter
 */
export async function addtagtogroup(group_id: number, tag_id: number) {
  return api.post(`/groups/${group_id}/tags/${tag_id}`)
}

/**
 * Removes a specific tag from a group
 * @param group_id group_id parameter
 * @param tag_id tag_id parameter
 */
export async function removetagfromgroup(group_id: number, tag_id: number) {
  return api.delete(`/groups/${group_id}/tags/${tag_id}`)
}
