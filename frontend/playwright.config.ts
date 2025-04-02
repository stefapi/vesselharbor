import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests', // Dossier où sont vos tests
  fullyParallel: true, // Exécution en parallèle
  retries: 2, // Nombre de réessais en cas d'échec
  workers: 3, // Nombre de workers pour les tests parallèles
  reporter: 'html', // Rapport HTML
  use: {
    baseURL: 'http://localhost:3001', // URL de votre app Vue en dev
    trace: 'on-first-retry', // Capture des traces pour le debug
    screenshot: 'only-on-failure', // Screenshots en cas d'échec
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
  ],
    webServer: {
    command: 'npm run dev', // Lance Vite en mode dev
    url: 'http://localhost:3001', // URL de votre app
    reuseExistingServer: true, // Réutilise le serveur si déjà lancé
    timeout: 120 * 1000, // Délai d'attente max
  },
});
