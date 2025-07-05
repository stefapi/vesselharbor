import type * as Types from './types.ts'

/**
 * Authentifie un utilisateur avec son email et mot de passe et retourne un token d'accès
 */
export async function authentifierunutilisateur() {
  return api.post('/login')
}

/**
 * Déconnecte l'utilisateur en supprimant les cookies d'authentification
 */
export async function sedeconnecter() {
  return api.post('/logout')
}

/**
 * Renouvelle le token d'accès à partir d'un refresh token valide
 */
export async function renouvelerletoken() {
  return api.post('/refresh-token')
}

/**
 * Récupère les informations du profil de l'utilisateur actuellement connecté
 */
export async function profilutilisateurconnecte() {
  return api.get('/me')
}

/**
 * Envoie un email contenant un lien de réinitialisation de mot de passe à l'adresse email fournie
 * @param data Request data
 */
export async function demanderunereinitialisationdemotdepasse(data: Types.PasswordResetRequest) {
  return api.post('/users/reset_password_request', data)
}

/**
 * Réinitialise le mot de passe d'un utilisateur à l'aide d'un token de réinitialisation valide
 * @param data Request data
 */
export async function reinitialiserlemotdepasse(data: Types.PasswordReset) {
  return api.post('/users/reset_password', data)
}
