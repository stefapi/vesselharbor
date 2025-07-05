import type * as Types from './types.ts'

/**
 * Retrieves the list of policies for a given organization with pagination.
 */
export async function listpolicies() {
  return api.get('/policies')
}

/**
 * Creates a new policy in the specified organization.
 * @param data Request data
 */
export async function createpolicy(data: Types.PolicyCreate) {
  return api.post('/policies', data)
}

/**
 * Retrieves details of a specific policy by its ID.
 * @param policy_id policy_id parameter
 */
export async function getpolicypolicies(policy_id: number) {
  return api.get(`/policies/${policy_id}`)
}

/**
 * Modifies information of an existing policy.
 * @param policy_id policy_id parameter
 */
export async function updatepolicy(policy_id: number, data: Types.PolicyUpdate) {
  return api.put(`/policies/${policy_id}`, data)
}

/**
 * Permanently deletes an existing policy.
 * @param policy_id policy_id parameter
 */
export async function deletepolicy(policy_id: number) {
  return api.delete(`/policies/${policy_id}`)
}

/**
 * Retrieves all users associated with a specific policy.
 * @param policy_id policy_id parameter
 */
export async function listpolicyuserspolicies(policy_id: number) {
  return api.get(`/policies/${policy_id}/users`)
}

/**
 * Associates a specific user with a policy to grant defined permissions.
 * @param policy_id policy_id parameter
 * @param user_id user_id parameter
 */
export async function addusertopolicy(policy_id: number, user_id: number) {
  return api.post(`/policies/${policy_id}/users/${user_id}`)
}

/**
 * Disassociates a user from a policy, revoking associated permissions.
 * @param policy_id policy_id parameter
 * @param user_id user_id parameter
 */
export async function removeuserfrompolicy(policy_id: number, user_id: number) {
  return api.delete(`/policies/${policy_id}/users/${user_id}`)
}

/**
 * Retrieves all groups associated with a specific policy.
 * @param policy_id policy_id parameter
 */
export async function listpolicygroupspolicies(policy_id: number) {
  return api.get(`/policies/${policy_id}/groups`)
}

/**
 * Associates a group with a policy, granting defined permissions to all group members.
 * @param policy_id policy_id parameter
 * @param group_id group_id parameter
 */
export async function addgrouptopolicy(policy_id: number, group_id: number) {
  return api.post(`/policies/${policy_id}/groups/${group_id}`)
}

/**
 * Disassociates a group from a policy, revoking associated permissions from all group members.
 * @param policy_id policy_id parameter
 * @param group_id group_id parameter
 */
export async function removegroupfrompolicy(policy_id: number, group_id: number) {
  return api.delete(`/policies/${policy_id}/groups/${group_id}`)
}

/**
 * Retrieves all rules associated with a specific policy
 * @param policy_id policy_id parameter
 */
export async function listpolicyrulespolicies(policy_id: number) {
  return api.get(`/policies/${policy_id}/rules`)
}

/**
 * Associates a tag with a policy, applying the policy to all resources with this tag.
 * @param policy_id policy_id parameter
 * @param tag_id tag_id parameter
 */
export async function addtagtopolicy(policy_id: number, tag_id: number) {
  return api.post(`/policies/${policy_id}/tags/${tag_id}`)
}

/**
 * Disassociates a tag from a policy, removing policy application from resources with this tag.
 * @param policy_id policy_id parameter
 * @param tag_id tag_id parameter
 */
export async function removetagfrompolicy(policy_id: number, tag_id: number) {
  return api.delete(`/policies/${policy_id}/tags/${tag_id}`)
}
