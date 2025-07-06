import type * as Types from './types.ts'

/**
 * Authenticates a user with their email and password and returns an access token
 * @param data Request data
 */
export async function authenticateauser(data: Types.Body_login_login_post) {
  const formData = new FormData()

  if (data.grant_type !== null && data.grant_type !== undefined) {
    formData.append('grant_type', data.grant_type)
  }

  if (data.username !== null && data.username !== undefined) {
    formData.append('username', data.username)
  }

  if (data.password !== null && data.password !== undefined) {
    formData.append('password', data.password)
  }

  if (data.scope !== null && data.scope !== undefined) {
    formData.append('scope', data.scope)
  }

  if (data.client_id !== null && data.client_id !== undefined) {
    formData.append('client_id', data.client_id)
  }

  if (data.client_secret !== null && data.client_secret !== undefined) {
    formData.append('client_secret', data.client_secret)
  }

  return api.post('/login', formData, {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
  })
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
