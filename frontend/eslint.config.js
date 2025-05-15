// eslint.config.js  – @ts-check
import eslint   from '@eslint/js'
import vue      from 'eslint-plugin-vue'
import tseslint from 'typescript-eslint'
import imp      from 'eslint-plugin-import'
import prettier from 'eslint-plugin-prettier'
import unused   from 'eslint-plugin-unused-imports'
import n        from 'eslint-plugin-n'
import vitest   from '@vitest/eslint-plugin'

export default tseslint.config(
  /** bloc ignore = .eslintignore */
  { ignores: ['dist', 'node_modules', 'public', '*.css', '*.scss'] },

  /* presets */
  eslint.configs.recommended,
  ...tseslint.configs.recommended,
  ...vue.configs['flat/recommended'],
  n.configs['flat/recommended-script'],

  /** rules applicables à TOUT le code d’app */
  {
    files: ['**/*.{ts,vue,tsx}'],
    plugins: {
      '@typescript-eslint': tseslint.plugin,
      vue,
      import: imp,
      prettier,
      'unused-imports': unused
    },
    languageOptions: {
      parser: tseslint.parser,
      parserOptions: {
        project: './tsconfig.json',
        tsconfigRootDir: import.meta.dirname,
        extraFileExtensions: ['.vue'],
        ecmaFeatures: { jsx: true }
      }
    },
    settings: {
      /* ↓ pour que eslint-plugin-import comprenne les alias TS */
      'import/resolver': { typescript: { project: './tsconfig.json' } },
      'import/parsers': { '@typescript-eslint/parser': ['.ts', '.tsx', '.vue'] },
      vue: { version: 'detect' }
    },
    rules: {
      /* Style – laissez Prettier décider */
      ...prettier.configs.recommended.rules,

      /* Vos exclusions Vue */
      'vue/no-v-html': 'off',
      'vue/require-default-prop': 'off',
      'vue/multi-word-component-names': 'off',

      /* Imports */
      'import/order': ['error',
        { groups: ['type', 'builtin', 'external', 'internal',
                   'parent', 'sibling', 'index'],
          alphabetize: { order: 'asc', caseInsensitive: true },
          'newlines-between': 'always'
        }],

      /* Unused */
      'no-unused-vars': 'off',
      'unused-imports/no-unused-imports': 'error',
      'unused-imports/no-unused-vars': [
        'warn', { vars: 'all', varsIgnorePattern: '^_', args: 'after-used',
                  argsIgnorePattern: '^_' }
      ],

      /* Préférences Prettier */
      'prettier/prettier': ['error',
        { singleQuote: true, semi: false,
          singleAttributePerLine: true,   // ← 1 attribut / ligne
          endOfLine: 'auto'
        }]
    }
  },

  /** overrides pour les tests Vitest */
  {
    files: ['**/*.test.{ts,tsx}', '**/__tests__/**/*.{ts,tsx}'],
    plugins: { vitest },
    languageOptions: { globals: vitest.environments.env.globals },
    rules: vitest.configs.recommended.rules
  }
)
