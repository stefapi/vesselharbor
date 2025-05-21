# Project Architecture

This document outlines the architecture of the FastAPI Vue Template project.

## Overview

The project follows a modern web application architecture with a clear separation between the backend and frontend:

- **Backend**: FastAPI-based RESTful API
- **Frontend**: Vue.js 3 single-page application (SPA)
- **Deployment**: Docker containerization for both development and production

## Backend Architecture

### Technology Stack

- **Framework**: FastAPI (Python)
- **Database**: SQLAlchemy ORM with SQLite/PostgreSQL
- **Authentication**: JWT-based authentication
- **API Documentation**: Swagger UI and ReDoc (auto-generated)

### Directory Structure

```
app/
├── alembic/            # Database migrations
├── api/                # API endpoints
│   ├── deps.py         # Dependency injection
│   ├── routes/         # API route definitions
│   └── ...
├── core/               # Core application components
│   ├── config.py       # Configuration management
│   ├── security.py     # Security utilities
│   └── ...
├── db/                 # Database models and session management
├── models/             # Pydantic models for request/response
├── schemas/            # Pydantic schemas for validation
├── services/           # Business logic
├── tests/              # Test suite
└── main.py             # Application entry point
```

### Data Flow

1. Client sends HTTP request to API endpoint
2. Request is validated using Pydantic models
3. Dependencies are injected (auth, database session, etc.)
4. Business logic is executed in service layer
5. Response is formatted and returned to client

## Frontend Architecture

### Technology Stack

- **Framework**: Vue.js 3 with Composition API
- **State Management**: Pinia
- **Routing**: Vue Router
- **UI Components**: Custom components with UnoCSS
- **HTTP Client**: Axios
- **Testing**: Vitest (unit) and Playwright (e2e)

### Directory Structure

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
└── tests/              # Test suite
```

### Component Architecture

The frontend follows a component-based architecture:

- **Layouts**: Define the overall structure of pages
- **Views**: Page-level components that compose smaller components
- **Components**: Reusable UI elements
- **Composables**: Reusable logic extracted into composition functions

## Authentication Flow

1. User submits credentials via login form
2. Backend validates credentials and issues JWT token
3. Frontend stores token in localStorage/cookie
4. Token is included in Authorization header for subsequent requests
5. Protected routes check for valid token before rendering

## Deployment Architecture

### Development Environment

- Backend and frontend run as separate services
- Hot-reloading enabled for both
- Local database for development

### Production Environment

- Single Docker image containing both backend and frontend
- Caddy as reverse proxy and static file server
- Environment variables for configuration
- Optional Kubernetes deployment via Helm charts

## Communication Between Components

- Frontend communicates with backend via RESTful API calls
- API responses follow consistent JSON structure
- Error handling is standardized across the application
