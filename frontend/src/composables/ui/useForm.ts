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

import { ref, computed, readonly, reactive, watch, nextTick } from 'vue'
import { useAsyncState } from '@vueuse/core'

/**
 * Type pour une règle de validation
 */
export type ValidationRule<T = any> = {
  required?: boolean
  message?: string
  validator?: (value: T, formData: Record<string, any>) => boolean | string | Promise<boolean | string>
  trigger?: 'blur' | 'change' | 'submit'
}

/**
 * Interface pour l'état d'un champ
 */
export interface FieldState {
  value: any
  error: string | null
  touched: boolean
  dirty: boolean
  validating: boolean
}

/**
 * Interface pour la configuration d'un champ
 */
export interface FieldConfig {
  initialValue?: any
  rules?: ValidationRule[]
  transform?: (value: any) => any // Transformation de la valeur avant validation
}

/**
 * Interface pour la configuration du formulaire
 */
export interface FormConfig<T = Record<string, any>> {
  initialValues?: Partial<T>
  validateOnChange?: boolean
  validateOnBlur?: boolean
  resetOnSubmit?: boolean
  onSubmit?: (values: T) => void | Promise<void>
  onError?: (errors: Record<string, string>) => void
  onReset?: () => void
}

/**
 * Composable pour la gestion des formulaires avec validation
 * Fournit une logique réutilisable pour la gestion des formulaires, validation et soumission
 */
