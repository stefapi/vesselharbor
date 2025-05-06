# Présentation du projet

Ce dépôt contient une application **full-stack** découpée en :

1. **Backend Python**  
   - Framework : FastAPI  
   - Gestion de la configuration : `pydantic` & fichiers `.env`  
   - Persistance : SQLAlchemy (→ base de données relationnelle, par défaut PostgreSQL)  
   - CLI utilitaire : `click`  
   - Gestion des dépendances : **poetry**

2. **Frontend Vue 3**  
   - Vite comme bundler & serveur de dev  
   - Pinia pour le state-management  
   - Vue-Router pour la navigation  
   - UnoCSS pour la couche CSS utilitaire (+ Explorateur intégré)  
   - PWA prête via `vite-plugin-pwa`  
   - Tests e2e : Playwright  
   - Tests unitaires : Vitest  
   - Gestion des dépendances : **pnpm**

Le backend écoute par défaut sur le port **8010** (Swagger UI : `/docs`) et le frontend de développement sur **5173** (hot-reload).  
Un conteneur Docker unique peut servir l’application compilée, ou plusieurs services peuvent être orchestrés via **docker-compose** (backend, frontend, base de données).

---

## Installation & lancement rapides

### Prérequis

• Docker ≥ 20.10  
• docker-compose v2  
• Node .js ≥ 18 + pnpm ≥ 8 (pour le dev frontend)  
• Python ≥ 3.13 + poetry ≥ 1.8 (pour le dev backend)

### Clonage

```shell script
git clone https://<votre-forguerie>/<orga>/<repo>.git
cd <repo>
```


---

## 1. Démarrage avec Docker 🐳

### 1.1 Image tout-en-un

```shell script
# Construction
docker build -t monapp:latest .

# Exécution (port 80 externe ⇒ 80 interne)
docker run -d --name monapp -p 80:80 monapp:latest
```


Visitez : `http://localhost/` pour le front et `http://localhost/docs` pour l’API.

### 1.2 Stack complète via docker-compose

```shell script
# Lancement
docker compose up --build -d

# Arrêt
docker compose down
```


Services typiques déclarés dans `docker-compose.yml` :

| Service      | Port hôte | Rôle                            |
|--------------|-----------|--------------------------------|
| db           | 5432      | PostgreSQL                     |
| backend      | 8010      | API FastAPI                    |
| frontend     | 80        | Fichiers statiques Vite build  |
| nginx (opt.) | 80 / 443  | Reverse-proxy & TLS            |

Avant le premier `up`, copiez le fichier d’exemple d’environnement :

```shell script
cp .env.example .env          # secrets applicatifs
cp backend/.env.example backend/.env
```


Adaptez au besoin :

```
POSTGRES_PASSWORD=********
DATABASE_URL=postgresql+asyncpg://postgres:********@db:5432/monapp
API_HOST=0.0.0.0
API_PORT=8010
MODE=production
```


---

## 2. Environnement de développement

### 2.1 Backend

```shell script
cd backend
poetry install                # installe les dépendances
cp .env.example .env          # variables d’environnement locales

# Lancer le serveur auto-reload
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8010
```


Tests :

```shell script
poetry run pytest
```


Migration (si Alembic est utilisé) :

```shell script
poetry run alembic upgrade head
```


### 2.2 Frontend

```shell script
cd frontend
pnpm install                  # installe les dépendances
pnpm dev                      # démarre Vite (http://localhost:5173)
```


Outils intégrés :

| Outil                     | URL locale                                            |
|---------------------------|-------------------------------------------------------|
| UnoCSS Explorer           | `http://localhost:5173/__unocss`                     |
| Vite Inspector            | `http://localhost:5173/__inspect/`                   |
| Vue 3 DevTools            | `http://localhost:5173/__devtools__/`                |

Tests :

```shell script
# Unités & composants
pnpm test:unit               # (alias vitest)

# End-to-end
pnpm test:e2e                # (alias playwright test)
```


### 2.3 Hot reload cross-stack

Pour coder simultanément sur le front et le back :

1. Lancez Postgres via Docker (ou un service local).  
2. Démarrez le backend en mode `--reload`.  
3. Démarrez le frontend avec `pnpm dev`.  
4. Ouvrez http://localhost:5173 ; toute sauvegarde de fichier entraîne un rafraîchissement automatique.

---

## 3. Structure des dossiers (vue d’ensemble)

```
<repo>/
├── backend/                 # API FastAPI
│   ├── app/                 # code source Python
│   ├── tests/
│   └── pyproject.toml
├── frontend/                # Vue 3 + Vite
│   ├── src/
│   ├── public/
│   └── vitest.config.ts
├── docker/                  # Dockerfiles additionnels
├── docker-compose.yml
├── .env.example             # variables globales
└── README.md
```


---

## 4. Personnalisation & configuration

• **Base de données** : changez `DATABASE_URL` dans `backend/.env`.  
• **CORS** : ajustez `settings.py` (liste `ALLOWED_ORIGINS`).  
• **Port front** : modifiez `frontend/vite.config.ts`.  
• **PWA** : éditez `frontend/vite.config.ts` section `pwa`, puis exécutez `pnpm build`.

---

## 5. Déploiement (production)

1. Construisez les images : `docker compose build --no-cache`.  
2. Poussez-les sur votre registry Docker.  
3. Sur le serveur cible, récupérez vos `docker-compose.yml` & `.env` puis :  

```shell script
docker compose pull
docker compose up -d
```


Ajoutez un **reverse-proxy** (Traefik, Nginx, Caddy) pour gérer TLS / HTTP-2.

---

## 6. Ressources utiles

• Swagger / Redoc : `http://localhost:8010/docs` & `/redoc`  
• Logs de conteneur : `docker compose logs -f backend`  
• Couverture tests front : `pnpm coverage` (rapport HTML dans `coverage/`)  

---

Bon développement !
