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
  <em>Self‑hosted application harbor & orchestrator — one‑click install, rock‑solid security, zero‑headache maintenance</em>
</p>

---

VesselHarbor is a self-hosted platform for managing and orchestrating containerized applications and virtual machines, similar to platforms like Heroku or Vercel. It provides a comprehensive solution for infrastructure management.

## 🖥️ Infrastructure Management

* **Container & VM orchestration** — Docker, Docker Compose, Swarm and KVM‑based virtual machines side‑by‑side
* **Cluster aware** — manage multiple nodes from a single dashboard; automatic service discovery
* **Network fabric** — encrypted overlay networks and service mesh out‑of‑the‑box
* **Gateway & ingress** — Layer‑4/7 reverse proxy with automatic TLS, wildcard & Wildcard+SAN certificates
* **Resource insight** — live CPU, RAM, disk & network monitoring for every workload

## 🔌 Connectivity & Extensibility

* **SSO everywhere** — OAuth2 / OpenID Connect, LDAP and SAML providers supported
* **Fine‑grained RBAC** — role & project based access for teams and external collaborators
* **REST & WebSocket API** — automate everything; first‑class Terraform provider coming soon
* **Add‑on engine** — databases (PostgreSQL, MySQL, MongoDB, Redis), object storage (MinIO, S3), message queues (NATS, RabbitMQ) and more can be installed as add‑ons and shared between apps

## 📦 Application Experience

* **Curated App Store** —  pre‑packaged images adapted for VesselHarbor with health‑checks, backups and sane defaults
* **One‑click updates** — rolling updates with automatic rollback on failure
* **Continuous backups** — incremental, encrypted and delta‑compressed backups to any S3 compatible storage
* **Self‑healing** — automatic restarts, replica rescheduling and service dependency checks
* **Metrics & alerts** — Prometheus‑compatible metrics endpoint and pluggable alert receivers (Email, Discord, Slack, Matrix)

## 🚢 What's in a Name?

> *Vessel*: a container, **Harbor**: a safe port. VesselHarbor offers a safe haven for your containers and virtual machines, guarding them against storms of complexity.



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

Full documentation lives in the `.junie` directory of the repository:

* [API Reference](.junie/api-endpoints.md)
* [System Architecture](.junie/architecture.md)
* [Security Model](.junie/security.md)
* [User Guide](.junie/user-guide.md)

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

Found a bug, have an idea or want to add a new app to the catalogue? Check the [Contributing Guidelines](.junie/contributing.md) and join the discussion in the GitHub issues.

## 📄 License

VesselHarbor is released under the **MIT License**. See [LICENSE](LICENSE) for details.

## 🙏 Acknowledgements

VesselHarbor stands on the shoulders of giants — thank you to the communities behind FastAPI, Vue, Docker and all the amazing self‑hosting projects that inspired this work.
