/*
 * Copyright (c) 2025.  VesselHarbor
 *
 * ____   ____                          .__    ___ ___             ___.
 * \   \ /   /____   ______ ______ ____ |  |  /   |   \_____ ______\_ |__   ___________
 *  \   Y   // __ \ /  ___//  ___// __ \|  | /    ~    \__  \\_  __ \ __ \ /  _ \_  __ \
 *   \     /\  ___/ \___ \ \___ \\  ___/|  |_\    Y    // __ \|  | \/ \_\ (  <_> )  | \/
 *    \___/  \___  >____  >____  >\___  >____/\___|_  /(____  /__|  |___  /\____/|__|
 *               \/     \/     \/     \/            \/      \/          \/
 *
 *
 * MIT License
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 *
 */

import { ref, computed, readonly, nextTick } from 'vue'
import { useEventListener } from '@vueuse/core'

/**
 * Types de modales disponibles
 */
export type ModalType = 'info' | 'success' | 'warning' | 'error' | 'confirm' | 'custom'

/**
 * Interface pour la configuration d'une modale
 */
export interface ModalConfig {
  id?: string
  type?: ModalType
  title?: string
  message?: string
  confirmText?: string
  cancelText?: string
  showCancel?: boolean
  showConfirm?: boolean
  persistent?: boolean // Ne se ferme pas en cliquant à l'extérieur
  width?: string
  maxWidth?: string
  fullscreen?: boolean
  destroyOnClose?: boolean
  beforeClose?: () => boolean | Promise<boolean>
  onConfirm?: () => void | Promise<void>
  onCancel?: () => void | Promise<void>
  onClose?: () => void | Promise<void>
}

/**
 * Interface pour une modale active
 */
export interface ActiveModal extends Required<Omit<ModalConfig, 'beforeClose' | 'onConfirm' | 'onCancel' | 'onClose'>> {
  id: string
  isVisible: boolean
  isLoading: boolean
  beforeClose?: () => boolean | Promise<boolean>
  onConfirm?: () => void | Promise<void>
  onCancel?: () => void | Promise<void>
  onClose?: () => void | Promise<void>
}

/**
 * Configuration par défaut pour les modales
 */
const defaultModalConfig: Partial<ModalConfig> = {
  type: 'custom',
  confirmText: 'Confirmer',
  cancelText: 'Annuler',
  showCancel: true,
  showConfirm: true,
  persistent: false,
  width: 'auto',
  maxWidth: '500px',
  fullscreen: false,
  destroyOnClose: true
}

/**
 * Composable pour la gestion centralisée des modales
 * Fournit un système de gestion des modales avec différents types et états globaux
 */
