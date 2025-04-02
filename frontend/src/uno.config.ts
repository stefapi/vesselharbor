import { defineConfig, presetUno, presetIcons, presetWind } from 'unocss'

export default defineConfig({
  presets: [
    presetUno(),
    presetWind(), // style tailwind-like
    presetIcons(),
  ],
})
