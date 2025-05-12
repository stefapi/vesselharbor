import { defineConfig, presetUno, presetTypography, presetWebFonts, presetIcons, presetWind } from 'unocss'
import { presetAttributify, transformerDirectives, transformerVariantGroup } from 'unocss'

export default defineConfig({
  content: {
    pipeline: {
      include: ['./index.html', './src/**/*.{vue,js,ts,md}', './src/styles/**/*.{css}'],
    },
  },
  presets: [
    presetUno({
      prefix: 'u-', // ✅ Ton préfixe personnalisé
    }),
    presetAttributify(),

    presetWind(), // style tailwind-like
    presetIcons(),
            presetTypography(),
        presetWebFonts({
            fonts: {
                sans: "Roboto",
                serif: "DM Serif Display",
                mono: "DM Mono",
            },
        }),
  ],
  safelist: ['u-bg-code-bg u-prose u-m-auto u-text-left".split(" ")'],
  transformers: [transformerDirectives(), transformerVariantGroup()],
  theme: {
    colors: {
      primary: '#646cff',
      success: '#4CAF50', // Vert Vuestic
      danger: '#FF5252', // Rouge Vuestic
      warning: '#FFC107', // Orange Vuestic
      info: '#2196F3', // Bleu Vuestic
      'code-bg': '#f5f5f5', // pour SHiki
      gray: {
        100: '#f5f5f5',
        300: '#e5e7eb',
        700: '#374151',
        800: '#1f2937',
        900: '#111827',
      },
      white: '#ffffff',
    },
    breakpoints: {
      md: '768px',
    },
  },
  shortcuts: {
    'full-reset': 'u-m-0 u-p-0 u-box-border',
    'form': 'u-space-y-4',
    'form-item': 'u-w-full u-space-y-2',
    btn: 'u-bg-primary u-text-white u-px-4 u-py-2 u-rounded hover:u-bg-primary/90 u-transition',
    card: 'u-bg-white u-rounded-lg u-shadow-sm u-p-6',
    'shiki-block': 'u-bg-code-bg u-text-black u-p-4 u-rounded u-text-sm u-leading-relaxed u-overflow-auto',
          'card-style': 'bg-white rounded-lg shadow-sm p-6',
    // ✅ Badges
    badge: 'u-inline-block u-px-2 u-py-0.5 u-rounded u-text-xs u-font-semibold',
    'badge-success': 'badge u-bg-success u-text-white',
    'badge-danger': 'badge u-bg-danger u-text-white',
    'badge-warning': 'badge u-bg-warning u-text-black',
    'badge-info': 'badge u-bg-info u-text-white',

    // ✅ Tags
    tag: 'u-inline-block u-text-xs u-px-2 u-py-0.5 u-rounded-full u-border u-font-medium',
    'tag-ghost': 'tag u-bg-gray-100 u-text-gray-600 u-border-transparent',
    'tag-outline': 'tag u-border-gray-300 u-text-gray-700 u-bg-transparent',
    'tag-primary': 'tag u-bg-primary/10 u-text-primary u-border-primary/20',
    'tag-danger': 'tag u-bg-danger/10 u-text-danger u-border-danger/20',
    'tag-success': 'tag u-bg-success/10 u-text-success u-border-success/20',

    'markdown-body': 'u-m-auto u-text-left u-max-w-full',
    'markdown-body-card': 'u-w-full u-max-w-3xl u-shadow-md u-bg-white dark:u-bg-gray-800 u-border-none',
  },
})
