# VesselHarbor Project Guidelines

## Project Overview

VesselHarbor is a self-hosted platform for managing and orchestrating containerized applications and virtual machines. It provides a comprehensive solution for infrastructure management, similar to platforms like Heroku or Vercel, with a focus on simplicity.

Key features include:
- Container orchestration (Docker, Docker Compose, Docker Swarm)
- Virtual machine management
- Network infrastructure management
- Application deployment and monitoring
- Integration capabilities with SSO providers and external systems

The project uses a modern tech stack:
- Backend: FastAPI with Python 3.13+
- Frontend: Vue 3 with TypeScript
- Database: PostgreSQL with SQLAlchemy ORM
- Containerization: Docker and Docker Compose

### Prerequisites

- Docker ≥ 20.10 and docker-compose v2 (for containerized deployment)
- Node.js ≥ 18 and pnpm ≥ 8 (for frontend development)
- Python ≥ 3.13 and poetry ≥ 1.8 (for backend development)

## Project Structure

```
./
├── app/                  # FastAPI backend
│   ├── alembic/          # Database migrations
│   ├── api/              # API endpoints
│   ├── core/             # Core application components
│   ├── db/               # Database models and session
│   ├── models/           # Pydantic models
│   ├── services/         # Business logic
│   └── tests/            # Backend tests
├── frontend/             # Vue 3 frontend
│   ├── public/           # Static assets
│   ├── src/              # Source code
│   │   ├── assets/       # Images, fonts, etc.
│   │   ├── components/   # Vue components
│   │   ├── composables/  # Composition API hooks
│   │   ├── layouts/      # Page layouts
│   │   ├── router/       # Vue Router configuration
│   │   ├── services/     # API service layer
│   │   ├── store/        # Pinia stores
│   │   └── views/        # Page components
│   └── tests/            # Frontend tests
├── .junie/               # Project documentation
├── docker/               # Additional Dockerfiles
├── docker-compose.yml    # Docker Compose configuration
└── .env.example          # Environment variables example
```

## Development Setup

### Backend Setup (FastAPI)

1. Install dependencies:
   ```bash
   cd app
   poetry install
   ```

2. Configure environment variables:
   ```bash
   cp .env.example .env
   ```

3. Run the development server:
   ```bash
   poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8010
   ```

   Alternatively, use the Makefile:
   ```bash
   make run
   ```

### Frontend Setup (Vue 3)

1. Install dependencies:
   ```bash
   cd frontend
   pnpm install
   ```

2. Run the development server:
   ```bash
   pnpm dev
   ```

### Docker Deployment

#### All-in-one Image

```bash
# Build
docker build -t vesselharbor:latest .

# Run
docker run -d --name vesselharbor -p 80:80 vesselharbor:latest
```

#### Docker Compose Stack

```bash
# Copy environment files
cp .env.example .env
cp app/.env.example app/.env

# Start services
docker compose up --build -d

# Stop services
docker compose down
```

### Development Workflow

For simultaneous frontend and backend development:

1. Start the backend server with hot reload
2. Start the frontend dev server
3. Access the application at http://localhost:5173

Before the first `up`, copy the environment example files:

```bash
cp .env.example .env          # Application secrets
cp app/.env.example app/.env
```

## Testing Guidelines

### Backend Tests (pytest)

The backend uses pytest for testing. Tests are located in the `app/tests` directory.

1. Run all tests:
   ```bash
   cd app
   poetry run pytest
   ```

   Or use the Makefile:
   ```bash
   make test
   ```

2. Adding new tests:
   - Create test files in the `app/tests` directory with the naming pattern `test_*.py`
   - Use the fixtures defined in `conftest.py` for common test setup
   - Follow the existing test patterns for consistency

Example test:
```python
def test_feature(test_client, test_data):
    response = test_client.get("/endpoint")
    assert response.status_code == 200
    data = response.json()
    assert "expected_key" in data
```

### Frontend Tests

#### Unit Tests (Vitest)

The frontend uses Vitest for unit testing. Tests are located in the `frontend/tests` directory.

1. Run tests in watch mode:
   ```bash
   cd frontend
   pnpm test
   ```

2. Run tests once (for CI):
   ```bash
   pnpm test:ci
   ```

3. Adding new tests:
   - Create test files with the naming pattern `*.test.ts` or `*.spec.ts`
   - Use the Vitest API (`describe`, `it`, `expect`) for writing tests

Example test:
```typescript
import { describe, it, expect } from 'vitest'

function sum(a: number, b: number): number {
  return a + b
}

describe('Sum function', () => {
  it('adds two numbers correctly', () => {
    expect(sum(1, 2)).toBe(3)
  })
})
```

#### End-to-End Tests (Playwright)

The frontend uses Playwright for end-to-end testing. Tests are configured in `frontend/playwright.config.ts`.

1. Run e2e tests:
   ```bash
   cd frontend
   pnpm test:e2e
   ```

2. Run e2e tests in development mode:
   ```bash
   pnpm test:e2e:dev
   ```

3. Run e2e tests with UI:
   ```bash
   pnpm test:eui:dev
   ```

4. Record new tests:
   ```bash
   pnpm test:record:dev
   ```

## Build Instructions

Before submitting changes, verify that the project builds correctly:

