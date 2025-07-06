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

import { ref, computed, readonly } from 'vue'

/**
 * Interface pour un résultat de validation
 */
export interface ValidationResult {
  isValid: boolean
  errors: string[]
  warnings?: string[]
}

/**
 * Interface pour une règle de validation métier
 */
export interface BusinessValidationRule<T = any> {
  name: string
  description?: string
  validator: (value: T, context?: ValidationContext) => ValidationResult | Promise<ValidationResult>
  severity?: 'error' | 'warning'
}

/**
 * Interface pour le contexte de validation
 */
export interface ValidationContext {
  user?: any
  organization?: any
  environment?: any
  existingData?: any
  [key: string]: any
}

/**
 * Interface pour les contraintes de nommage
 */
export interface NamingConstraints {
  minLength?: number
  maxLength?: number
  allowedCharacters?: RegExp
  forbiddenWords?: string[]
  mustStartWith?: string
  mustEndWith?: string
  caseSensitive?: boolean
}

/**
 * Composable pour la validation métier
 * Fournit des règles de validation spécifiques au domaine métier de VesselHarbor
 */
export function useValidation() {
  // État réactif
  const validationCache = ref<Map<string, ValidationResult>>(new Map())
  const loading = ref(false)
  const error = ref<string | null>(null)

  // Computed properties
  const cacheSize = computed(() => validationCache.value.size)

  /**
   * Valide une valeur selon une règle spécifique
   */
  const validateWithRule = async <T>(
    value: T,
    rule: BusinessValidationRule<T>,
    context?: ValidationContext
  ): Promise<ValidationResult> => {
    try {
      const result = await rule.validator(value, context)
      return result
    } catch (err) {
      return {
        isValid: false,
        errors: [err instanceof Error ? err.message : 'Erreur de validation']
      }
    }
  }

  /**
   * Valide une valeur selon plusieurs règles
   */
  const validateWithRules = async <T>(
    value: T,
    rules: BusinessValidationRule<T>[],
    context?: ValidationContext
  ): Promise<ValidationResult> => {
    const results = await Promise.all(
      rules.map(rule => validateWithRule(value, rule, context))
    )

    const allErrors = results.flatMap(result => result.errors)
    const allWarnings = results.flatMap(result => result.warnings || [])
    const isValid = results.every(result => result.isValid)

    return {
      isValid,
      errors: allErrors,
      warnings: allWarnings.length > 0 ? allWarnings : undefined
    }
  }

  /**
   * Règles de validation pour les noms d'organisation
   */
  const validateOrganizationName = (constraints: NamingConstraints = {}): BusinessValidationRule<string> => ({
    name: 'organization-name',
    description: 'Validation du nom d\'organisation',
    validator: (name: string) => {
      const errors: string[] = []
      const {
        minLength = 2,
        maxLength = 50,
        allowedCharacters = /^[a-zA-Z0-9\s\-_]+$/,
        forbiddenWords = ['admin', 'root', 'system', 'api'],
        caseSensitive = false
      } = constraints

      // Vérification de la longueur
      if (name.length < minLength) {
        errors.push(`Le nom doit contenir au moins ${minLength} caractères`)
      }
      if (name.length > maxLength) {
        errors.push(`Le nom ne peut pas dépasser ${maxLength} caractères`)
      }

      // Vérification des caractères autorisés
      if (!allowedCharacters.test(name)) {
        errors.push('Le nom contient des caractères non autorisés')
      }

      // Vérification des mots interdits
      const nameToCheck = caseSensitive ? name : name.toLowerCase()
      const hasForbiddenWord = forbiddenWords.some(word =>
        nameToCheck.includes(caseSensitive ? word : word.toLowerCase())
      )
      if (hasForbiddenWord) {
        errors.push('Le nom contient des mots réservés')
      }

      // Vérification des espaces en début/fin
      if (name.trim() !== name) {
        errors.push('Le nom ne peut pas commencer ou finir par des espaces')
      }

      return {
        isValid: errors.length === 0,
        errors
      }
    }
  })

  /**
   * Règles de validation pour les noms d'environnement
   */
  const validateEnvironmentName = (constraints: NamingConstraints = {}): BusinessValidationRule<string> => ({
    name: 'environment-name',
    description: 'Validation du nom d\'environnement',
    validator: (name: string) => {
      const errors: string[] = []
      const {
        minLength = 2,
        maxLength = 30,
        allowedCharacters = /^[a-zA-Z0-9\-_]+$/,
        forbiddenWords = ['prod', 'production', 'staging', 'dev', 'development', 'test']
      } = constraints

      // Vérifications similaires à l'organisation mais plus strictes
      if (name.length < minLength) {
        errors.push(`Le nom doit contenir au moins ${minLength} caractères`)
      }
      if (name.length > maxLength) {
        errors.push(`Le nom ne peut pas dépasser ${maxLength} caractères`)
      }

      if (!allowedCharacters.test(name)) {
        errors.push('Le nom ne peut contenir que des lettres, chiffres, tirets et underscores')
      }

      // Vérification que le nom ne commence pas par un chiffre
      if (/^\d/.test(name)) {
        errors.push('Le nom ne peut pas commencer par un chiffre')
      }

      return {
        isValid: errors.length === 0,
        errors
      }
    }
  })

  /**
   * Règles de validation pour les adresses email d'entreprise
   */
  const validateBusinessEmail = (): BusinessValidationRule<string> => ({
    name: 'business-email',
    description: 'Validation d\'email professionnel',
    validator: (email: string) => {
      const errors: string[] = []
      const warnings: string[] = []

      // Validation email basique
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
      if (!emailRegex.test(email)) {
        errors.push('Format d\'email invalide')
        return { isValid: false, errors }
      }

      // Domaines personnels à éviter
      const personalDomains = [
        'gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com',
        'free.fr', 'orange.fr', 'wanadoo.fr', 'laposte.net'
      ]

      const domain = email.split('@')[1]?.toLowerCase()
      if (personalDomains.includes(domain)) {
        warnings.push('Il est recommandé d\'utiliser une adresse email professionnelle')
      }

      // Vérification de domaines suspects
      const suspiciousDomains = ['tempmail', '10minutemail', 'guerrillamail']
      if (suspiciousDomains.some(suspicious => domain.includes(suspicious))) {
        errors.push('Les adresses email temporaires ne sont pas autorisées')
      }

      return {
        isValid: errors.length === 0,
        errors,
        warnings: warnings.length > 0 ? warnings : undefined
      }
    }
  })

  /**
   * Règles de validation pour les mots de passe sécurisés
   */
  const validateSecurePassword = (): BusinessValidationRule<string> => ({
    name: 'secure-password',
    description: 'Validation de mot de passe sécurisé',
    validator: (password: string) => {
      const errors: string[] = []
      const warnings: string[] = []

      // Longueur minimale
      if (password.length < 12) {
        errors.push('Le mot de passe doit contenir au moins 12 caractères')
      }

      // Complexité
      const hasLowercase = /[a-z]/.test(password)
      const hasUppercase = /[A-Z]/.test(password)
      const hasNumbers = /\d/.test(password)
      const hasSpecialChars = /[!@#$%^&*(),.?":{}|<>]/.test(password)

      if (!hasLowercase) errors.push('Le mot de passe doit contenir au moins une minuscule')
      if (!hasUppercase) errors.push('Le mot de passe doit contenir au moins une majuscule')
      if (!hasNumbers) errors.push('Le mot de passe doit contenir au moins un chiffre')
      if (!hasSpecialChars) errors.push('Le mot de passe doit contenir au moins un caractère spécial')

      // Patterns à éviter
      const commonPatterns = [
        /123456/, /password/, /admin/, /qwerty/, /azerty/,
        /(.)\1{3,}/, // Répétition de caractères
        /012345/, /abcdef/
      ]

      const hasCommonPattern = commonPatterns.some(pattern => pattern.test(password.toLowerCase()))
      if (hasCommonPattern) {
        errors.push('Le mot de passe contient des séquences trop simples')
      }

      // Avertissements pour améliorer la sécurité
      if (password.length < 16) {
        warnings.push('Un mot de passe de 16 caractères ou plus est recommandé')
      }

      return {
        isValid: errors.length === 0,
        errors,
        warnings: warnings.length > 0 ? warnings : undefined
      }
    }
  })

  /**
   * Règles de validation pour les ports réseau
   */
  const validateNetworkPort = (): BusinessValidationRule<number> => ({
    name: 'network-port',
    description: 'Validation de port réseau',
    validator: (port: number) => {
      const errors: string[] = []
      const warnings: string[] = []

      // Plage valide
      if (port < 1 || port > 65535) {
        errors.push('Le port doit être entre 1 et 65535')
        return { isValid: false, errors }
      }

      // Ports système (privilégiés)
      if (port < 1024) {
        warnings.push('Les ports inférieurs à 1024 nécessitent des privilèges administrateur')
      }

      // Ports couramment utilisés à éviter
      const commonPorts = [22, 23, 25, 53, 80, 110, 143, 443, 993, 995]
      if (commonPorts.includes(port)) {
        warnings.push(`Le port ${port} est couramment utilisé par d'autres services`)
      }

      return {
        isValid: errors.length === 0,
        errors,
        warnings: warnings.length > 0 ? warnings : undefined
      }
    }
  })

  /**
   * Règles de validation pour les ressources système
   */
  const validateSystemResources = (): BusinessValidationRule<{ cpu: number; memory: number; storage: number }> => ({
    name: 'system-resources',
    description: 'Validation des ressources système',
    validator: (resources: { cpu: number; memory: number; storage: number }) => {
      const errors: string[] = []
      const warnings: string[] = []

      // CPU (en millicores)
      if (resources.cpu < 100) {
        errors.push('CPU minimum : 100m (0.1 core)')
      }
      if (resources.cpu > 32000) {
        warnings.push('Allocation CPU très élevée, vérifiez la disponibilité')
      }

      // Mémoire (en MB)
      if (resources.memory < 128) {
        errors.push('Mémoire minimum : 128MB')
      }
      if (resources.memory > 64000) {
        warnings.push('Allocation mémoire très élevée, vérifiez la disponibilité')
      }

      // Stockage (en GB)
      if (resources.storage < 1) {
        errors.push('Stockage minimum : 1GB')
      }
      if (resources.storage > 1000) {
        warnings.push('Allocation stockage très élevée, vérifiez la disponibilité')
      }

      // Ratios recommandés
      const memoryToCpuRatio = resources.memory / (resources.cpu / 1000) // MB par core
      if (memoryToCpuRatio < 512) {
        warnings.push('Ratio mémoire/CPU faible, performances potentiellement limitées')
      }

      return {
        isValid: errors.length === 0,
        errors,
        warnings: warnings.length > 0 ? warnings : undefined
      }
    }
  })

  /**
   * Validation de l'unicité d'un nom dans un contexte
   */
  const validateUniqueName = (
    existingNames: string[],
    caseSensitive = false
  ): BusinessValidationRule<string> => ({
    name: 'unique-name',
    description: 'Validation de l\'unicité du nom',
    validator: (name: string) => {
      const errors: string[] = []

      const namesToCheck = caseSensitive ? existingNames : existingNames.map(n => n.toLowerCase())
      const nameToCheck = caseSensitive ? name : name.toLowerCase()

      if (namesToCheck.includes(nameToCheck)) {
        errors.push('Ce nom est déjà utilisé')
      }

      return {
        isValid: errors.length === 0,
        errors
      }
    }
  })

  /**
   * Validation des tags
   */
  const validateTag = (): BusinessValidationRule<string> => ({
    name: 'tag-validation',
    description: 'Validation des tags',
    validator: (tag: string) => {
      const errors: string[] = []

      // Format des tags
      if (!/^[a-z0-9\-]+$/.test(tag)) {
        errors.push('Les tags ne peuvent contenir que des minuscules, chiffres et tirets')
      }

      if (tag.length < 2 || tag.length > 20) {
        errors.push('Les tags doivent contenir entre 2 et 20 caractères')
      }

      if (tag.startsWith('-') || tag.endsWith('-')) {
        errors.push('Les tags ne peuvent pas commencer ou finir par un tiret')
      }

      return {
        isValid: errors.length === 0,
        errors
      }
    }
  })

  /**
   * Efface le cache de validation
   */
  const clearValidationCache = () => {
    validationCache.value.clear()
  }

  /**
   * Ajoute un résultat au cache
   */
  const cacheValidationResult = (key: string, result: ValidationResult) => {
    validationCache.value.set(key, result)
  }

  /**
   * Récupère un résultat du cache
   */
  const getCachedValidationResult = (key: string): ValidationResult | undefined => {
    return validationCache.value.get(key)
  }

  /**
   * Utilitaire pour créer une clé de cache
   */
  const createCacheKey = (ruleName: string, value: any): string => {
    return `${ruleName}:${JSON.stringify(value)}`
  }

  return {
    // État (readonly pour éviter les modifications directes)
    loading: readonly(loading),
    error: readonly(error),

    // Computed properties
    cacheSize,

    // Fonctions de validation principales
    validateWithRule,
    validateWithRules,

    // Règles de validation métier prédéfinies
    validateOrganizationName,
    validateEnvironmentName,
    validateBusinessEmail,
    validateSecurePassword,
    validateNetworkPort,
    validateSystemResources,
    validateUniqueName,
    validateTag,

    // Gestion du cache
    clearValidationCache,
    cacheValidationResult,
    getCachedValidationResult,
    createCacheKey
  }
}

/**
 * Règles de validation métier prêtes à l'emploi
 */
export const businessValidationRules = {
  organizationName: (constraints?: NamingConstraints) => useValidation().validateOrganizationName(constraints),
  environmentName: (constraints?: NamingConstraints) => useValidation().validateEnvironmentName(constraints),
  businessEmail: () => useValidation().validateBusinessEmail(),
  securePassword: () => useValidation().validateSecurePassword(),
  networkPort: () => useValidation().validateNetworkPort(),
  systemResources: () => useValidation().validateSystemResources(),
  uniqueName: (existingNames: string[], caseSensitive = false) =>
    useValidation().validateUniqueName(existingNames, caseSensitive),
  tag: () => useValidation().validateTag()
}
