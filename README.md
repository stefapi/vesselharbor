# VesselHarbor

<div align="center">
  <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi" alt="FastAPI">
  <img src="https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D" alt="Vue.js">
  <img src="https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white" alt="Docker">
  <img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white" alt="TypeScript">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
</div>

<p align="center">
  <em>A self-hosted platform for managing containerized applications and virtual machines with a focus on simplicity</em>
</p>

VesselHarbor is a self-hosted platform for managing and orchestrating containerized applications and virtual machines, similar to platforms like Heroku or Vercel. It provides a comprehensive solution for infrastructure management.

### 🖥️ Infrastructure Management

- **Container Orchestration**: Support for Docker, Docker Compose, and Docker Swarm deployments
- **Virtual Machine Management**: Deploy and manage VMs alongside containers
- **Network Infrastructure**: Advanced network structure management and interconnections
- **Gateway Management**: Configurable gateways with cascading capabilities
- **Resource Monitoring**: Real-time monitoring of system resources, container, and VM performance
- **Application Deployment**: Components deployed as application stacks on managed clusters

### 🔌 Integration & Connectivity

- **SSO Integration**: Connect with Single Sign-On providers for centralized authentication
- **Custom Network Configuration**: Easily configure networking between containers, VMs, and external access
- **API Connectivity**: Comprehensive API for integration with external systems
- **Multi-user Access**: Role-based access control for team collaboration

### 📦 Application Management

- **Application Catalog**: One-click installation of popular applications from a curated catalog
- **Automated Updates**: Keep your applications up-to-date with automated update checks and deployment
- **Backup & Restore**: Scheduled backups and easy restoration of your applications and data
- **Volume Management**: Simplified management of persistent data volumes
- **Health Checks**: Automated monitoring of application health with notification alerts

### 🧩 Extensible Components

VesselHarbor components can dynamically add functionality to your infrastructure:

- **Database Services**: PostgreSQL, MySQL, MongoDB, Redis, and more
- **Storage Solutions**: MinIO and various storage backends
- **Reverse Proxies**: Multiple reverse proxy options for routing and load balancing
- **Custom Services**: Extend with your own service components



## ✨ Features

- **Modern Stack**: FastAPI backend + Vue 3 frontend with TypeScript
- **Docker Ready**: Containerized development and production environments
- **Authentication**: JWT-based authentication system
- **Database**: SQLAlchemy ORM with PostgreSQL
- **API Documentation**: Auto-generated with Swagger UI and ReDoc
- **State Management**: Pinia for predictable state management
- **Styling**: UnoCSS for utility-first CSS
- **Testing**: Comprehensive testing setup with pytest, Vitest, and Playwright
- **Hot Reload**: Development environment with hot reload for both frontend and backend
- **PWA Support**: Progressive Web App ready with vite-plugin-pwa

## 🚢 What is VesselHarbor?

The name "VesselHarbor" carries a dual meaning: "Vessel" refers to containerization (Docker containers), while "Harbor" represents a safe haven for self-hosting applications without worrying about complex technical details. Just as a harbor provides shelter and organization for ships, VesselHarbor offers a secure and simplified environment for managing your containerized applications.

## 🚀 Quick Start

### Prerequisites

- Docker ≥ 20.10 and docker-compose v2
- Node.js ≥ 18 and pnpm ≥ 8 (for frontend development)
- Python ≥ 3.13 and poetry ≥ 1.8 (for backend development)

### Using Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/VesselHarbor.git
cd VesselHarbor

# Copy environment files
cp .env.example .env
cp backend/.env.example backend/.env

# Start the application
docker compose up --build -d
```

Visit:
- Frontend: http://localhost/
- API Documentation: http://localhost/docs

## 📖 Documentation

Comprehensive documentation is available in the `.junie` directory:

- [API Endpoints](.junie/api-endpoints.md)
- [Architecture](.junie/architecture.md)
- [Authentication](.junie/authentication.md)
- [Project Guidelines](.junie/guidelines.md)
- [Changelog](.junie/changelog.md)

## 💻 Development

### Backend (FastAPI)

```bash
cd app
poetry install
cp .env.example .env

# Start development server with auto-reload
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8010

# Run tests
poetry run pytest
```

Visit:
- Frontend: http://localhost/
- API Documentation: http://localhost/docs

### Frontend (Vue 3)

```bash
cd frontend
pnpm install
pnpm dev  # Starts Vite dev server at http://localhost:5173

# Run unit tests
pnpm test:unit

# Run end-to-end tests
pnpm test:e2e
```

### Full-Stack Development

For simultaneous frontend and backend development:

1. Start PostgreSQL via Docker or a local service
2. Start the backend with hot reload
3. Start the frontend dev server
4. Access the application at http://localhost:5173

Before the first `up`, copy the environment example files:

```bash
cp .env.example .env          # Application secrets
cp backend/.env.example backend/.env
```

Adjust as needed:

```
POSTGRES_PASSWORD=********
DATABASE_URL=postgresql+asyncpg://postgres:********@db:5432/monapp
API_HOST=0.0.0.0
API_PORT=8010
MODE=production
```

## 🔧 Configuration

- **Database**: Change `DATABASE_URL` in `backend/.env`
- **CORS**: Adjust `BACKEND_CORS_ORIGINS` in `backend/.env`
- **Frontend Port**: Modify `frontend/vite.config.ts`
- **PWA**: Edit the `pwa` section in `frontend/vite.config.ts`

## 🚢 Deployment

### Production Deployment

1. Build Docker images: `docker compose build --no-cache`
2. Push to your Docker registry
3. On your server, pull and start the containers:

```bash
docker compose pull
docker compose up -d
```

For production environments, add a reverse proxy (Traefik, Nginx, Caddy) to handle TLS/HTTP-2.

## 🤝 Contributing

Contributions are welcome! Please check our [Contributing Guidelines](.junie/contributing.md) before submitting pull requests.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgements

- [FastAPI](https://fastapi.tiangolo.com/)
- [Vue.js](https://vuejs.org/)
- [Pinia](https://pinia.vuejs.org/)
- [UnoCSS](https://github.com/unocss/unocss)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Docker](https://www.docker.com/)
