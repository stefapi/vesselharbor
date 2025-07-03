# Project Development Guidelines

This document provides guidelines and information for developing and maintaining this FastAPI + Vue.js project.

## Build and Configuration Instructions

### Prerequisites

- Docker ≥ 20.10 and docker-compose v2 (for containerized deployment)
- Node.js ≥ 18 and pnpm ≥ 8 (for frontend development)
- Python ≥ 3.13 and poetry ≥ 1.8 (for backend development)

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
docker build -t myapp:latest .

# Run
docker run -d --name myapp -p 80:80 myapp:latest
```

#### Docker Compose Stack

```bash
# Copy environment files
cp .env.example .env
cp backend/.env.example backend/.env

# Start services
docker compose up --build -d

# Stop services
docker compose down
```

## Testing Information

### Backend Testing (pytest)

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

### Frontend Testing

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

5. Adding new tests:
   - Create test files in the `frontend/tests` directory
   - Use the Playwright API for writing tests

Example test:
```typescript
import { test, expect } from '@playwright/test'

test('basic navigation', async ({ page }) => {
  await page.goto('/')
  await expect(page.locator('h1')).toContainText('Welcome')
  await page.click('text=Login')
  await expect(page).toHaveURL(/.*login/)
})
```

## Code Style and Development Practices

### Backend (Python)

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

### Development Workflow

1. For simultaneous frontend and backend development:
   - Start the backend server with hot reload
   - Start the frontend dev server
   - Access the application at http://localhost:5173

2. Available development tools:
   - UnoCSS Explorer: http://localhost:5173/__unocss
   - Vite Inspector: http://localhost:5173/__inspect/
   - Vue 3 DevTools: http://localhost:5173/__devtools__/

3. Project structure:
   - Backend code is in the `app` directory
   - Frontend code is in the `frontend/src` directory
   - Docker configuration is in the root directory

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
     "[python]": {
       "editor.formatOnSave": true,
       "editor.defaultFormatter": "ms-python.black-formatter"
     }
   }
   ```

#### PyCharm

1. Configure Poetry:
   - Settings → Python Interpreter → Add → Poetry Environment
   - Select the existing environment in the project

2. Configure ESLint and Prettier:
   - Settings → Languages & Frameworks → JavaScript → Code Quality Tools → ESLint
   - Enable ESLint and set the path to the ESLint package

## API Integration Examples

### Authentication

```typescript
// services/authService.ts
import { api } from './api'

export async function login(username: string, password: string) {
  try {
    const response = await api.post('/auth/login', { username, password })
    const token = response.data.access_token

    // Store token
    localStorage.setItem('token', token)

    // Set default Authorization header for future requests
    api.defaults.headers.common['Authorization'] = `Bearer ${token}`

    return response.data
  } catch (error) {
    console.error('Login failed:', error)
    throw error
  }
}

export async function getCurrentUser() {
  try {
    const response = await api.get('/users/me')
    return response.data
  } catch (error) {
    console.error('Failed to get current user:', error)
    throw error
  }
}
```

### User Management

```typescript
// services/userService.ts
import { api } from './api'
import type { User, UserCreate } from '@/types/user'

export async function getUsers(skip = 0, limit = 100): Promise<User[]> {
  const response = await api.get('/users/', { params: { skip, limit } })
  return response.data
}

export async function getUser(id: number): Promise<User> {
  const response = await api.get(`/users/${id}`)
  return response.data
}

export async function createUser(userData: UserCreate): Promise<User> {
  const response = await api.post('/users/', userData)
  return response.data
}

export async function updateUser(id: number, userData: Partial<User>): Promise<User> {
  const response = await api.put(`/users/${id}`, userData)
  return response.data
}

export async function deleteUser(id: number): Promise<void> {
  await api.delete(`/users/${id}`)
}
```

## Environment Variables

### Backend (.env)

```
# Database
DATABASE_URL=postgresql://postgres:postgres@db:5432/app
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=app

# Security
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Server
BACKEND_CORS_ORIGINS=["http://localhost:5173","http://localhost:80"]
```

### Frontend (.env)

```
VITE_API_BASE_URL=http://localhost:8010/api/v1
VITE_APP_TITLE=FastAPI Vue Template
```

## Performance Optimization

### Backend

1. Database query optimization:
   - Use SQLAlchemy's `select()` instead of `query()` for better performance
   - Add indexes to frequently queried columns
   - Use `joinedload()` to avoid N+1 query problems

2. Caching:
   - Use Redis for caching frequently accessed data
   - Implement FastAPI's response caching with `@app.get(..., response_model_exclude_unset=True)`

3. Async operations:
   - Use async/await for I/O-bound operations
   - Use background tasks for non-critical operations: `BackgroundTasks.add_task()`

### Frontend

1. Component optimization:
   - Use `v-once` for static content
   - Use `v-memo` to memoize DOM nodes
   - Implement virtual scrolling for long lists

2. Bundle optimization:
   - Enable code splitting with dynamic imports
   - Use tree-shaking to eliminate dead code
   - Optimize images and assets

## Troubleshooting Common Issues

### Backend

1. Database connection issues:
   - Check database credentials in `.env`
   - Ensure database service is running
   - Verify network connectivity between app and database

2. Migration errors:
   - Run `alembic upgrade head` to apply all migrations
   - Check for conflicts in migration files

3. Authentication problems:
   - Verify SECRET_KEY is consistent
   - Check token expiration time
   - Ensure correct permissions for endpoints

### Frontend

1. API connection issues:
   - Verify API base URL in `.env`
   - Check CORS settings in backend
   - Inspect network requests in browser DevTools

2. Build errors:
   - Clear node_modules and reinstall: `rm -rf node_modules && pnpm install`
   - Check TypeScript errors: `pnpm type-check`
   - Verify Vue component syntax

3. State management issues:
   - Use Vue DevTools to inspect Pinia store state
   - Check for reactivity issues with complex objects
   - Verify store actions are being dispatched correctly

## Additional Resources

- API Documentation: http://localhost:8010/docs (Swagger UI) or http://localhost:8010/redoc (ReDoc)
- Container logs: `docker compose logs -f backend`
- Test coverage reports: `cd frontend && pnpm coverage`
- Vue.js Documentation: https://vuejs.org/guide/introduction.html
- FastAPI Documentation: https://fastapi.tiangolo.com/
- Pinia Documentation: https://pinia.vuejs.org/
- UnoCSS Documentation: https://unocss.dev/
