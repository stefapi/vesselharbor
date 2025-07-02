# Structure du Projet

Ce document fournit une vue d'ensemble de la structure du projet FastAPI + Vue.js, expliquant l'organisation des répertoires et des fichiers clés.

## Structure Globale

```
VesselHarbor/
├── .github/                # Configuration GitHub (workflows CI/CD)
├── .junie/                 # Documentation et configuration centralisée
├── app/                    # Backend FastAPI
├── frontend/               # Frontend Vue.js
├── docker/                 # Fichiers de configuration Docker
├── .env.example            # Exemple de variables d'environnement
├── docker-compose.yml      # Configuration Docker Compose
├── Dockerfile              # Configuration Docker principale
└── Makefile                # Commandes Make pour le développement
```

## Backend (app/)

```
app/
├── alembic/                # Migrations de base de données
├── api/                    # Points d'accès API
│   ├── deps.py             # Dépendances d'injection FastAPI
│   ├── v1/                 # API version 1
│   │   ├── endpoints/      # Points d'accès par ressource
│   │   └── api.py          # Routeur API principal
├── core/                   # Fonctionnalités centrales
│   ├── config.py           # Configuration de l'application
│   ├── security.py         # Fonctions de sécurité
│   └── settings.py         # Paramètres de l'application
├── crud/                   # Opérations CRUD
├── db/                     # Configuration de la base de données
│   ├── base.py             # Classe de base SQLAlchemy
│   ├── init_db.py          # Initialisation de la base de données
│   └── session.py          # Session de base de données
├── models/                 # Modèles SQLAlchemy
├── schemas/                # Schémas Pydantic
├── tests/                  # Tests unitaires et d'intégration
├── utils/                  # Utilitaires
├── main.py                 # Point d'entrée de l'application
└── pyproject.toml          # Configuration Poetry
```

## Frontend (frontend/)

```
frontend/
├── public/                 # Fichiers statiques publics
├── src/                    # Code source
│   ├── assets/             # Ressources (images, styles)
│   ├── components/         # Composants Vue réutilisables
│   ├── composables/        # Composables Vue
│   ├── layouts/            # Layouts de l'application
│   ├── pages/              # Pages de l'application
│   ├── router/             # Configuration du routeur Vue
│   ├── services/           # Services API
│   ├── stores/             # Stores Pinia
│   ├── types/              # Types TypeScript
│   ├── utils/              # Fonctions utilitaires
│   ├── views/              # Vues de l'application
│   ├── App.vue             # Composant racine
│   └── main.ts             # Point d'entrée
├── tests/                  # Tests unitaires et e2e
├── index.html              # Page HTML principale
├── package.json            # Configuration npm/pnpm
├── tsconfig.json           # Configuration TypeScript
└── vite.config.ts          # Configuration Vite
```

## Fichiers Clés

### Backend

- **app/main.py**: Point d'entrée de l'application FastAPI
- **app/api/v1/api.py**: Routeur principal de l'API
- **app/core/config.py**: Configuration de l'application
- **app/db/session.py**: Configuration de la session de base de données
- **app/models/__init__.py**: Définition des modèles SQLAlchemy
- **app/schemas/__init__.py**: Définition des schémas Pydantic

### Frontend

- **frontend/src/main.ts**: Point d'entrée de l'application Vue
- **frontend/src/App.vue**: Composant racine Vue
- **frontend/src/router/index.ts**: Configuration du routeur Vue
- **frontend/src/stores/index.ts**: Configuration des stores Pinia
- **frontend/src/services/api.ts**: Configuration du client API

### Configuration

- **docker-compose.yml**: Configuration des services Docker
- **Dockerfile**: Instructions de build Docker
- **.env.example**: Exemple de variables d'environnement
- **Makefile**: Commandes utilitaires pour le développement

## Flux de Données

1. Les requêtes HTTP arrivent au backend FastAPI via les points d'accès définis dans **app/api/v1/endpoints/**
2. Les données sont validées via les schémas Pydantic dans **app/schemas/**
3. Les opérations CRUD sont effectuées via les fonctions dans **app/crud/**
4. Les modèles dans **app/models/** définissent la structure de la base de données
5. Le frontend envoie des requêtes API via les services dans **frontend/src/services/**
6. Les données sont stockées dans les stores Pinia dans **frontend/src/stores/**
7. Les composants Vue dans **frontend/src/components/** et **frontend/src/views/** affichent les données
