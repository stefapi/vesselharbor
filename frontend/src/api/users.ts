import type * as Types from './types.ts'

/**
 * Creates a new user in free mode in the system. The first user created automatically becomes superadmin.
 * @param data Request data
 */
export async function createauserinfreemode(data: Types.UserCreate) {
  return api.post('/users', data)
}

/**
 * Retrieves the list of users with pagination and optional filtering by email.
 */
export async function listusers() {
  return api.get('/users')
}

/**
 * Creates a new user in the system. It is attached to an Organization
 * @param organization_id organization_id parameter
 */
export async function createauser(organization_id: number, data: Types.UserCreate) {
  return api.post(`/users/${organization_id}`, data)
}

/**
 * Retrieves detailed information of a specific user by their ID.
 * @param user_id user_id parameter
 */
export async function getauserusers(user_id: number) {
  return api.get(`/users/${user_id}`)
}

/**
 * Modifies the personal information of an existing user (last name, first name, email, username).
 * @param user_id user_id parameter
 */
export async function updateuserinformation(user_id: number, data: Types.UserUpdate) {
  return api.put(`/users/${user_id}`, data)
}

/**
 * Permanently deletes a user from the system. A user cannot delete themselves, and the last superadmin cannot be deleted.
 * @param user_id user_id parameter
 */
export async function deleteauser(user_id: number) {
  return api.delete(`/users/${user_id}`)
}

/**
 * Allows a user to change their own password or an administrator to reset another user's password.
 * @param user_id user_id parameter
 */
export async function changepassword(user_id: number, data: Types.ChangePassword) {
  return api.put(`/users/${user_id}/password`, data)
}

/**
 * Allows a superadmin to modify another user's superadmin status. A superadmin cannot modify their own status, and the last superadmin cannot be demoted.
 * @param user_id user_id parameter
 */
export async function modifysuperadminstatus(user_id: number, data: Types.ChangeSuperadmin) {
  return api.put(`/users/${user_id}/superadmin`, data)
}

/**
 * Retrieves the list of groups the user belongs to.
 * @param user_id user_id parameter
 */
export async function usergroups(user_id: number) {
  return api.get(`/users/${user_id}/groups`)
}

/**
 * Retrieves the list of policies directly associated with the user.
 * @param user_id user_id parameter
 */
export async function userpolicies(user_id: number) {
  return api.get(`/users/${user_id}/policies`)
}

/**
 * Retrieves the list of organizations the user is associated with.
 * @param user_id user_id parameter
 */
export async function userorganizations(user_id: number) {
  return api.get(`/users/${user_id}/organizations`)
}

/**
 * Retrieves the list of tags associated with a specific user.
 * @param user_id user_id parameter
 */
export async function listusertagsusers(user_id: number) {
  return api.get(`/users/${user_id}/tags`)
}

/**
 * Adds a specific tag to a user for categorization or special attributes.
 * @param user_id user_id parameter
 * @param tag_id tag_id parameter
 */
export async function associatetagwithuser(user_id: number, tag_id: number) {
  return api.post(`/users/${user_id}/tags/${tag_id}`)
}

/**
 * Removes a specific tag from a user, deleting the associated categorization or attributes.
 * @param user_id user_id parameter
 * @param tag_id tag_id parameter
 */
export async function removetagfromuser(user_id: number, tag_id: number) {
  return api.delete(`/users/${user_id}/tags/${tag_id}`)
}