export function useForm<T extends Record<string, any> = Record<string, any>>(
  fields: Record<keyof T, FieldConfig>,
  config: FormConfig<T> = {}
) {
  const {
    initialValues = {},
    validateOnChange = true,
    validateOnBlur = true,
    resetOnSubmit = false,
    onSubmit,
    onError,
    onReset
  } = config

  // État des champs
  const fieldStates = reactive<Record<keyof T, FieldState>>({} as Record<keyof T, FieldState>)

  // État global du formulaire
  const isSubmitting = ref(false)
  const submitCount = ref(0)
  const hasBeenSubmitted = computed(() => submitCount.value > 0)

  // Initialiser les champs
  Object.keys(fields).forEach((fieldName) => {
    const fieldConfig = fields[fieldName as keyof T]
    const initialValue = initialValues[fieldName as keyof T] ?? fieldConfig.initialValue ?? ''

    fieldStates[fieldName as keyof T] = reactive({
      value: initialValue,
      error: null,
      touched: false,
      dirty: false,
      validating: false
    })
  })

  // Computed properties
  const values = computed(() => {
    const result = {} as T
    Object.keys(fieldStates).forEach((fieldName) => {
      result[fieldName as keyof T] = fieldStates[fieldName as keyof T].value
    })
    return result
  })

  const errors = computed(() => {
    const result: Record<string, string> = {}
    Object.keys(fieldStates).forEach((fieldName) => {
      const error = fieldStates[fieldName as keyof T].error
      if (error) {
        result[fieldName] = error
      }
    })
    return result
  })

  const isValid = computed(() => Object.keys(errors.value).length === 0)

  const isDirty = computed(() =>
    Object.values(fieldStates).some(field => field.dirty)
  )

  const isTouched = computed(() =>
    Object.values(fieldStates).some(field => field.touched)
  )

  const isValidating = computed(() =>
    Object.values(fieldStates).some(field => field.validating)
  )

  /**
   * Valide un champ spécifique
   */
  const validateField = async (fieldName: keyof T): Promise<boolean> => {
    const fieldState = fieldStates[fieldName]
    const fieldConfig = fields[fieldName]

    if (!fieldState || !fieldConfig.rules) return true

    fieldState.validating = true
    fieldState.error = null

    try {
      const value = fieldConfig.transform ? fieldConfig.transform(fieldState.value) : fieldState.value

      for (const rule of fieldConfig.rules) {
        // Validation required
        if (rule.required && (value === null || value === undefined || value === '')) {
          fieldState.error = rule.message || `${String(fieldName)} est requis`
          return false
        }

        // Validation personnalisée
        if (rule.validator && value !== null && value !== undefined && value !== '') {
          const result = await rule.validator(value, values.value)

          if (result === false) {
            fieldState.error = rule.message || `${String(fieldName)} n'est pas valide`
            return false
          } else if (typeof result === 'string') {
            fieldState.error = result
            return false
          }
        }
      }

      return true
    } catch (error) {
      fieldState.error = error instanceof Error ? error.message : 'Erreur de validation'
      return false
    } finally {
      fieldState.validating = false
    }
  }

  /**
   * Valide tous les champs du formulaire
   */
  const validateForm = async (): Promise<boolean> => {
    const validationPromises = Object.keys(fieldStates).map(fieldName =>
      validateField(fieldName as keyof T)
    )

    const results = await Promise.all(validationPromises)
    return results.every(result => result)
  }

  /**
   * Met à jour la valeur d'un champ
   */
  const setFieldValue = async (fieldName: keyof T, value: any, shouldValidate = validateOnChange) => {
    const fieldState = fieldStates[fieldName]
    if (!fieldState) return

    const oldValue = fieldState.value
    fieldState.value = value
    fieldState.dirty = fieldState.dirty || value !== (initialValues[fieldName] ?? fields[fieldName].initialValue ?? '')

    if (shouldValidate && fieldState.touched) {
      await validateField(fieldName)
    }
  }

  /**
   * Marque un champ comme touché
   */
  const setFieldTouched = async (fieldName: keyof T, shouldValidate = validateOnBlur) => {
    const fieldState = fieldStates[fieldName]
    if (!fieldState) return

    fieldState.touched = true

    if (shouldValidate) {
      await validateField(fieldName)
    }
  }

  /**
   * Définit une erreur pour un champ
   */
  const setFieldError = (fieldName: keyof T, error: string | null) => {
    const fieldState = fieldStates[fieldName]
    if (fieldState) {
      fieldState.error = error
    }
  }

  /**
   * Efface l'erreur d'un champ
   */
  const clearFieldError = (fieldName: keyof T) => {
    setFieldError(fieldName, null)
  }

  /**
   * Efface toutes les erreurs
   */
  const clearErrors = () => {
    Object.keys(fieldStates).forEach(fieldName => {
      clearFieldError(fieldName as keyof T)
    })
  }

  /**
   * Réinitialise un champ à sa valeur initiale
   */
  const resetField = (fieldName: keyof T) => {
    const fieldState = fieldStates[fieldName]
    const fieldConfig = fields[fieldName]

    if (fieldState) {
      fieldState.value = initialValues[fieldName] ?? fieldConfig.initialValue ?? ''
      fieldState.error = null
      fieldState.touched = false
      fieldState.dirty = false
      fieldState.validating = false
    }
  }

  /**
   * Réinitialise tout le formulaire
   */
  const resetForm = () => {
    Object.keys(fieldStates).forEach(fieldName => {
      resetField(fieldName as keyof T)
    })

    submitCount.value = 0

    if (onReset) {
      onReset()
    }
  }

  /**
   * Définit les valeurs de plusieurs champs
   */
  const setValues = async (newValues: Partial<T>, shouldValidate = false) => {
    const promises = Object.entries(newValues).map(([fieldName, value]) =>
      setFieldValue(fieldName as keyof T, value, shouldValidate)
    )

    await Promise.all(promises)
  }

  /**
   * Définit les erreurs de plusieurs champs
   */
  const setErrors = (newErrors: Partial<Record<keyof T, string>>) => {
    Object.entries(newErrors).forEach(([fieldName, error]) => {
      setFieldError(fieldName as keyof T, error as string)
    })
  }

  /**
   * Soumet le formulaire
   */
  const { execute: submitForm, isLoading: isSubmittingAsync } = useAsyncState(
    async () => {
      submitCount.value++

      // Marquer tous les champs comme touchés
      Object.keys(fieldStates).forEach(fieldName => {
        fieldStates[fieldName as keyof T].touched = true
      })

      // Valider le formulaire
      const isFormValid = await validateForm()

      if (!isFormValid) {
        if (onError) {
          onError(errors.value)
        }
        throw new Error('Formulaire invalide')
      }

      // Soumettre si valide
      if (onSubmit) {
        await onSubmit(values.value)
      }

      // Réinitialiser si configuré
      if (resetOnSubmit) {
        resetForm()
      }

      return values.value
    },
    null,
    { immediate: false }
  )

  // Surveiller les changements pour la validation automatique
  if (validateOnChange) {
    Object.keys(fieldStates).forEach(fieldName => {
      watch(
        () => fieldStates[fieldName as keyof T].value,
        () => {
          if (fieldStates[fieldName as keyof T].touched) {
            validateField(fieldName as keyof T)
          }
        }
      )
    })
  }

  /**
   * Utilitaires pour créer des handlers d'événements
   */
  const createFieldHandlers = (fieldName: keyof T) => ({
    onChange: (value: any) => setFieldValue(fieldName, value),
    onBlur: () => setFieldTouched(fieldName),
    onFocus: () => {
      // Optionnel: effacer l'erreur au focus
      if (fieldStates[fieldName].error) {
        clearFieldError(fieldName)
      }
    }
  })

  /**
   * Récupère l'état d'un champ
   */
  const getFieldState = (fieldName: keyof T) => {
    return fieldStates[fieldName] ? readonly(fieldStates[fieldName]) : null
  }

  /**
   * Récupère la valeur d'un champ
   */
  const getFieldValue = (fieldName: keyof T) => {
    return fieldStates[fieldName]?.value
  }

  /**
   * Récupère l'erreur d'un champ
   */
  const getFieldError = (fieldName: keyof T) => {
    return fieldStates[fieldName]?.error
  }

  return {
    // État (readonly pour éviter les modifications directes)
    values: readonly(values),
    errors: readonly(errors),
    isSubmitting: readonly(ref(isSubmittingAsync.value || isSubmitting.value)),
    submitCount: readonly(submitCount),

    // Computed properties
    isValid,
    isDirty,
    isTouched,
    isValidating,
    hasBeenSubmitted,

    // Actions pour les champs
    setFieldValue,
    setFieldTouched,
    setFieldError,
    clearFieldError,
    resetField,
    getFieldState,
    getFieldValue,
    getFieldError,
    createFieldHandlers,

    // Actions pour le formulaire
    validateField,
    validateForm,
    setValues,
    setErrors,
    clearErrors,
    resetForm,
    submitForm,

    // État des champs (pour accès direct si nécessaire)
    fieldStates: readonly(fieldStates)
  }
}

