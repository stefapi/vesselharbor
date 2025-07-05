import type * as Types from './types.ts'

/**
 * Liste les environnements filtrés par nom ou organisation (superadmins voient tout, les autres uniquement ce qu'ils ont le droit de lire).
 */
export async function listerlesenvironnementsenvironments() {
  return api.get('/environments')
}

/**
 * Crée un environnement rattaché à une organisation. Associe une policy d’admin au créateur si nécessaire.
 * @param data Request data
 */
export async function creerunenvironnement(data: Types.EnvironmentCreate) {
  return api.post('/environments', data)
}

/**
 * Renvoie les détails d’un environnement si l’utilisateur y a accès.
 * @param environment_id environment_id parameter
 */
export async function detaildunenvironnement(environment_id: number) {
  return api.get(`/environments/${environment_id}`)
}

/**
 * Met à jour un environnement s’il existe et si l’utilisateur a les droits.
 * @param environment_id environment_id parameter
 */
export async function mettreajourunenvironnement(environment_id: number, data: Types.EnvironmentCreate) {
  return api.put(`/environments/${environment_id}`, data)
}

/**
 * Supprime un environnement si l’utilisateur a les droits requis.
 * @param environment_id environment_id parameter
 */
export async function supprimerunenvironnement(environment_id: number) {
  return api.delete(`/environments/${environment_id}`)
}

/**
 * Renvoie la liste des hôtes physiques associés à un environnement si l'utilisateur y a accès.
 * @param environment_id environment_id parameter
 */
export async function listedeshotesphysiquesdunenvironnementenvironments(environment_id: number) {
  return api.get(`/environments/${environment_id}/physical-hosts`)
}

/**
 * Génère un nom unique à partir d'un animal ou d'un adjectif.
 */
export async function genererunnomaleatoire() {
  return api.get('/environments/generate-name')
}

/**
 * Renvoie tous les utilisateurs ayant accès à un environnement via une policy (via les rules).
 * @param environment_id environment_id parameter
 */
export async function utilisateursliesaunenvironnement(environment_id: number) {
  return api.get(`/environments/${environment_id}/users`)
}

/**
 * Liste les éléments d'un environnement avec pagination et filtrage par nom et type.
 * @param environment_id environment_id parameter
 */
export async function listerleselementsdunenvironnementenvironments(environment_id: number) {
  return api.get(`/environments/${environment_id}/elements`)
}

/**
 * Récupère tous les tags associés à un environnement.
 * @param environment_id environment_id parameter
 */
export async function listerlestagsdunenvironnementenvironments(environment_id: number) {
  return api.get(`/environments/${environment_id}/tags`)
}

/**
 * Associe un tag existant à un environnement.
 * @param environment_id environment_id parameter
 * @param tag_id tag_id parameter
 */
export async function ajouteruntagaunenvironnement(environment_id: number, tag_id: number) {
  return api.post(`/environments/${environment_id}/tags/${tag_id}`)
}

/**
 * Retire l'association entre un tag et un environnement.
 * @param environment_id environment_id parameter
 * @param tag_id tag_id parameter
 */
export async function retireruntagdunenvironnement(environment_id: number, tag_id: number) {
  return api.delete(`/environments/${environment_id}/tags/${tag_id}`)
}

/**
 * Liste les éléments de type réseau dans un environnement avec pagination et filtrage par nom.
 * @param environment_id environment_id parameter
 */
export async function listerlesreseauxdunenvironnementenvironments(environment_id: number) {
  return api.get(`/environments/${environment_id}/networks`)
}

/**
 * Liste les éléments de type machine virtuelle dans un environnement avec pagination et filtrage par nom.
 * @param environment_id environment_id parameter
 */
export async function listerlesmachinesvirtuellesdunenvironnementenvironments(environment_id: number) {
  return api.get(`/environments/${environment_id}/vms`)
}

/**
 * Liste les éléments de type pool de stockage dans un environnement avec pagination et filtrage par nom.
 * @param environment_id environment_id parameter
 */
export async function listerlespoolsdestockagedunenvironnementenvironments(environment_id: number) {
  return api.get(`/environments/${environment_id}/storage-pools`)
}

/**
 * Liste les éléments de type volume dans un environnement avec pagination et filtrage par nom.
 * @param environment_id environment_id parameter
 */
export async function listerlesvolumesdunenvironnementenvironments(environment_id: number) {
  return api.get(`/environments/${environment_id}/volumes`)
}

/**
 * Liste les éléments de type domaine dans un environnement avec pagination et filtrage par nom.
 * @param environment_id environment_id parameter
 */
export async function listerlesdomainesdunenvironnementenvironments(environment_id: number) {
  return api.get(`/environments/${environment_id}/domains`)
}

/**
 * Liste les éléments de type noeud de conteneur dans un environnement avec pagination et filtrage par nom.
 * @param environment_id environment_id parameter
 */
export async function listerlesnoeudsdeconteneurdunenvironnementenvironments(environment_id: number) {
  return api.get(`/environments/${environment_id}/container-nodes`)
}

/**
 * Liste les éléments de type cluster de conteneur dans un environnement avec pagination et filtrage par nom.
 * @param environment_id environment_id parameter
 */
export async function listerlesclustersdeconteneurdunenvironnementenvironments(environment_id: number) {
  return api.get(`/environments/${environment_id}/container-clusters`)
}

/**
 * Liste les éléments de type stack dans un environnement avec pagination et filtrage par nom.
 * @param environment_id environment_id parameter
 */
export async function listerlesstacksdunenvironnementenvironments(environment_id: number) {
  return api.get(`/environments/${environment_id}/stacks`)
}

/**
 * Liste les éléments de type application dans un environnement avec pagination et filtrage par nom.
 * @param environment_id environment_id parameter
 */
export async function listerlesapplicationsdunenvironnementenvironments(environment_id: number) {
  return api.get(`/environments/${environment_id}/applications`)
}
