# Makefile Commands Documentation

This document provides comprehensive information about the Makefile commands available in the VesselHarbor project. The Makefile includes commands for development, testing, building, and deployment.

## Common Commands

| Command | Description |
|---------|-------------|
| `make help` | Display help information about available commands |
| `make outdated` | Check for outdated dependencies in both backend and frontend |
| `make setup` | Setup complete development environment |
| `make install` | Install development version |
| `make clean` | Clean all build artifacts and temporary files |
| `make format` | Format all code (backend and frontend) |
| `make lint` | Lint all code (backend and frontend) |
| `make test` | Run all tests (backend and frontend) |
| `make dev` | Start both backend and frontend development servers |

## Backend Commands

| Command | Description |
|---------|-------------|
| `make backend` | Start backend development server |
| `make backend-clean` | Clean backend-specific artifacts |
| `make backend-typecheck` | Type check the backend code |
| `make backend-build` | Build backend package |
| `make backend-test` | Run backend tests |
| `make backend-format` | Format backend code |
| `make backend-lint` | Lint backend code |
| `make backend-all` | Run all backend checks and tests |
| `make backend-coverage` | Generate and view test coverage report |

## Frontend Commands

| Command | Description |
|---------|-------------|
| `make frontend` | Start frontend development server |
| `make frontend-clean` | Clean frontend build artifacts |
| `make frontend-install` | Install frontend dependencies |
| `make frontend-build` | Build frontend for production |
| `make frontend-build-prod` | Build frontend and copy to app directory |
| `make frontend-dev` | Start frontend development server |
| `make frontend-start` | Start frontend server from output directory |
| `make frontend-preview` | Preview production build locally |
| `make frontend-preview-local` | Preview local build with serve |
| `make frontend-preview-dist` | Preview app directory build with serve |
| `make frontend-lint` | Lint frontend code |
| `make frontend-lint-check` | Check frontend code for linting issues |
| `make frontend-lint-fix` | Fix frontend linting issues |
| `make frontend-css-check` | Check frontend CSS for style issues |
| `make frontend-css-fix` | Fix frontend CSS style issues |
| `make frontend-format` | Format frontend code |
| `make frontend-test` | Run frontend unit tests |
| `make frontend-test-e2e` | Run frontend end-to-end tests |
| `make frontend-test-e2e-ui` | Run frontend end-to-end tests with UI |
| `make frontend-test-record` | Record frontend end-to-end tests |
| `make frontend-typecheck` | Type check frontend code |
| `make frontend-sizecheck` | Analyze frontend bundle size |
| `make frontend-unlighthouse` | Run Unlighthouse for performance testing |
| `make frontend-generate` | Generate code for frontend |
| `make frontend-all` | Run all frontend checks and tests |

## Cleaning Commands

| Command | Description |
|---------|-------------|
| `make clean-data` | Remove all developer data for a fresh start |
| `make clean-build` | Clean Python build files |
| `make clean-docs` | Clean documentation build |
| `make clean-tests` | Remove test and coverage artifacts |
| `make clean-pyc` | Remove Python file artifacts |
| `make clean-frontend` | Remove frontend build artifacts |
| `make clean` | Clean all build artifacts and temporary files |

## Development Commands

| Command | Description |
|---------|-------------|
| `make vagrant-up` | Start Vagrant development server |
| `make vagrant-ssh` | SSH into Vagrant server |
| `make purge` | Remove everything for a fresh environment |
| `make migrate` | Generate database migration |
| `make serve` | Serve client and server separately |
| `make run` | Run server in production mode |

## Documentation Commands

| Command | Description |
|---------|-------------|
| `make docs` | Generate and serve documentation |

## Deployment Commands

| Command | Description |
|---------|-------------|
| `make prepare` | Prepare for deployment |
| `make dist` | Create distribution files |
| `make release` | Build and publish to PyPI |
| `make release-install` | Install production version from PyPI |
| `make stage` | Build and publish to TestPyPI |
| `make stage-install` | Install testing version from TestPyPI |

## Docker Commands

| Command | Description |
|---------|-------------|
| `make docker-build-backend` | Build backend Docker image |
| `make docker-build-frontend` | Build frontend Docker image |
| `make docker-build` | Build all Docker images |
| `make docker-up` | Start Docker containers |
| `make docker-down` | Stop Docker containers |
| `make docker-logs` | View Docker logs |
| `make docker-dev` | Start Docker development stack |
| `make docker-prod` | Start Docker production stack |

## Code Generation Commands

| Command | Description |
|---------|-------------|
| `make code-gen` | Generate API routes |

## All-in-One Commands

| Command | Description |
|---------|-------------|
| `make all` | Complete setup, format, lint, test, and run |

## Examples

### Setting Up Development Environment

```bash
# Clone the repository
git clone https://github.com/yourusername/vesselharbor.git
cd vesselharbor

# Set up the development environment
make setup

# Start both backend and frontend development servers
make dev
```

### Running Tests

```bash
# Run all tests
make test

# Run backend tests only
make backend-test

# Run frontend tests only
make frontend-test

# Run backend tests with coverage
make backend-coverage

# Run frontend end-to-end tests
make frontend-test-e2e
```

### Code Quality

```bash
# Format all code
make format

# Lint all code
make lint

# Type check backend code
make backend-typecheck

# Type check frontend code
make frontend-typecheck
```

### Building for Production

```bash
# Build backend and frontend for production
make dist

# Build and publish to PyPI
make release

# Build Docker images
make docker-build

# Start Docker production stack
make docker-prod
```

### Cleaning Up

```bash
# Clean all build artifacts
make clean

# Remove everything for a fresh environment
make purge
```

## Environment Variables

The Makefile uses several environment variables that can be overridden:

- `PYTHON`: Path to Python executable (default: `python3`)
- `POETRY`: Path to Poetry executable (default: `poetry`)
- `PNPM`: Path to PNPM executable (default: `pnpm`)
- `NODE`: Path to Node.js executable (default: `node`)
- `DOCKER`: Path to Docker executable (default: `docker`)
- `DOCKER_COMPOSE`: Path to Docker Compose executable (default: `docker-compose`)
- `VENV_BASE`: Base directory for Python virtual environments (default: `./venv`)
- `GIT_BRANCH`: Git branch name (default: current branch)
- `COMPOSE_TAG`: Tag for Docker Compose images (default: `GIT_BRANCH`)
- `COMPOSE_HOST`: Host for Docker Compose (default: current hostname)

Example of overriding environment variables:

```bash
PYTHON=/usr/bin/python3.10 POETRY=/usr/local/bin/poetry make setup
```

## Tips and Tricks

1. **Use `make help` for quick reference**: This command displays a list of available commands with brief descriptions.

2. **Development workflow**: Use `make dev` to start both backend and frontend development servers simultaneously.

3. **Code quality checks**: Use `make backend-all` and `make frontend-all` to run all checks and tests for backend and frontend respectively.

4. **Clean before building**: Use `make clean` before building to ensure a clean build.

5. **Continuous Integration**: The commands `make backend-all` and `make frontend-all` are useful for CI pipelines.

6. **Docker development**: Use `make docker-dev` to start a Docker-based development environment.

7. **Production deployment**: Use `make docker-prod` to start a Docker-based production environment.

8. **Database migrations**: Use `make migrate` to generate database migrations after model changes.
