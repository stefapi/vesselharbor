import { defineConfig, presetUno, presetIcons, presetWind } from 'unocss'
import { presetAttributify, transformerDirectives, transformerVariantGroup } from 'unocss'

export default defineConfig({
  presets: [
    presetAttributify(),
    presetUno({
      prefix: 'u-', // ✅ Ton préfixe personnalisé
    }),
    presetWind(), // style tailwind-like
    presetIcons(),
  ],
  transformers: [transformerDirectives(), transformerVariantGroup()],
  theme: {
    colors: {
      primary: 'var(--va-primary)',
      success: 'var(--va-success)',
      danger: 'var(--va-danger)',
      background: 'var(--va-background-primary)',
    },
    shortcuts: {
   'card-style': 'bg-white rounded-lg shadow-sm p-6'
    },
    breakpoints: {
      md: '768px',
    },
  },
})
