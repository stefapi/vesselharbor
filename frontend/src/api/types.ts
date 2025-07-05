// This Content is Auto Generated

/**
 * ApplicationOut
 
 */

export interface ApplicationOut {
  id: number

  name: string

  description: string | null

  plugin_name: string

  plugin_version: string

  application_type: string

  deployment_status: string

  config: Record<string, unknown> | null

  is_active: boolean

  element_id: number

  stack_id: number | null

  vm_id: number | null

  physical_host_id: number | null
}

/**
 * AuditLogOut
 
 */

export interface AuditLogOut {
  id: number

  user_id: number | null

  action: string

  details: string | null

  timestamp: string
}

/**
 * BaseResponse[ElementOut]
 
 */

export interface BaseResponse_ElementOut_ {
  status: string

  message: string

  data: ElementOut
}

/**
 * BaseResponse[EmptyData]
 
 */

export interface BaseResponse_EmptyData_ {
  status: string

  message: string

  data: EmptyData
}

/**
 * BaseResponse[EnvironmentOut]
 
 */

export interface BaseResponse_EnvironmentOut_ {
  status: string

  message: string

  data: EnvironmentOut
}

/**
 * BaseResponse[FunctionOut]
 
 */

export interface BaseResponse_FunctionOut_ {
  status: string

  message: string

  data: FunctionOut
}

/**
 * BaseResponse[GroupOut]
 
 */

export interface BaseResponse_GroupOut_ {
  status: string

  message: string

  data: GroupOut
}

/**
 * BaseResponse[List[AuditLogOut]]
 
 */

export interface BaseResponse_List_AuditLogOut__ {
  status: string

  message: string

  data: AuditLogOut[]
}

/**
 * BaseResponse[List[ElementOut]]
 
 */

export interface BaseResponse_List_ElementOut__ {
  status: string

  message: string

  data: ElementOut[]
}

/**
 * BaseResponse[List[EnvironmentOut]]
 
 */

export interface BaseResponse_List_EnvironmentOut__ {
  status: string

  message: string

  data: EnvironmentOut[]
}

/**
 * BaseResponse[List[FunctionOut]]
 
 */

export interface BaseResponse_List_FunctionOut__ {
  status: string

  message: string

  data: FunctionOut[]
}

/**
 * BaseResponse[List[GroupOut]]
 
 */

export interface BaseResponse_List_GroupOut__ {
  status: string

  message: string

  data: GroupOut[]
}

/**
 * BaseResponse[List[OrganizationOut]]
 
 */

export interface BaseResponse_List_OrganizationOut__ {
  status: string

  message: string

  data: OrganizationOut[]
}

/**
 * BaseResponse[List[PhysicalHostOut]]
 
 */

export interface BaseResponse_List_PhysicalHostOut__ {
  status: string

  message: string

  data: PhysicalHostOut[]
}

/**
 * BaseResponse[List[PolicyOut]]
 
 */

export interface BaseResponse_List_PolicyOut__ {
  status: string

  message: string

  data: PolicyOut[]
}

/**
 * BaseResponse[List[RuleOut]]
 
 */

export interface BaseResponse_List_RuleOut__ {
  status: string

  message: string

  data: RuleOut[]
}

/**
 * BaseResponse[List[TagOut]]
 
 */

export interface BaseResponse_List_TagOut__ {
  status: string

  message: string

  data: TagOut[]
}

/**
 * BaseResponse[List[UserOut]]
 
 */

export interface BaseResponse_List_UserOut__ {
  status: string

  message: string

  data: UserOut[]
}

/**
 * BaseResponse[OrganizationOut]
 
 */

export interface BaseResponse_OrganizationOut_ {
  status: string

  message: string

  data: OrganizationOut
}

/**
 * BaseResponse[PolicyOut]
 
 */

export interface BaseResponse_PolicyOut_ {
  status: string

  message: string

  data: PolicyOut
}

/**
 * BaseResponse[RuleOut]
 
 */

export interface BaseResponse_RuleOut_ {
  status: string

  message: string

  data: RuleOut
}

/**
 * BaseResponse[TagOut]
 
 */

export interface BaseResponse_TagOut_ {
  status: string

  message: string

  data: TagOut
}

/**
 * BaseResponse[UserOut]
 
 */

export interface BaseResponse_UserOut_ {
  status: string

  message: string

  data: UserOut
}

/**
 * BaseResponse[str]
 
 */

export interface BaseResponse_str_ {
  status: string

  message: string

  data: string
}

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
 * ComponentHealth
 * Health status of a system component
 */

export interface ComponentHealth {
  status: string

  details?: string | null
}

/**
 * ContainerClusterOut
 
 */

export interface ContainerClusterOut {
  id: number

  mode: string

  version: string

  ha_enabled: boolean

  endpoint: string

