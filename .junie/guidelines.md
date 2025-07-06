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
│   │   ├── auth.py       # Authentication endpoints
│   │   ├── users.py      # User management endpoints
│   │   └── ...           # Other resource endpoints
│   ├── core/             # Core application components
│   ├── database/         # Database configuration and session
│   ├── helper/           # Helper utilities
│   │   ├── audit.py      # Audit logging
│   │   ├── email.py      # Email functionality
│   │   ├── permissions.py # Permission checking
│   │   ├── response.py   # Standardized response formatting
│   │   └── security.py   # Security utilities
│   ├── models/           # SQLAlchemy models
│   ├── repositories/     # Data access layer
│   ├── schema/           # Pydantic schemas for validation
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

### Backend Development Patterns

#### Repository Pattern

The application uses the repository pattern to separate data access logic from business logic:

- **Models**: SQLAlchemy models in the `models/` directory define the database schema
- **Repositories**: Classes in the `repositories/` directory handle data access operations
- **API Routes**: Endpoints in the `api/` directory use repositories to interact with the database

Example repository pattern usage:

```python
# In api/users.py
@router.get("/{user_id}", response_model=dict)
def get_user(user_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Use the repository to get the user
    user = user_repo.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # Check permissions
    if current_user.id != user_id and not permissions.has_permission(db, current_user, None, "user:read"):
        raise HTTPException(status_code=403, detail="Permission insufficient")
    # Return standardized response
    return response.success_response(UserOut.model_validate(user), "User retrieved successfully")

# In repositories/user_repo.py
def get_user(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()
```

#### Standardized Response Format

All API endpoints use a standardized response format through the `response` helper:

```python
# Success response
return response.success_response(data, message)

# Error response (via HTTPException)
raise HTTPException(status_code=status_code, detail=error_message)
```

The standard response format is:

```json
{
  "status": "success",
  "message": "Operation successful message",
  "data": { ... }
}
```

#### Permission System

The application uses a fine-grained permission system:

- Permissions are checked using the `permissions.has_permission()` function
- Permissions are defined as strings in the format `"resource:action"`
- Permissions are enforced at the API endpoint level
- Policies and rules define what users can do with which resources

Example permission check:

```python
if not permissions.has_permission(db, current_user, organization_id, "user:create"):
    raise HTTPException(status_code=403, detail="Permission insufficient")
```

#### Audit Logging

All significant actions are logged using the audit system:

```python
audit.log_action(db, user.id, "Action Type", "Detailed description of the action")
```

#### Error Handling

Errors are handled consistently using FastAPI's HTTPException:

```python
raise HTTPException(status_code=404, detail="Resource not found")
```

Custom exception handlers in main.py ensure consistent error responses.

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

### Frontend Development Patterns

#### Component Structure

Components should follow these patterns:

- Use `<script setup>` syntax for the Composition API
- Define props and emits with TypeScript types
- Use TypeScript interfaces for complex data structures
- Keep components focused on a single responsibility
- Extract reusable logic to composables

Example component:

```vue
<template>
  <div class="u-p-4">
    <h1 class="u-text-2xl u-font-bold">{{ title }}</h1>
    <p v-if="description">{{ description }}</p>
    <slot></slot>
    <el-button @click="$emit('action', id)">{{ buttonText }}</el-button>
  </div>
</template>

<script setup lang="ts">
interface Props {
  id: number
  title: string
  description?: string
  buttonText: string
}

// Define props with defaults where appropriate
const props = withDefaults(defineProps<Props>(), {
  buttonText: 'Submit',
  description: ''
})

// Define emits
defineEmits<{
  (e: 'action', id: number): void
}>()
</script>
```

#### State Management

- Use Pinia stores for global state management
- Keep store modules focused on specific domains
- Use TypeScript for type-safe state
- Define clear interfaces for state
- Use getters for derived state
- Use actions for asynchronous operations

Example store:

