# Stage 1: Build du backend (FastAPI via Poetry)
FROM python:3.9-slim as backend-builder
WORKDIR /app
# Copier les fichiers de configuration de Poetry
COPY app/pyproject.toml app/poetry.lock /app/
# Installer Poetry et les dépendances (sans créer d'environnement virtuel)
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev --no-root
# Copier le code backend
COPY app/ /app/

# Stage 2: Build du frontend (Vue3)
FROM node:16-alpine as frontend-builder
WORKDIR /app
COPY frontend/package.json frontend/package-lock.json* ./
RUN npm install
COPY frontend/ .
RUN npm run build

# Stage 3: Image finale
FROM python:3.9-alpine

# Installer Node, npm et Caddy
RUN apk add --no-cache nodejs npm caddy

WORKDIR /app

# Copier le backend construit depuis backend-builder
COPY --from=backend-builder /app /app

# Copier le frontend construit depuis frontend-builder
COPY --from=frontend-builder /app/dist /app/frontend/dist

# Copier le fichier Caddyfile et le script de démarrage
COPY Caddyfile /etc/caddy/Caddyfile
COPY start.sh /start.sh
RUN chmod +x /start.sh

# Exposer le port 80 (qui sera mappé sur le port 3000 lors de l'exécution)
EXPOSE 80

CMD ["/start.sh"]

