import type * as Types from './types.ts'

/**
 * Creates an element in a given environment.
 * @param environment_id environment_id parameter
 */
export async function createanelement(environment_id: number, data: Types.ElementCreate) {
  return api.post(`/elements/${environment_id}`, data)
}

/**
 * Returns information about a specific element.
 * @param element_id element_id parameter
 */
export async function getanelementelements(element_id: number) {
  return api.get(`/elements/${element_id}`)
}

/**
 * Modifies the information of an element.
 * @param element_id element_id parameter
 */
export async function updateanelement(element_id: number, data: Types.ElementUpdate) {
  return api.put(`/elements/${element_id}`, data)
}

/**
 * Deletes a given element.
 * @param element_id element_id parameter
 */
export async function deleteanelement(element_id: number) {
  return api.delete(`/elements/${element_id}`)
}

/**
 * Retrieves all tags associated with an element.
 * @param element_id element_id parameter
 */
export async function listelementtagselements(element_id: number) {
  return api.get(`/elements/${element_id}/tags`)
}

/**
 * Associates an existing tag with an element.
 * @param element_id element_id parameter
 * @param tag_id tag_id parameter
 */
export async function addatagtoanelement(element_id: number, tag_id: number) {
  return api.post(`/elements/${element_id}/tags/${tag_id}`)
}

/**
 * Removes the association between a tag and an element.
 * @param element_id element_id parameter
 * @param tag_id tag_id parameter
 */
export async function removeatagfromanelement(element_id: number, tag_id: number) {
  return api.delete(`/elements/${element_id}/tags/${tag_id}`)
}
