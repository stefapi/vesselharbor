import { defineConfig, PluginOption } from 'vite'
import vue from '@vitejs/plugin-vue'
import UnoCSS from 'unocss/vite'
import { presetUno, presetAttributify, presetIcons, presetWind, transformerDirectives, transformerVariantGroup } from 'unocss'
import Inspect from 'vite-plugin-inspect'
import VueDevTools from 'vite-plugin-vue-devtools'
import Components from 'unplugin-vue-components/vite'
import AutoImport from 'unplugin-auto-import/vite'
import Inspector from 'unplugin-vue-inspector/vite'
import dts from 'vite-plugin-dts'
import mkcert from 'vite-plugin-mkcert'
import compression from 'vite-plugin-compression'
import { VitePWA } from 'vite-plugin-pwa'
import VueRouter from 'unplugin-vue-router/vite'
import VueMacros from 'unplugin-vue-macros/vite'
import Icons from 'unplugin-icons/vite'
import IconsResolver from 'unplugin-icons/resolver'
import Markdown from 'unplugin-vue-markdown/vite'
import LinkAttributes from 'markdown-it-link-attributes'
import Shiki from 'markdown-it-shiki'
import vueJsx from '@vitejs/plugin-vue-jsx'
import webfontDownload from 'vite-plugin-webfont-dl'
import { FileSystemIconLoader } from 'unplugin-icons/loaders'
import { VueRouterAutoImports } from 'unplugin-vue-router'
import { visualizer } from 'rollup-plugin-visualizer'
import path from 'node:path'
import ElementPlus from 'unplugin-element-plus/vite'
import { ElementPlusResolver } from 'unplugin-vue-components/resolvers'

export default defineConfig({
  plugins: [
    // https://github.com/vue-macros/vue-macros
    VueMacros({
      plugins: {
        vue: vue({
          include: [/\.vue$/, /\.md$/],
        }),
        vueJsx: vueJsx(),
      },
    }),
    // https://github.com/posva/unplugin-vue-router
    VueRouter({
      /* options */
      routesFolder: 'src/pages',
      extensions: ['.vue', '.md'],
      dts: 'src/types/typed-router.d.ts',
      routeBlockLang: 'yaml', // ou json, selon ta préférence
    }),
    ElementPlus({
      useSource: true, // Active les styles SCSS personnalisables
    }),
    // 🧪 Outils d’inspection des plugins Vite
    Inspect({
      build: true,
      outputDir: '.vite-inspect',
    }),

    Inspector({
      launchEditor: 'pycharm',
    }),
    mkcert(),

    // https://github.com/antfu/vite-plugin-pwa
    VitePWA({
      registerType: 'autoUpdate',
      includeAssets: ['favicon.svg', 'safari-pinned-tab.svg'],
      base: '/',
      workbox: {
        globPatterns: ['manifest.webmanifest', '**/*.{js,css,html,ico,png,svg,webp,woff,woff2,ttf}'],
      },
      manifest: {
        name: 'appName',
        short_name: 'appShort',
        description: 'My Vue Application',
        theme_color: '#ffffff',
        // strategies: "injectManifest",
        icons: [
          {
            src: '/pwa-192x192.png',
            sizes: '192x192',
            type: 'image/png',
          },
          {
            src: '/pwa-512x512.png',
            sizes: '512x512',
            type: 'image/png',
          },
          {
            src: '/pwa-512x512.png',
            sizes: '512x512',
            type: 'image/png',
            purpose: 'any maskable',
          },
        ],
      },
    }),
    UnoCSS({
      presets: [
        presetUno({
          prefix: 'u-', // ✅ Ton préfixe personnalisé
        }),
        presetAttributify(),

        presetWind(), // style tailwind-like
        presetIcons(),
      ],
      transformers: [transformerDirectives(), transformerVariantGroup()],
      inspector: true,
    }), // Ajout du plugin UnoCSS
    // ⚡ Auto-import d’API Vue + VueUse + Pinia + Router
    AutoImport({
      imports: ['vue', 'vue-router', 'pinia', '@vueuse/core', VueRouterAutoImports],
      dts: 'src/auto-imports.d.ts',
      dirs: ['src/services', 'src/store'],
      vueTemplate: true,
    }),
    // https://github.com/antfu/unplugin-icons
    Icons({
      compiler: 'vue3',
      autoInstall: true,
      scale: 1.5, // Échelle par défaut des icônes
      defaultClass: 'icon', // Classe CSS par défaut
      customCollections: {
        // Your custom icons
        'my-icons': FileSystemIconLoader('./src/assets/icons'),
      },
    }),
    // 🧩 Auto-import des composants Vue
    Components({
      dts: 'src/components.d.ts',
      dirs: ['src/components'],
      extensions: ['vue', 'md'],
      resolvers: [
        ElementPlusResolver(),
        IconsResolver({
          prefix: 'i', // Préfixe optionnel (défaut: 'i')
          enabledCollections: ['carbon', 'fa', 'mdi', 'twemoji', 'material-symbols'], // Collections activées
        }),
      ],
      deep: true,
    }),
    Markdown({
      headEnabled: true,
      markdownItSetup(md) {
        md.use(Shiki)
        md.use(LinkAttributes, {
          matcher: (link: string) => /^https?:\/\//.test(link),
          attrs: {
            target: '_blank',
            rel: 'noopener',
          },
        })
      },
    }),

    dts({
      rollupTypes: true,
      entryRoot: 'src', // root directory for the declaration files
      cleanVueFileName: true, // removes .vue suffix from filenames
      staticImport: true, // uses static imports in declaration files
    }),

    // 🐞 Vue Devtools en développement (local)
    VueDevTools(),
    // Performance optimizations
    compression(),
    // Webfont download
    webfontDownload(),

    // Bundle analysis (only in build mode)
    visualizer({
      open: true,
      gzipSize: true,
      brotliSize: true,
    }) as PluginOption,
  ],
  resolve: {
    alias: {
      '@/': `${path.resolve(__dirname, 'src')}/`,
    },
  },
  server: {
    // @ts-ignore
    https: false,
    port: 3000,
    watch: {
      ignored: ['!**/src/layouts/**'], // 👈 Vite va surveiller ce dossier
    },
  },
  base: './',
  build: {
    manifest: true,
    rollupOptions: {
      output: {
        manualChunks(id) {
          if (id.includes('pinia')) return 'pinia'
          if (id.includes('vue-router')) return 'vue-router'
          if (id.includes('@iconify')) return 'iconify'
          if (id.includes('vue')) return 'vue'
        },
      },
    },
  },
})
