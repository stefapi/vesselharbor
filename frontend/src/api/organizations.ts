import type * as Types from './types.ts'

/**
 * Retrieve list of organizations accessible to the user
 */
export async function listorganizations() {
  return api.get('/organizations')
}

/**
 * Create a new organization and configure default groups/policies
 * @param data Request data
 */
export async function createorganization(data: Types.OrganizationCreate) {
  return api.post('/organizations', data)
}

/**
 * Retrieve details of a specific organization
 * @param org_id org_id parameter
 */
export async function organizationdetails(org_id: number) {
  return api.get(`/organizations/${org_id}`)
}

/**
 * Update information of an existing organization
 * @param org_id org_id parameter
 */
export async function updateorganization(org_id: number, data: Types.OrganizationUpdate) {
  return api.put(`/organizations/${org_id}`, data)
}

/**
 * Delete an existing organization and all associated data
 * @param org_id org_id parameter
 */
export async function deleteorganization(org_id: number) {
  return api.delete(`/organizations/${org_id}`)
}

/**
 * Add specified user to an organization
 * @param org_id org_id parameter
 * @param user_id user_id parameter
 */
export async function addusertoorganization(org_id: number, user_id: number) {
  return api.post(`/organizations/${org_id}/users/${user_id}`)
}

/**
 * Remove specified user from an organization
 * @param org_id org_id parameter
 * @param user_id user_id parameter
 */
export async function removeuserfromorganization(org_id: number, user_id: number) {
  return api.delete(`/organizations/${org_id}/users/${user_id}`)
}

/**
 * Retrieve all tags associated with an organization
 * @param org_id org_id parameter
 */
export async function listorganizationtagsorganizations(org_id: number) {
  return api.get(`/organizations/${org_id}/tags`)
}

/**
 * Retrieve all policies associated with an organization
 * @param org_id org_id parameter
 */
export async function listorganizationpoliciesorganizations(org_id: number) {
  return api.get(`/organizations/${org_id}/policies`)
}

/**
 * Retrieve all groups associated with an organization
 * @param org_id org_id parameter
 */
export async function listorganizationgroupsorganizations(org_id: number) {
  return api.get(`/organizations/${org_id}/groups`)
}

/**
 * Retrieve all environments associated with an organization
 * @param org_id org_id parameter
 */
export async function listorganizationenvironmentsorganizations(org_id: number) {
  return api.get(`/organizations/${org_id}/environments`)
}

/**
 * Retrieve all users with access to a specific organization.
 * @param org_id org_id parameter
 */
export async function listorganizationusersorganizations(org_id: number) {
  return api.get(`/organizations/${org_id}/users`)
}

/**
 * Retrieve all elements in an organization accessible to the user, with pagination and name filtering.
 * @param org_id org_id parameter
 */
export async function listorganizationelementsorganizations(org_id: number) {
  return api.get(`/organizations/${org_id}/elements`)
}