```typescript
// src/store/counter.ts
import { defineStore } from 'pinia'

interface CounterState {
  count: number
  lastUpdated: Date | null
}

export const useCounterStore = defineStore('counter', {
  state: (): CounterState => ({
    count: 0,
    lastUpdated: null
  }),

  getters: {
    doubleCount: (state) => state.count * 2
  },

  actions: {
    increment() {
      this.count++
      this.lastUpdated = new Date()
    },
    async fetchCount() {
      const response = await apiGet('/count')
      this.count = response.data.count
      this.lastUpdated = new Date()
    }
  },

  // Optional: persist state to localStorage
  persist: true
})
```

#### API Service Layer

- Create service modules for different API endpoints
- Use the base API client for all requests
- Handle errors consistently
- Use TypeScript for request and response types
- Consider offline scenarios

Example service:

```typescript
// src/services/userService.ts
import { apiGet, apiPost, apiPut, apiDelete } from '@/services/api'
import type { User, UserCreateInput, UserUpdateInput } from '@/types/user'

export async function getUsers() {
  return apiGet<User[]>('/users')
}

export async function getUser(id: number) {
  return apiGet<User>(`/users/${id}`)
}

export async function createUser(data: UserCreateInput) {
  return apiPost<User>('/users', data)
}

export async function updateUser(id: number, data: UserUpdateInput) {
  return apiPut<User>(`/users/${id}`, data)
}

export async function deleteUser(id: number) {
  return apiDelete<void>(`/users/${id}`)
}
```

#### Offline Support

When working with offline features:

- Use the offline cache for GET requests that should work offline
- Queue mutations (POST, PUT, DELETE) for later execution
- Handle synchronization conflicts appropriately
- Provide clear feedback to users about offline status
- Test both online and offline scenarios

Example offline-aware component:

```vue
<template>
  <div>
    <el-alert v-if="syncStore.hasPendingActions" type="info">
      {{ syncStore.pendingCount }} actions pending synchronization
    </el-alert>

    <user-list :users="users" />

    <el-button @click="syncStore.syncNow" :loading="syncStore.isSyncing">
      Sync Now
    </el-button>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useOfflineSyncStore } from '@/store/offlineSync'
import { getUsers } from '@/services/userService'
import type { User } from '@/types/user'

const users = ref<User[]>([])
const syncStore = useOfflineSyncStore()

onMounted(async () => {
  try {
    const response = await getUsers()
    users.value = response.data
  } catch (error) {
    // Handle error (will use cached data if offline)
  }
})
</script>
```

#### Form Handling

- Use Element Plus form components
- Implement client-side validation
- Handle form submission asynchronously
- Provide clear feedback on validation errors
- Consider offline form submission

Example form component:

```vue
<template>
  <el-form :model="form" :rules="rules" ref="formRef">
    <el-form-item prop="email" label="Email">
      <el-input v-model="form.email" type="email" />
    </el-form-item>

    <el-form-item prop="password" label="Password">
      <el-input v-model="form.password" type="password" />
    </el-form-item>

    <el-button type="primary" @click="submitForm" :loading="isSubmitting">
      Submit
    </el-button>
  </el-form>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import type { FormInstance, FormRules } from 'element-plus'

const formRef = ref<FormInstance>()
const isSubmitting = ref(false)

const form = reactive({
  email: '',
  password: ''
})

const rules: FormRules = {
  email: [
    { required: true, message: 'Email is required', trigger: 'blur' },
    { type: 'email', message: 'Please enter a valid email', trigger: 'blur' }
  ],
  password: [
    { required: true, message: 'Password is required', trigger: 'blur' },
    { min: 8, message: 'Password must be at least 8 characters', trigger: 'blur' }
  ]
}

const submitForm = async () => {
  if (!formRef.value) return

  try {
    await formRef.value.validate()
    isSubmitting.value = true

    // Submit form data
    await apiPost('/login', form)

    // Handle success
  } catch (error) {
    // Handle validation or API errors
  } finally {
    isSubmitting.value = false
  }
}
</script>
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

## frontend api

the frontend api is located in frontend/src/api
this directory is generated and must be never modified but used as is.
if you change  something in the backend related to the endpoints , you have to regenerate the frontend/src/api directory by typing:

```
make generate-api
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

