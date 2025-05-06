module.exports = {
  root: true,
  env: { browser: true, node: true, es2022: true },
  parser: 'vue-eslint-parser',
  parserOptions: {
    parser: '@typescript-eslint/parser',
    ecmaVersion: 'latest',
    sourceType: 'module',
  },
  extends: ['eslint:recommended', 'plugin:vue/vue3-recommended', 'plugin:@typescript-eslint/recommended', 'plugin:prettier/recommended'],
  plugins: ['vue', '@typescript-eslint', 'import', 'unused-imports', 'unocss', 'prettier'],
  rules: {
    // Typescript
    '@typescript-eslint/no-unused-vars': 'off',
    'unused-imports/no-unused-imports': 'error',
    'import/extensions': 'off',
    'import/no-unresolved': 'off',

    // Vue
    'vue/multi-word-component-names': 'off',
    'vue/no-v-html': 'off',

    // UnoCSS
    'unocss/order': 'warn',

    // Style
    'import/order': [
      'warn',
      {
        groups: ['builtin', 'external', 'internal'],
        alphabetize: { order: 'asc', caseInsensitive: true },
      },
    ],

    // Prettier
    'prettier/prettier': 'warn',
  },
  settings: {
    'import/resolver': {
      typescript: true,
    },
  },
}