  stack_id: number | null

  element_id: number
}

/**
 * ContainerNodeOut
 
 */

export interface ContainerNodeOut {
  id: number

  cluster_id: number

  vm_id: number | null

  host_id: number | null

  role: string

  element_id: number
}

/**
 * DomainOut
 
 */

export interface DomainOut {
  id: number

  element_id: number

  fqdn: string

  dnssec_enabled: boolean

  dnssec_status: string | null

  dnssec_last_signed: string | null

  dnssec_key_tag: number | null

  dnssec_algorithm: number | null

  dnssec_digest_type: number | null

  dnssec_digest: string | null
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
 * ElementOut
 
 */

export interface ElementOut {
  id: number

  name: string

  description: string | null

  environment_id: number

  environment?: EnvironmentBase | null

  rules?: RuleOut[] | null

  users?: UserOut[] | null

  groups?: GroupOut[] | null

  tags?: TagOut[] | null

  environment_physical_hosts?: PhysicalHostOut[] | null

  network?: NetworkOut | null

  vm?: VMOut | null

  storage_pool?: StoragePoolOut | null

  volume?: VolumeOut | null

  domain?: DomainOut | null

  container_node?: ContainerNodeOut | null

  container_cluster?: ContainerClusterOut | null

  stack?: StackOut | null

  application?: ApplicationOut | null
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
 * EnvironmentBase
 
 */

export interface EnvironmentBase {
  id: number

  name: string

  description: string | null

  organization_id: number
}

/**
 * EnvironmentCreate
 
 */

export interface EnvironmentCreate {
  name: string

  description?: string | null

  organization_id: number
}

/**
 * EnvironmentOut
 
 */

export interface EnvironmentOut {
  id: number

  name: string

  description: string | null

  organization_id: number

  organization?: OrganizationOut | null

  elements?: ElementOut[]

  rules?: RuleOut[]

  users?: UserOut[]

  groups_with_access?: GroupOut[]

  tags?: TagOut[]

  physical_hosts?: PhysicalHostOut[]
}

/**
 * FunctionOut
 
 */

export interface FunctionOut {
  id: number

  name: string

  description: string | null
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
 * GroupOut
 
 */

export interface GroupOut {
  id: number

  name: string

  description: string | null

  tags?: TagOut[]

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
 * HealthComponents
 * Collection of system component health statuses
 */

export interface HealthComponents {
  database: ComponentHealth
}

/**
 * HealthData
 * Health check data structure
 */

export interface HealthData {
  status: string

  components: HealthComponents
}

/**
 * HealthResponse
 * Response schema for health check endpoint
 */

export interface HealthResponse {
  status: string

  message: string

  data: HealthData
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
 * NetworkOut
 
 */

export interface NetworkOut {
  id: number

  cidr: string

  vlan: number | null

  type: string

  environment_scoped: boolean

  element_id: number
}

/**
 * OrganizationCreate
 
 */

export interface OrganizationCreate {
  name: string

  description?: string | null
}

/**
 * OrganizationOut
 
 */

export interface OrganizationOut {
  name: string

  description?: string | null

  id: number

  users?: UserOut[]

  environments?: EnvironmentOut[]

  groups?: GroupOut[]

  policies?: PolicyOut[]
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
 * PhysicalHostOut
 
 */

export interface PhysicalHostOut {
  id: number

  fqdn: string

  ip_mgmt: string

  cpu_threads: number

  ram_mb: number

  hypervisor_type: HypervisorType

  is_schedulable: boolean

  allocation_mode: AllocationMode

  dedicated_environment_id?: number | null
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
 * PolicyOut
 
 */

export interface PolicyOut {
  id: number

  name: string

  description: string | null

  organization_id: number

  tags?: TagOut[]

  users?: UserOut[]

  groups?: GroupOut[]
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
 * RuleOut
 
 */

export interface RuleOut {
  id: number

  function_id: number

  environment_id: number | null

  element_id: number | null

  access_schedule: Record<string, unknown> | null
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
 * StackOut
 
 */

export interface StackOut {
  id: number

  name: string

  description: string | null

  element_id: number
}

/**
 * StoragePoolOut
 
 */

export interface StoragePoolOut {
  id: number

  type: string

  parameters: Record<string, unknown> | null

  scope: string

  element_id: number | null
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
 * VMOut
 
 */

export interface VMOut {
  id: number

  host_id: number

  name: string

  vcpu: number

  ram_mb: number

  disk_gb: number

  os_image: string

  stack_id: number | null

  element_id: number
}

/**
 * ValidationError
 
 */

export interface ValidationError {
  loc: string | number[]

  msg: string

  type: string
}

/**
 * VolumeOut
 
 */

export interface VolumeOut {
  id: number

  pool_id: number

  size_gb: number

  mode: string

  element_id: number
}