```bash
# For Docker-based build
docker compose build --no-cache

# For backend development
cd app
poetry install

# For frontend development
cd frontend
pnpm install
pnpm build
```

## Code Style Guidelines

### Backend (Python)

- Follow PEP 8 guidelines for Python code
- Code formatting is enforced using `black` and `isort`
- Run linting checks:
  ```bash
  make lint
  ```
- Format code:
  ```bash
  make format
  ```

### Frontend (Vue/TypeScript)

- Follow the project's ESLint configuration
- Use the Composition API with `<script setup>` syntax
- Use UnoCSS utility classes for styling
- Code formatting is enforced using Prettier with the following configuration:
  - No semicolons
  - Single quotes
  - 2 spaces for indentation
  - ES5-style trailing commas

- Run linting checks:
  ```bash
  cd frontend
  pnpm lint
  ```

- Format code:
  ```bash
  cd frontend
  pnpm format
  ```

## Git Workflow

The project follows a GitFlow-based branching strategy:

### Branch Structure
- **main**: Production-ready code
- **develop**: Integration branch for development
- **feature/xxx**: For new features
- **bugfix/xxx**: For non-critical bug fixes
- **hotfix/xxx**: For urgent fixes from main
- **release/x.y.z**: For release preparation

### Commit Conventions
We follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>[scope optional]: <description>
```

Types include:
- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Formatting changes
- **refactor**: Code refactoring
- **test**: Adding or fixing tests
- **chore**: Maintenance tasks

### Pull Request Process
1. Create a branch from develop
2. Make your changes with regular commits
3. Keep your branch updated with develop
4. Submit a pull request with a clear description
5. Ensure all tests pass
6. Address review comments
7. Squash and merge after approval

For more details, see [Git Workflow](git_workflow.md).

## Debugging and Development Tools

### Backend Debugging

1. Using pdb:
   ```python
   import pdb; pdb.set_trace()  # Add this line where you want to set a breakpoint
   ```

2. Using FastAPI's debug mode:
   - The `--reload` flag enables hot reloading
   - Set `debug=True` in your FastAPI app for more detailed error information:
     ```python
     app = FastAPI(debug=True)
     ```

3. Logging:
   ```python
   import logging

   logging.basicConfig(level=logging.DEBUG)
   logger = logging.getLogger(__name__)

   logger.debug("Debug message")
   logger.info("Info message")
   logger.warning("Warning message")
   logger.error("Error message")
   ```

### Frontend Debugging

1. Vue DevTools:
   - Install the [Vue.js DevTools](https://chrome.google.com/webstore/detail/vuejs-devtools/nhdogjmejiglipccpnnnanhbledajbpd) browser extension
   - Access it at http://localhost:5173/__devtools__/

2. Console logging:
   ```typescript
   console.log('Data:', data)
   console.warn('Warning message')
   console.error('Error message')
   ```

3. Network monitoring:
   - Use browser DevTools (F12) to monitor API requests in the Network tab
   - Filter by XHR/Fetch requests to focus on API calls

4. Component debugging:
   - Use the Vite Inspector at http://localhost:5173/__inspect/
   - Click on any component to see its source code

### Development Tools
- UnoCSS Explorer: http://localhost:5173/__unocss
- Vue 3 DevTools: http://localhost:5173/__devtools__/

### IDE Setup

#### VS Code

1. Recommended extensions:
   - Vue Language Features (Volar)
   - TypeScript Vue Plugin (Volar)
   - ESLint
   - Prettier
   - Python
   - Pylance
   - Docker

2. Workspace settings (`.vscode/settings.json`):
   ```json
   {
     "editor.formatOnSave": true,
     "editor.codeActionsOnSave": {
       "source.fixAll.eslint": true
     },
     "python.linting.enabled": true,
     "python.linting.pylintEnabled": true,
     "python.formatting.provider": "black",
     "[vue]": {
       "editor.defaultFormatter": "Vue.volar"
     },
     "[typescript]": {
       "editor.defaultFormatter": "esbenp.prettier-vscode"
     },
     "[javascript]": {
       "editor.defaultFormatter": "esbenp.prettier-vscode"
     },
     "[python]": {
       "editor.defaultFormatter": "ms-python.python"
     }
   }
   ```

## Environment Variables

### Backend (.env)
```
DATABASE_URL=postgresql://postgres:postgres@db:5432/app
SECRET_KEY=your-secret-key-here
BACKEND_CORS_ORIGINS=["http://localhost:5173","http://localhost:80"]
```

### Frontend (.env)
```
VITE_API_BASE_URL=http://localhost:8010/api/v1
VITE_APP_TITLE=VesselHarbor
```

## Troubleshooting Common Issues

### Database Connection Issues
- Check database credentials in `.env`
- Ensure database service is running
- Verify network connectivity

### Build Errors
- Clear node_modules: `rm -rf node_modules && pnpm install`
- Check TypeScript errors: `pnpm type-check`
- Verify Vue component syntax

### API Connection Issues
- Verify API base URL in `.env`
- Check CORS settings in backend
- Inspect network requests in browser DevTools

## Documentation

When making significant changes, update the relevant documentation in the `.junie` directory:
- API Endpoints (`.junie/api-endpoints.md`)
- Architecture (`.junie/architecture.md`)
- Authentication (`.junie/authentication.md`)
- Changelog (`.junie/changelog.md`)
