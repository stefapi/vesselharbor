import type * as Types from './types.ts'

/**
 * Crée un nouvel utilisateur en mode libre dans le système. Le premier utilisateur créé devient automatiquement superadmin.
 * @param data Request data
 */
export async function creerunutilisateurenmodelibre(data: Types.UserCreate) {
  return api.post('/users', data)
}

/**
 * Récupère la liste des utilisateurs avec pagination et filtrage optionnel par email.
 */
export async function listerlesutilisateursusers() {
  return api.get('/users')
}

/**
 * Crée un nouvel utilisateur dans le système. Il est rattaché à une Organization
 * @param organization_id organization_id parameter
 */
export async function creerunutilisateur(organization_id: number, data: Types.UserCreate) {
  return api.post(`/users/${organization_id}`, data)
}

/**
 * Récupère les informations détaillées d'un utilisateur spécifique par son ID.
 * @param user_id user_id parameter
 */
export async function obtenirunutilisateur(user_id: number) {
  return api.get(`/users/${user_id}`)
}

/**
 * Modifie les informations personnelles d'un utilisateur existant (nom, prénom, email, username).
 * @param user_id user_id parameter
 */
export async function mettreajourlesinformationsdunutilisateur(user_id: number, data: Types.UserUpdate) {
  return api.put(`/users/${user_id}`, data)
}

/**
 * Supprime définitivement un utilisateur du système. Un utilisateur ne peut pas se supprimer lui-même, et le dernier superadmin ne peut pas être supprimé.
 * @param user_id user_id parameter
 */
export async function supprimerunutilisateur(user_id: number) {
  return api.delete(`/users/${user_id}`)
}

/**
 * Permet à un utilisateur de changer son propre mot de passe ou à un administrateur de réinitialiser le mot de passe d'un autre utilisateur.
 * @param user_id user_id parameter
 */
export async function changerlemotdepasse(user_id: number, data: Types.ChangePassword) {
  return api.put(`/users/${user_id}/password`, data)
}

/**
 * Permet à un superadmin de modifier le statut superadmin d'un autre utilisateur. Un superadmin ne peut pas modifier son propre statut, et le dernier superadmin ne peut pas être déclassé.
 * @param user_id user_id parameter
 */
export async function modifierstatutsuperadmin(user_id: number, data: Types.ChangeSuperadmin) {
  return api.put(`/users/${user_id}/superadmin`, data)
}

/**
 * Récupère la liste des groupes auxquels l'utilisateur appartient.
 * @param user_id user_id parameter
 */
export async function groupesduuser(user_id: number) {
  return api.get(`/users/${user_id}/groups`)
}

/**
 * Récupère la liste des policies directement associées à l'utilisateur.
 * @param user_id user_id parameter
 */
export async function policiesduuser(user_id: number) {
  return api.get(`/users/${user_id}/policies`)
}

/**
 * Récupère la liste des organisations auxquelles l'utilisateur est associé.
 * @param user_id user_id parameter
 */
export async function organisationsduuser(user_id: number) {
  return api.get(`/users/${user_id}/organizations`)
}

/**
 * Récupère la liste des tags associés à un utilisateur spécifique.
 * @param user_id user_id parameter
 */
export async function listerlestagsdunutilisateurusers(user_id: number) {
  return api.get(`/users/${user_id}/tags`)
}

/**
 * Ajoute un tag spécifique à un utilisateur pour le catégoriser ou lui attribuer des caractéristiques particulières.
 * @param user_id user_id parameter
 * @param tag_id tag_id parameter
 */
export async function associeruntagaunutilisateur(user_id: number, tag_id: number) {
  return api.post(`/users/${user_id}/tags/${tag_id}`)
}

/**
 * Retire un tag spécifique d'un utilisateur, supprimant ainsi la catégorisation ou les caractéristiques associées.
 * @param user_id user_id parameter
 * @param tag_id tag_id parameter
 */
export async function dissocieruntagdunutilisateur(user_id: number, tag_id: number) {
  return api.delete(`/users/${user_id}/tags/${tag_id}`)
}
