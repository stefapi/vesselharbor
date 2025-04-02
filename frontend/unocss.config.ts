// unocss.config.ts
import { defineConfig, presetUno, presetAttributify, presetIcons } from 'unocss'

export default defineConfig({
  shortcuts: {
    // Définition d'un raccourci pour un bouton
    'btn': 'px-4 py-1 rounded inline-block bg-primary text-white cursor-pointer hover:bg-primary-600 disabled:cursor-default disabled:bg-gray-600 disabled:opacity-50',
    // Raccourci pour un bouton avec icône
    'icon-btn': 'inline-block cursor-pointer select-none opacity-75 transition duration-200 ease-in-out hover:opacity-100 hover:text-primary',
  },
  presets: [
    presetUno(),
    presetAttributify(),
    presetIcons({
      scale: 1.2, // ajuste la taille des icônes
      warn: true, // affiche des avertissements pour les icônes non trouvées
    }),
  ],
  rules: [
    // Vous pouvez ajouter ici des règles personnalisées si nécessaire
  ],
});