export function useModal() {
  // État global des modales
  const modals = ref<Map<string, ActiveModal>>(new Map())
  const modalStack = ref<string[]>([]) // Stack pour gérer l'ordre d'affichage

  // Computed properties
  const hasOpenModals = computed(() => modals.value.size > 0)
  const currentModal = computed(() => {
    const topModalId = modalStack.value[modalStack.value.length - 1]
    return topModalId ? modals.value.get(topModalId) : null
  })
  const modalCount = computed(() => modals.value.size)

  // Génère un ID unique pour une modale
  const generateModalId = (): string => {
    return `modal-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`
  }

  /**
   * Ouvre une modale avec la configuration spécifiée
   */
  const openModal = async (config: ModalConfig): Promise<string> => {
    const modalId = config.id || generateModalId()

    const modal: ActiveModal = {
      ...defaultModalConfig,
      ...config,
      id: modalId,
      isVisible: false,
      isLoading: false
    } as ActiveModal

    modals.value.set(modalId, modal)
    modalStack.value.push(modalId)

    // Attendre le prochain tick pour l'animation
    await nextTick()
    modal.isVisible = true

    return modalId
  }

  /**
   * Ferme une modale spécifique
   */
  const closeModal = async (modalId: string, force = false): Promise<boolean> => {
    const modal = modals.value.get(modalId)
    if (!modal) return false

    // Vérifier beforeClose si défini et pas forcé
    if (!force && modal.beforeClose) {
      try {
        const canClose = await modal.beforeClose()
        if (!canClose) return false
      } catch (error) {
        console.error('Erreur dans beforeClose:', error)
        return false
      }
    }

    // Masquer la modale avec animation
    modal.isVisible = false

    // Attendre l'animation avant de supprimer
    setTimeout(() => {
      modals.value.delete(modalId)
      const stackIndex = modalStack.value.indexOf(modalId)
      if (stackIndex > -1) {
        modalStack.value.splice(stackIndex, 1)
      }

      // Appeler onClose si défini
      if (modal.onClose) {
        try {
          modal.onClose()
        } catch (error) {
          console.error('Erreur dans onClose:', error)
        }
      }
    }, 300) // Durée de l'animation

    return true
  }

  /**
   * Ferme la modale actuellement au top
   */
  const closeCurrentModal = async (force = false): Promise<boolean> => {
    if (currentModal.value) {
      return await closeModal(currentModal.value.id, force)
    }
    return false
  }

  /**
   * Ferme toutes les modales
   */
  const closeAllModals = async (force = false): Promise<void> => {
    const modalIds = Array.from(modals.value.keys())

    for (const modalId of modalIds) {
      await closeModal(modalId, force)
    }
  }

  /**
   * Confirme la modale actuelle
   */
  const confirmModal = async (modalId?: string): Promise<void> => {
    const modal = modalId ? modals.value.get(modalId) : currentModal.value
    if (!modal) return

    modal.isLoading = true

    try {
      if (modal.onConfirm) {
        await modal.onConfirm()
      }
      await closeModal(modal.id)
    } catch (error) {
      console.error('Erreur lors de la confirmation:', error)
    } finally {
      modal.isLoading = false
    }
  }

  /**
   * Annule la modale actuelle
   */
  const cancelModal = async (modalId?: string): Promise<void> => {
    const modal = modalId ? modals.value.get(modalId) : currentModal.value
    if (!modal) return

    try {
      if (modal.onCancel) {
        await modal.onCancel()
      }
      await closeModal(modal.id)
    } catch (error) {
      console.error('Erreur lors de l\'annulation:', error)
    }
  }

  /**
   * Modales prédéfinies pour les cas d'usage courants
   */
  const showInfo = (title: string, message: string, config?: Partial<ModalConfig>) => {
    return openModal({
      type: 'info',
      title,
      message,
      showCancel: false,
      confirmText: 'OK',
      ...config
    })
  }

  const showSuccess = (title: string, message: string, config?: Partial<ModalConfig>) => {
    return openModal({
      type: 'success',
      title,
      message,
      showCancel: false,
      confirmText: 'OK',
      ...config
    })
  }

  const showWarning = (title: string, message: string, config?: Partial<ModalConfig>) => {
    return openModal({
      type: 'warning',
      title,
      message,
      showCancel: false,
      confirmText: 'OK',
      ...config
    })
  }

  const showError = (title: string, message: string, config?: Partial<ModalConfig>) => {
    return openModal({
      type: 'error',
      title,
      message,
      showCancel: false,
      confirmText: 'OK',
      ...config
    })
  }

  const showConfirm = (
    title: string,
    message: string,
    onConfirm?: () => void | Promise<void>,
    config?: Partial<ModalConfig>
  ) => {
    return openModal({
      type: 'confirm',
      title,
      message,
      onConfirm,
      ...config
    })
  }

  /**
   * Utilitaire pour créer une modale de confirmation avec Promise
   */
  const confirmDialog = (title: string, message: string, config?: Partial<ModalConfig>): Promise<boolean> => {
    return new Promise((resolve) => {
      openModal({
        type: 'confirm',
        title,
        message,
        onConfirm: () => resolve(true),
        onCancel: () => resolve(false),
        onClose: () => resolve(false),
        ...config
      })
    })
  }

  /**
   * Met à jour la configuration d'une modale existante
   */
  const updateModal = (modalId: string, updates: Partial<ModalConfig>): boolean => {
    const modal = modals.value.get(modalId)
    if (!modal) return false

    Object.assign(modal, updates)
    return true
  }

  /**
   * Vérifie si une modale spécifique est ouverte
   */
  const isModalOpen = (modalId: string): boolean => {
    return modals.value.has(modalId)
  }

  /**
   * Récupère une modale par son ID
   */
  const getModal = (modalId: string): ActiveModal | undefined => {
    return modals.value.get(modalId)
  }

  // Gestion des touches clavier (ESC pour fermer)
  useEventListener('keydown', (event: KeyboardEvent) => {
    if (event.key === 'Escape' && currentModal.value && !currentModal.value.persistent) {
      cancelModal()
    }
  })

  return {
    // État (readonly pour éviter les modifications directes)
    modals: readonly(modals),
    modalStack: readonly(modalStack),

    // Computed properties
    hasOpenModals,
    currentModal,
    modalCount,

    // Actions principales
    openModal,
    closeModal,
    closeCurrentModal,
    closeAllModals,
    confirmModal,
    cancelModal,

    // Modales prédéfinies
    showInfo,
    showSuccess,
    showWarning,
    showError,
    showConfirm,
    confirmDialog,

    // Utilitaires
    updateModal,
    isModalOpen,
    getModal
  }
}

/**
 * Instance globale du gestionnaire de modales
 * Permet d'utiliser les modales depuis n'importe où dans l'application
 */
export const globalModal = useModal()
