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

## Testing Guidelines

When making changes to the codebase, Junie should run the appropriate tests to ensure the correctness of the solution:

### Backend Tests
```bash
cd app
poetry run pytest
```

### Frontend Tests
```bash
cd frontend
pnpm test:unit  # For unit tests
pnpm test:e2e   # For end-to-end tests
```

## Build Instructions

Before submitting changes, Junie should verify that the project builds correctly:

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

- **Python**: Follow PEP 8 guidelines for Python code
- **TypeScript/JavaScript**: Follow the project's ESLint configuration
- **Vue Components**: Use the Composition API with `<script setup>` syntax
- **CSS**: Use UnoCSS utility classes for styling

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

For more details, see [Git Workflow](.junie/git_workflow.md).

## Debugging and Development Tools

### Backend Debugging
- Use `import pdb; pdb.set_trace()` for breakpoints
- Enable FastAPI debug mode with `--reload` flag
- Use logging with appropriate levels

### Frontend Debugging
- Use Vue DevTools browser extension
- Use browser console for logging
- Use Vite Inspector at http://localhost:5173/__inspect/

### Development Tools
- UnoCSS Explorer: http://localhost:5173/__unocss
- Vue 3 DevTools: http://localhost:5173/__devtools__/

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
- Logical Architecture (`.junie/logical_architecture.md`)
- Changelog (`.junie/changelog.md`)