/**
 * Règles de validation prédéfinies
 */
export const validationRules = {
  required: (message = 'Ce champ est requis'): ValidationRule => ({
    required: true,
    message
  }),

  email: (message = 'Adresse email invalide'): ValidationRule => ({
    validator: (value: string) => {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
      return emailRegex.test(value)
    },
    message
  }),

  minLength: (min: number, message?: string): ValidationRule => ({
    validator: (value: string) => value.length >= min,
    message: message || `Minimum ${min} caractères requis`
  }),

  maxLength: (max: number, message?: string): ValidationRule => ({
    validator: (value: string) => value.length <= max,
    message: message || `Maximum ${max} caractères autorisés`
  }),

  pattern: (regex: RegExp, message = 'Format invalide'): ValidationRule => ({
    validator: (value: string) => regex.test(value),
    message
  }),

  numeric: (message = 'Doit être un nombre'): ValidationRule => ({
    validator: (value: any) => !isNaN(Number(value)),
    message
  }),

  min: (min: number, message?: string): ValidationRule => ({
    validator: (value: number) => Number(value) >= min,
    message: message || `La valeur doit être supérieure ou égale à ${min}`
  }),

  max: (max: number, message?: string): ValidationRule => ({
    validator: (value: number) => Number(value) <= max,
    message: message || `La valeur doit être inférieure ou égale à ${max}`
  }),

  confirm: (fieldName: string, message?: string): ValidationRule => ({
    validator: (value: any, formData: Record<string, any>) => {
      return value === formData[fieldName]
    },
    message: message || 'Les valeurs ne correspondent pas'
  })
}
