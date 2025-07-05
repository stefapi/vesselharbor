import api from '@/services/api.ts';
import type { ElementListParams } from '@/types/api';

/**
 * Crée un nouvel élément dans l'environnement spécifié.
 * @param environmentId L'identifiant de l'environnement.
 * @param element Les données de l'élément (nom, description, etc.).
 */
export async function createElement(environmentId: number, element: { name: string; description: string }) {
  return api.post(`/elements/${environmentId}`, element);
}

/**
 * Récupère la liste des éléments d'un environnement.
 * @param environmentId L'identifiant de l'environnement.
 * @param params Paramètres optionnels pour filtrer ou paginer la liste.
 */
export async function listElements(environmentId: number, params: ElementListParams = {}) {
  return api.get(`/elements/environment/${environmentId}`, { params });
}

/**
 * Récupère les détails d'un élément spécifique.
 * @param elementId L'identifiant de l'élément.
 */
export async function getElement(elementId: number) {
  return api.get(`/elements/${elementId}`);
}

/**
 * Met à jour un élément existant.
 * @param elementId L'identifiant de l'élément à mettre à jour.
 * @param element Les nouvelles données de l'élément.
 */
export async function updateElement(elementId: number, element: { name: string; description: string }) {
  return api.put(`/elements/${elementId}`, element);
}

/**
 * Supprime un élément.
 * @param elementId L'identifiant de l'élément à supprimer.
 */
export async function deleteElement(elementId: number) {
  return api.delete(`/elements/${elementId}`);
}
