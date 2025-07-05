import type * as Types from './types.ts'

/**
 * Lists environments filtered by name or organization (superadmins see everything, others only what they have permission to read).
 */
export async function listenvironments() {
  return api.get('/environments')
}

/**
 * Creates an environment attached to an organization. Assigns an admin policy to the creator if needed.
 * @param data Request data
 */
export async function createanenvironment(data: Types.EnvironmentCreate) {
  return api.post('/environments', data)
}

/**
 * Returns environment details if the user has access.
 * @param environment_id environment_id parameter
 */
export async function environmentdetails(environment_id: number) {
  return api.get(`/environments/${environment_id}`)
}

/**
 * Updates an environment if it exists and the user has permission.
 * @param environment_id environment_id parameter
 */
export async function updateanenvironment(environment_id: number, data: Types.EnvironmentCreate) {
  return api.put(`/environments/${environment_id}`, data)
}

/**
 * Deletes an environment if the user has the required permissions.
 * @param environment_id environment_id parameter
 */
export async function deleteanenvironment(environment_id: number) {
  return api.delete(`/environments/${environment_id}`)
}

/**
 * Returns the list of physical hosts associated with an environment if the user has access to it.
 * @param environment_id environment_id parameter
 */
export async function listphysicalhostsofanenvironmentenvironments(environment_id: number) {
  return api.get(`/environments/${environment_id}/physical-hosts`)
}

/**
 * Generates a unique name from an animal or an adjective.
 */
export async function generatearandomname() {
  return api.get('/environments/generate-name')
}

/**
 * Returns all users who have access to an environment via a policy (via rules).
 * @param environment_id environment_id parameter
 */
export async function userslinkedtoanenvironment(environment_id: number) {
  return api.get(`/environments/${environment_id}/users`)
}

/**
 * Lists the elements of an environment with pagination and filtering by name and type.
 * @param environment_id environment_id parameter
 */
export async function listelementsofanenvironmentenvironments(environment_id: number) {
  return api.get(`/environments/${environment_id}/elements`)
}

/**
 * Retrieves all tags associated with an environment.
 * @param environment_id environment_id parameter
 */
export async function listenvironmenttagsenvironments(environment_id: number) {
  return api.get(`/environments/${environment_id}/tags`)
}

/**
 * Associates an existing tag with an environment.
 * @param environment_id environment_id parameter
 * @param tag_id tag_id parameter
 */
export async function addatagtoanenvironment(environment_id: number, tag_id: number) {
  return api.post(`/environments/${environment_id}/tags/${tag_id}`)
}

/**
 * Removes association between a tag and an environment.
 * @param environment_id environment_id parameter
 * @param tag_id tag_id parameter
 */
export async function removeatagfromanenvironment(environment_id: number, tag_id: number) {
  return api.delete(`/environments/${environment_id}/tags/${tag_id}`)
}

/**
 * Lists network-type elements in an environment with pagination and name filtering.
 * @param environment_id environment_id parameter
 */
export async function listnetworksofanenvironmentenvironments(environment_id: number) {
  return api.get(`/environments/${environment_id}/networks`)
}

/**
 * Lists virtual machine-type elements in an environment with pagination and name filtering.
 * @param environment_id environment_id parameter
 */
export async function listvirtualmachinesofanenvironmentenvironments(environment_id: number) {
  return api.get(`/environments/${environment_id}/vms`)
}

/**
 * Lists storage pool-type elements in an environment with pagination and name filtering.
 * @param environment_id environment_id parameter
 */
export async function liststoragepoolsofanenvironmentenvironments(environment_id: number) {
  return api.get(`/environments/${environment_id}/storage-pools`)
}

/**
 * Lists volume-type elements in an environment with pagination and name filtering.
 * @param environment_id environment_id parameter
 */
export async function listvolumesofanenvironmentenvironments(environment_id: number) {
  return api.get(`/environments/${environment_id}/volumes`)
}

/**
 * Lists domain-type elements in an environment with pagination and name filtering.
 * @param environment_id environment_id parameter
 */
export async function listdomainsofanenvironmentenvironments(environment_id: number) {
  return api.get(`/environments/${environment_id}/domains`)
}

/**
 * Lists container node-type elements in an environment with pagination and name filtering.
 * @param environment_id environment_id parameter
 */
export async function listcontainernodesofanenvironmentenvironments(environment_id: number) {
  return api.get(`/environments/${environment_id}/container-nodes`)
}

/**
 * Lists container cluster-type elements in an environment with pagination and name filtering.
 * @param environment_id environment_id parameter
 */
export async function listcontainerclustersofanenvironmentenvironments(environment_id: number) {
  return api.get(`/environments/${environment_id}/container-clusters`)
}

/**
 * Lists stack-type elements in an environment with pagination and name filtering.
 * @param environment_id environment_id parameter
 */
export async function liststacksofanenvironmentenvironments(environment_id: number) {
  return api.get(`/environments/${environment_id}/stacks`)
}

/**
 * Lists application-type elements in an environment with pagination and name filtering.
 * @param environment_id environment_id parameter
 */
export async function listapplicationsofanenvironmentenvironments(environment_id: number) {
  return api.get(`/environments/${environment_id}/applications`)
}
