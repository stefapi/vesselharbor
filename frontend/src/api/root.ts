import type * as Types from './types.ts'

/**
 * Authenticates a user with their email and password and returns an access token
 */
export async function authenticateauser() {
  return api.post('/login')
}

/**
 * Logs out the user by deleting authentication cookies
 */
export async function logout() {
  return api.post('/logout')
}

/**
 * Renews the access token from a valid refresh token
 */
export async function renewtoken() {
  return api.post('/refresh-token')
}

/**
 * Retrieves the profile information of the currently connected user
 */
export async function connecteduserprofile() {
  return api.get('/me')
}

/**
 * Sends an email containing a password reset link to the provided email address
 * @param data Request data
 */
export async function requestpasswordreset(data: Types.PasswordResetRequest) {
  return api.post('/users/reset_password_request', data)
}

/**
 * Resets a user's password using a valid reset token
 * @param data Request data
 */
export async function resetpassword(data: Types.PasswordReset) {
  return api.post('/users/reset_password', data)
}
