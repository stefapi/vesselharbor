# Frontend - FastAPI Vue Template

This directory contains the Vue.js frontend for the FastAPI Vue Template project.

## 🚀 Features

- **Vue 3**: Modern JavaScript framework with Composition API
- **TypeScript**: Type-safe JavaScript
- **Vite**: Fast build tool and development server
- **Pinia**: State management
- **Vue Router**: Client-side routing
- **UnoCSS**: Utility-first CSS framework
- **Testing**: Vitest for unit tests and Playwright for E2E tests
- **PWA Support**: Progressive Web App capabilities
- **Auto-imports**: Automatic component and API imports
- **Vue DevTools**: Enhanced debugging experience

## 📋 Prerequisites

- Node.js ≥ 20.0.0
- pnpm ≥ 9.0.0
- Docker ≥ 20.10 (for containerized development)
- IDE with TypeScript support (VS Code recommended)

## 🛠️ Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/fastapivue-template.git
   cd fastapivue-template
   ```

2. Install dependencies:
   ```bash
   cd frontend
   pnpm install
   ```

3. Create a `.env` file (or use the existing one from the root directory):
   ```bash
   ln -s ../.env .env
   # or
   cp ../.env.example .env
   ```

## 🚀 Development

Start the development server:
```bash
pnpm dev
```

This will start the Vite development server at http://localhost:5173 with hot module replacement.

### Available Scripts

- `pnpm dev`: Start development server
- `pnpm build`: Build for production
- `pnpm preview`: Preview production build locally
- `pnpm lint`: Run ESLint
- `pnpm format`: Format code with Prettier
- `pnpm test`: Run Vitest tests in watch mode
- `pnpm test:ci`: Run Vitest tests once (for CI)
- `pnpm test:e2e`: Run Playwright E2E tests
- `pnpm test:e2e:dev`: Run Playwright E2E tests against dev server
- `pnpm test:eui:dev`: Run Playwright tests with UI
- `pnpm test:record:dev`: Record Playwright tests

## 📁 Project Structure

```
frontend/
├── public/             # Static assets
├── src/
│   ├── assets/         # Images, fonts, etc.
│   ├── components/     # Reusable Vue components
│   ├── composables/    # Composition API hooks
│   ├── layouts/        # Page layouts
│   ├── pages/          # Page components (auto-routed)
│   ├── router/         # Vue Router configuration
│   ├── services/       # API service layer
│   ├── store/          # Pinia stores
│   ├── types/          # TypeScript type definitions
│   ├── utils/          # Utility functions
│   ├── views/          # View components
│   ├── App.vue         # Root component
│   └── main.ts         # Application entry point
└── tests/              # Test files
```

## 🔧 Configuration

- **Vite**: `vite.config.ts`
- **TypeScript**: `tsconfig.json`
- **ESLint**: `eslint.config.js`
- **Prettier**: `.prettierrc`
- **Stylelint**: `.stylelintrc.json`
- **UnoCSS**: `uno.config.ts`

## 🧪 Testing

### Unit Tests

Run unit tests with Vitest:
```bash
pnpm test
```

### End-to-End Tests

Run E2E tests with Playwright:
```bash
pnpm test:e2e
```

## 🔍 Development Tools

- **UnoCSS Explorer**: http://localhost:5173/__unocss
- **Vite Inspector**: http://localhost:5173/__inspect/
- **Vue DevTools**: http://localhost:5173/__devtools__/

## 📚 Documentation

For more detailed information, please refer to:

- [CONTRIBUTING.md](./CONTRIBUTING.md) - Guidelines for contributing to the frontend
- [CHANGELOG.md](./CHANGELOG.md) - History of changes to the frontend
- [Vue.js Documentation](https://vuejs.org/)
- [Pinia Documentation](https://pinia.vuejs.org/)
- [UnoCSS Documentation](https://unocss.dev/)
- [Vite Documentation](https://vitejs.dev/)

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guide](./CONTRIBUTING.md) before submitting a pull request.
