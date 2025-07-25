import path from 'node:path'

import vue from '@vitejs/plugin-vue'
import vueJsx from '@vitejs/plugin-vue-jsx'
// @ts-expect-error - No type definitions available for markdown-it-link-attributes
import LinkAttributes from 'markdown-it-link-attributes'
import Shiki from 'markdown-it-shiki'
import { visualizer } from 'rollup-plugin-visualizer'
import UnoCSS from 'unocss/vite'
import AutoImport from 'unplugin-auto-import/vite'
import ElementPlus from 'unplugin-element-plus/vite'
import { FileSystemIconLoader } from 'unplugin-icons/loaders'
import IconsResolver from 'unplugin-icons/resolver'
import Icons from 'unplugin-icons/vite'
import { ElementPlusResolver } from 'unplugin-vue-components/resolvers'
import Components from 'unplugin-vue-components/vite'
import { default as Inspector } from 'unplugin-vue-inspector/vite'
import VueMacros from 'unplugin-vue-macros/vite'
import Markdown from 'unplugin-vue-markdown/vite'
import { VueRouterAutoImports } from 'unplugin-vue-router'
import VueRouter from 'unplugin-vue-router/vite'
import { defineConfig } from 'vite'
import compression from 'vite-plugin-compression'
import dts from 'vite-plugin-dts'
import Inspect from 'vite-plugin-inspect'
import mkcert from 'vite-plugin-mkcert'
import { VitePWA } from 'vite-plugin-pwa'
import VueDevTools from 'vite-plugin-vue-devtools'
import webfontDownload from 'vite-plugin-webfont-dl'

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
      routeBlockLang: 'yaml', // or json, depending on your preference
    }),
    ElementPlus({
      useSource: true, // Enable customizable SCSS styles
    }),
    // 🧪 Vite plugin inspection tools
    Inspect({
      build: true,
      outputDir: '.vite-inspect',
    }),

    // @ts-expect-error - Plugin callable issue
    Inspector({
      launchEditor: 'pycharm',
    }),
    // @ts-expect-error - Plugin callable issue
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
        name: 'VesselHarbor',
        short_name: 'VesselHarbor',
        description: 'Self-hosted platform for managing and orchestrating containerized applications and virtual machines',
        theme_color: '#ffffff',
        background_color: '#ffffff',
        display: 'standalone',
        start_url: '/',
        scope: '/',
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
    UnoCSS(), // ✅ Uses configuration from uno.config.ts
    // ⚡ Auto-import Vue API + VueUse + Pinia + Router + Composables
    AutoImport({
      imports: [
        'vue',
        'vue-router',
        'pinia',
        '@vueuse/core',
        VueRouterAutoImports,
        {
          '@/composables/api': ['useAuth', 'useUsers', 'useGroups', 'useOrganizations', 'useEnvironments'],
          '@/composables/ui': ['useModal', 'useTable', 'useForm', 'globalModal', 'validationRules'],
          '@/composables/business': ['usePermissions', 'useValidation', 'businessValidationRules', 'ACTIONS', 'RESOURCES'],
        },
      ],
      dts: 'src/auto-imports.d.ts',
      dirs: ['src/services', 'src/store'],
      vueTemplate: true,
    }),
    // https://github.com/antfu/unplugin-icons
    Icons({
      compiler: 'vue3',
      autoInstall: true,
      scale: 1.5, // Default scale for icons
      defaultClass: 'icon', // Default CSS class
      customCollections: {
        // Your custom icons
        'my-icons': FileSystemIconLoader('./src/assets/icons'),
      },
    }),
    // 🧩 Auto-import Vue components
    Components({
      dts: 'src/components.d.ts',
      dirs: ['src/components'],
      extensions: ['vue', 'md'],
      resolvers: [
        ElementPlusResolver(),
        IconsResolver({
          prefix: 'i', // Optional prefix (default: 'i')
          enabledCollections: ['carbon', 'fa', 'mdi', 'twemoji', 'material-symbols'], // Enabled collections
        }),
      ],
      deep: true,
    }),
    Markdown({
      headEnabled: true,
      markdownItSetup(md) {
        // @ts-expect-error - Shiki plugin type compatibility issue
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

    // 🐞 Vue Devtools in development (local)
    VueDevTools(),
    // Performance optimizations
    // @ts-expect-error - Plugin callable issue
    compression(),
    // Webfont download
    // @ts-expect-error - Plugin callable issue
    webfontDownload(),

    // Bundle analysis (only in build mode)
    visualizer({
      open: true,
      gzipSize: true,
      brotliSize: true,
    }),
  ],
  resolve: {
    alias: {
      '@/': `${path.resolve(__dirname, 'src')}/`,
    },
  },
  server: {
    // @ts-expect-error - Plugin callable issue
    https: false,
    port: 3001, // Changed to 3001 to match e2e test scripts
    watch: {
      ignored: ['!**/src/layouts/**'], // 👈 Vite will watch this folder
    },
  },
  preview: {
    port: 3000, // Preview server port for built files
  },
  css: {
    preprocessorOptions: {
      scss: {
        additionalData: `@use "sass:math";`,
      },
    },
  },
  base: './',
  build: {
    manifest: true,
    target: 'esnext',
    minify: 'esbuild',
    rollupOptions: {
      output: {
        manualChunks(id: string) {
          // Core Vue ecosystem
          if (id.includes('pinia')) return 'pinia'
          if (id.includes('vue-router')) return 'vue-router'
          if (id.includes('vue') && !id.includes('vue-router') && !id.includes('@vue')) return 'vue'
          if (id.includes('@vue/')) return 'vue'

          // UI Libraries
          if (id.includes('element-plus')) return 'element-plus'
          if (id.includes('@iconify')) return 'iconify'
          if (id.includes('unplugin-icons')) return 'iconify'

          // Utilities
          if (id.includes('@vueuse/core')) return 'vueuse'
          if (id.includes('axios')) return 'axios'
          if (id.includes('workbox')) return 'workbox'

          // Large vendor libraries
          if (id.includes('node_modules')) {
            return 'vendor'
          }
        },
      },
    },
  },
  optimizeDeps: {
    include: ['vue', 'vue-router', 'pinia', 'pinia-plugin-persistedstate', 'element-plus', '@vueuse/core', 'axios', '@iconify/vue', '@unhead/vue', 'nprogress', 'idb', 'workbox-window'],
  },
})
