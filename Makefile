# ============================================================================
# VARIABLES
# ============================================================================

# Core tools
PYTHON ?= python3
LIBRARY = app
POETRY ?= poetry
PNPM ?= pnpm
NODE ?= node
DOCKER ?= docker
DOCKER_COMPOSE ?= docker-compose
ALEMBIC ?= alembic

# Python paths
PYTHON_VERSION = $(shell $(PYTHON) -c "from distutils.sysconfig import get_python_version; print(get_python_version())")
SITELIB = $(shell $(PYTHON) -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
VENV_BASE ?= ./venv

# Git and versioning
GIT_BRANCH ?= $(shell git rev-parse --abbrev-ref HEAD)
VERSION = $(shell git describe --long --first-parent 2>/dev/null || echo "0.1.0-dev")
RELEASE_VERSION = $(shell git describe --long --first-parent 2>/dev/null | sed 's@\([0-9.]\{1,\}\).*@\1@' || echo "0.1.0")

# Docker compose settings
COMPOSE_TAG ?= $(GIT_BRANCH)
COMPOSE_HOST ?= $(shell hostname)

# ============================================================================
# HELPER SCRIPTS
# ============================================================================

define BROWSER_PYSCRIPT
import os, webbrowser, sys
from urllib.request import pathname2url
webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

define PRINT_HELP_PYSCRIPT
import re, sys
for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

define APP_PYSCRIPT
from $(LIBRARY) import main
app = main.app
app.run()
endef
export APP_PYSCRIPT

BROWSER := $(PYTHON) -c "$$BROWSER_PYSCRIPT"

.ONESHELL:

# ============================================================================
# COMMON COMMANDS
# ============================================================================

help: ## Display help information about available commands
	@$(PYTHON) -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

outdated: ## 🚧 Check for outdated dependencies in both backend and frontend
	@echo "Checking backend dependencies..."
	$(POETRY) show --outdated
	@echo "\nChecking frontend dependencies..."
	cd frontend && $(PNPM) exec taze

setup: ## 🏗 Setup complete development environment
	$(POETRY) install --with dev
	cd frontend && $(PNPM) install
	$(POETRY) run pre-commit install
	cp -n template.env .env || true
	@echo "🏗  Development Setup Complete "
	@echo "❗️ Tips"
	@echo "    1. run 'make backend' to start the API server"
	@echo "    2. run 'make frontend' to start the frontend development server"
	@echo "    3. run 'make dev' to start both servers"

install: ## 📦 Install development version
	$(POETRY) install

# ============================================================================
# CLEANING COMMANDS
# ============================================================================

clean-data: ## ⚠️ Remove all developer data for a fresh start
	rm -rf ./dev/data/users/ 2>/dev/null || true
	rm -f ./dev/data/*.db 2>/dev/null || true
	rm -f ./dev/data/*.log 2>/dev/null || true
	rm -f ./dev/data/.secret 2>/dev/null || true

clean-build: ## 🧹 Clean Python build files
	rm -rf build dist .eggs
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-docs: ## 🧹 Clean documentation build
	rm -rf docs/_build

clean-tests: ## 🧹 Remove test and coverage artifacts
	rm -f .coverage
	rm -rf .tox
	rm -rf htmlcov
	rm -rf .pytest_cache

clean-pyc: ## 🧹 Remove Python file artifacts
	find ./$(LIBRARY) -type f -name '*.pyc' -delete
	find ./$(LIBRARY) -type f -name '*.log' -delete
	find ./$(LIBRARY) -type f -name '*~' -delete
	find ./$(LIBRARY) -name '__pycache__' -exec rm -fr {} +

clean-frontend: ## 🧹 Remove frontend build artifacts
	rm -rf $(LIBRARY)/dist

clean: clean-data clean-pyc clean-tests clean-frontend ## 🧹 Clean all build artifacts and temporary files

# ============================================================================
# BACKEND COMMANDS
# ============================================================================

backend-clean: clean-pyc clean-tests clean-frontend ## 🧹 Clean backend-specific artifacts
	rm -fr .mypy_cache

backend-typecheck: ## 🔍 Type check the backend code
	$(POETRY) run mypy $(LIBRARY)

backend-build: ## 🏗 Build backend package
	$(POETRY) build

backend-test: ## 🧪 Run backend tests
	$(POETRY) run pytest

backend-format: ## 🧺 Format backend code
	$(POETRY) run isort .
	$(POETRY) run black .

backend-lint: ## 🧹 Lint backend code
	$(POETRY) run isort --check-only .
	$(POETRY) run black --check .

backend-all: backend-format backend-lint backend-typecheck backend-test ## 🧪 Run all backend checks and tests

backend-coverage: ## ☂️ Generate and view test coverage report
	$(POETRY) run pytest
	$(POETRY) run coverage report -m
	$(POETRY) run coverage html
	$(BROWSER) htmlcov/index.html

.PHONY: backend
backend: ## 🎬 Start backend development server
	$(POETRY) run uvicorn app.main:app --reload --host 0.0.0.0 --port $$($(PYTHON) -c "import os; print(os.getenv('PORT', '8010'))")

# ============================================================================
# FRONTEND COMMANDS
# ============================================================================

frontend-clean: ## 🧹 Clean frontend build artifacts
	rm -rf frontend/dist
	rm -rf frontend/node_modules/.vite

frontend-install: ## 📦 Install frontend dependencies
	cd frontend && $(PNPM) install

frontend-build: ## 🏗 Build frontend for production
	cd frontend && $(PNPM) build

frontend-build-prod: ## 🏗 Build frontend and copy to app directory
	cd frontend && $(PNPM) build-prod

frontend-dev: ## 🎬 Start frontend development server
	cd frontend && $(PNPM) dev

frontend-start: ## 🎬 Start frontend server from output directory
	cd frontend && $(PNPM) start

frontend-preview: ## 🔍 Preview production build locally
	cd frontend && $(PNPM) preview

frontend-preview-local: ## 🔍 Preview local build with serve
	cd frontend && $(PNPM) preview:local

frontend-preview-dist: ## 🔍 Preview app directory build with serve
	cd frontend && $(PNPM) preview:dist

frontend-lint: ## 🧹 Lint frontend code
	cd frontend && $(PNPM) lint

frontend-lint-check: ## 🧹 Check frontend code for linting issues
	cd frontend && $(PNPM) lint-check

frontend-lint-fix: ## 🧹 Fix frontend linting issues
	cd frontend && $(PNPM) lint-fix

frontend-css-check: ## 🧹 Check frontend CSS for style issues
	cd frontend && $(PNPM) css-check

frontend-css-fix: ## 🧹 Fix frontend CSS style issues
	cd frontend && $(PNPM) css-fix

frontend-format: ## 🧺 Format frontend code
	cd frontend && $(PNPM) format

frontend-test: ## 🧪 Run frontend unit tests
	cd frontend && $(PNPM) test:ci

frontend-test-e2e: ## 🧪 Run frontend end-to-end tests
	cd frontend && $(PNPM) test:e2e:dev

frontend-test-e2e-ui: ## 🧪 Run frontend end-to-end tests with UI
	cd frontend && $(PNPM) test:e2eui:dev

frontend-test-record: ## 🎥 Record frontend end-to-end tests
	cd frontend && $(PNPM) test:record:dev

frontend-typecheck: ## 🔍 Type check frontend code
	cd frontend && $(PNPM) typecheck

frontend-sizecheck: ## 📊 Analyze frontend bundle size
	cd frontend && $(PNPM) sizecheck

frontend-unlighthouse: ## 🔍 Run Unlighthouse for performance testing
	cd frontend && $(PNPM) unlighthouse

frontend-generate: ## 🏗 Generate code for frontend
	$(POETRY) run python dev/code-generation/gen_frontend_types.py

frontend-all: frontend-format frontend-lint frontend-css-check frontend-typecheck frontend-test ## 🧪 Run all frontend checks and tests

.PHONY: frontend
frontend: ## 🎬 Start frontend development server
	cd frontend && $(PNPM) dev --open

# ============================================================================
# DEVELOPMENT COMMANDS
# ============================================================================

vagrant-up: ## 🚀 Start Vagrant development server
	vagrant up

vagrant-ssh: ## 🔌 SSH into Vagrant server
	vagrant ssh

purge: clean ## 🧹 Remove everything for a fresh environment
	rm -rf ./dev/data 2>/dev/null || true
	$(POETRY) env remove --all

migrate: ## 🗃️ Generate database migration
	$(POETRY) run $(ALEMBIC) revision --autogenerate -m "migration_to_be_named"

format: backend-format frontend-format ## 🧺 Format all code (backend and frontend)

lint: backend-lint frontend-lint ## 🧹 Lint all code (backend and frontend)

test: backend-test frontend-test ## 🧪 Run all tests (backend and frontend)

serve: ## 🎬 Serve client and server separately
	$(POETRY) run $(PYTHON) -c "$$APP_PYSCRIPT"

run: ## 🎬 Run server in production mode
	$(POETRY) run uvicorn app.main:app --host 0.0.0.0 --port $$($(PYTHON) -c "import os; print(os.getenv('PORT', '8010'))")

.PHONY: dev
dev: ## 🎬 Start both backend and frontend development servers
	@echo "Starting backend and frontend servers..."
	@(trap 'kill 0' SIGINT; \
		$(MAKE) backend & \
		$(MAKE) frontend & \
		wait)

# ============================================================================
# DOCUMENTATION COMMANDS
# ============================================================================

.PHONY: docs
docs: ## 📄 Generate and serve documentation
	cd docs && $(POETRY) run $(PYTHON) -m mkdocs serve

# ============================================================================
# DEPLOYMENT COMMANDS
# ============================================================================

prepare: ## 🏗 Prepare for deployment
	$(POETRY) export --output requirements.txt

.PHONY: dist
dist: clean prepare backend-build frontend-build ## 📦 Create distribution files

release: clean dist ## 🚀 Build and publish to PyPI
	$(POETRY) publish

release-install: ## 📥 Install production version from PyPI
	pip install $(LIBRARY) --break-system-packages

stage: clean dist ## 🧪 Build and publish to TestPyPI
	$(POETRY) config repositories.testpypi https://test.pypi.org/legacy/
	$(POETRY) publish -r testpypi

stage-install: ## 📥 Install testing version from TestPyPI
	pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ $(LIBRARY) --break-system-packages

# ============================================================================
# DOCKER COMMANDS
# ============================================================================

docker-build-backend: ## 🐳 Build backend Docker image
	$(DOCKER) build -t myorg/backend:latest -f Dockerfile .

docker-build-frontend: ## 🐳 Build frontend Docker image
	$(DOCKER) build -t myorg/frontend:latest -f frontend/Dockerfile frontend

docker-build: docker-build-backend docker-build-frontend ## 🐳 Build all Docker images

docker-up: ## 🐳 Start Docker containers
	$(DOCKER_COMPOSE) up -d

docker-down: ## 🐳 Stop Docker containers
	$(DOCKER_COMPOSE) down

docker-logs: ## 🐳 View Docker logs
	$(DOCKER_COMPOSE) logs -f

docker-dev: ## 🐳 Start Docker development stack
	$(DOCKER_COMPOSE) -f docker-compose.yml -f docker-compose.override.yml -p dev-$(LIBRARY) down && \
	$(DOCKER_COMPOSE) -f docker-compose.yml -f docker-compose.override.yml -p dev-$(LIBRARY) up --build

docker-prod: ## 🐳 Start Docker production stack
	$(DOCKER_COMPOSE) -f docker-compose.yml -p $(LIBRARY) up --build

# ============================================================================
# CODE GENERATION COMMANDS
# ============================================================================

code-gen: ## 🤖 Generate API routes
	$(POETRY) run dev/scripts/app_routes_gen.py

generate-api: ## 🔄 Regenerate TypeScript API client from backend routes
	$(POETRY) run python dev/scripts/daemon_routes_gen.py

generate-openapi-docs: ## 📋 Generate comprehensive OpenAPI specification in .junie directory
	$(POETRY) run python dev/scripts/generate_openapi_junie.py

# ============================================================================
# ALL-IN-ONE COMMANDS
# ============================================================================

all: clean setup format lint test dev ## 🚀 Complete setup, format, lint, test, and run
