// This Content is Auto Generated

/**
 * Body_login_login_post

 */

export interface Body_login_login_post {
  grant_type?: string | null

  username: string

  password: string

  scope?: string

  client_id?: string | null

  client_secret?: string | null
}

/**
 * ChangePassword

 */

export interface ChangePassword {
  old_password: string | null

  new_password: string | null

  send_email: boolean
}

/**
 * ChangeSuperadmin

 */

export interface ChangeSuperadmin {
  is_superadmin: boolean
}

/**
 * ElementCreate

 */

export interface ElementCreate {
  name: string

  description?: string | null

  environment_id: number

  subcomponent_type: string

  subcomponent_data: Record<string, unknown>
}

/**
 * ElementUpdate

 */

export interface ElementUpdate {
  name: string | null

  description: string | null

  environment_id?: number | null
}

/**
 * EmptyData
 * Empty data structure for responses with no data
 */

export type EmptyData = Record<string, never>

/**
 * EnvironmentCreate

 */

export interface EnvironmentCreate {
  name: string

  description?: string | null

  organization_id: number
}

/**
 * GroupCreate

 */

export interface GroupCreate {
  name: string

  description?: string | null

  organization_id: number
}

/**
 * GroupUpdate

 */

export interface GroupUpdate {
  name?: string | null

  description?: string | null
}

/**
 * HTTPValidationError

 */

export interface HTTPValidationError {
  detail?: ValidationError[]
}

/**
 * LoginData
 * Data structure for login response
 */

export interface LoginData {
  token_type: string
}

/**
 * LoginResponse
 * Response schema for login endpoint
 */

export interface LoginResponse {
  status: string

  message: string

  data: LoginData
}

/**
 * LogoutResponse
 * Response schema for logout endpoint
 */

export interface LogoutResponse {
  status: string

  message: string

  data: EmptyData
}

/**
 * MeResponse
 * Response schema for me/profile endpoint
 */

export interface MeResponse {
  status: string

  message: string

  data: UserOut
}

/**
 * OrganizationCreate

 */

export interface OrganizationCreate {
  name: string

  description?: string | null
}

/**
 * OrganizationUpdate

 */

export interface OrganizationUpdate {
  name: string

  description?: string | null
}

/**
 * PasswordReset

 */

export interface PasswordReset {
  token: string

  new_password: string
}

/**
 * PasswordResetRequest

 */

export interface PasswordResetRequest {
  email: string
}

/**
 * PasswordResetResponse
 * Response schema for password reset endpoints
 */

export interface PasswordResetResponse {
  status: string

  message: string

  data: never | null
}

/**
 * PolicyCreate

 */

export interface PolicyCreate {
  name: string

  description?: string | null

  organization_id: number
}

/**
 * PolicyUpdate

 */

export interface PolicyUpdate {
  name?: string | null

  description?: string | null
}

/**
 * RefreshTokenData
 * Data structure for refresh token response
 */

export interface RefreshTokenData {
  token_type: string
}

/**
 * RefreshTokenResponse
 * Response schema for refresh token endpoint
 */

export interface RefreshTokenResponse {
  status: string

  message: string

  data: RefreshTokenData
}

/**
 * RuleCreate

 */

export interface RuleCreate {
  policy_id: number

  function_id: number

  environment_id?: number | null

  element_id?: number | null

  access_schedule?: Record<string, unknown> | null
}

/**
 * RuleUpdate

 */

export interface RuleUpdate {
  function_id?: number | null

  environment_id?: number | null

  element_id?: number | null

  access_schedule?: Record<string, unknown> | null
}

/**
 * TagCreate

 */

export interface TagCreate {
  value: string

  organization_id: number
}

/**
 * TagOut

 */

export interface TagOut {
  id: number

  value: string
}

/**
 * UserCreate

 */

export interface UserCreate {
  username: string

  first_name: string

  last_name: string

  email: string

  password: string
}

/**
 * UserOut

 */

export interface UserOut {
  id: number

  username: string

  first_name: string

  last_name: string

  email: string

  is_superadmin: boolean

  tags?: TagOut[]
}

/**
 * UserUpdate

 */

export interface UserUpdate {
  first_name: string

  last_name: string

  username: string

  email: string
}

/**
 * ValidationError

 */

export interface ValidationError {
  loc: string | number[]

  msg: string

  type: string
}
