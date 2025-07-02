# Guide de Dépannage

Ce document fournit des solutions aux problèmes courants que vous pourriez rencontrer lors du développement avec ce projet FastAPI + Vue.js.

## Problèmes Backend

### Erreurs de Base de Données

#### Erreur de Connexion à la Base de Données

**Symptôme** : `sqlalchemy.exc.OperationalError: (psycopg2.OperationalError) could not connect to server`

**Solutions** :
1. Vérifiez que le service de base de données est en cours d'exécution :
   ```bash
   docker compose ps
   ```
2. Vérifiez les variables d'environnement dans votre fichier `.env` :
   ```
   DATABASE_URL=postgresql://postgres:postgres@db:5432/app
   ```
3. Si vous utilisez Docker, assurez-vous que le conteneur de base de données est en cours d'exécution :
   ```bash
   docker compose up -d db
   ```

#### Erreurs de Migration

**Symptôme** : `alembic.util.exc.CommandError: Can't locate revision identified by '...'`

**Solutions** :
1. Réinitialisez les migrations :
   ```bash
   cd app
   alembic revision --autogenerate -m "reset migrations"
   alembic upgrade head
   ```
2. Si cela ne fonctionne pas, supprimez le dossier `alembic/versions` et réinitialisez :
   ```bash
   rm -rf alembic/versions/*
   alembic revision --autogenerate -m "initial"
   alembic upgrade head
   ```

### Erreurs d'Installation des Dépendances

**Symptôme** : `Poetry could not find a matching version for ...`

**Solutions** :
1. Mettez à jour Poetry :
   ```bash
   poetry self update
   ```
2. Effacez le cache de Poetry :
   ```bash
   poetry cache clear --all .
   ```
3. Mettez à jour les dépendances :
   ```bash
   poetry update
   ```

### Erreurs de Démarrage du Serveur

**Symptôme** : `ERROR: Address already in use`

**Solutions** :
1. Trouvez et arrêtez le processus utilisant le port :
   ```bash
   lsof -i :8010
   kill -9 <PID>
   ```
2. Utilisez un port différent :
   ```bash
   poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8011
   ```

## Problèmes Frontend

### Erreurs d'Installation

**Symptôme** : `pnpm ERR! code ELIFECYCLE` ou erreurs d'installation de dépendances

**Solutions** :
1. Effacez le cache de pnpm et réinstallez :
   ```bash
   cd frontend
   rm -rf node_modules
   pnpm store prune
   pnpm install
   ```
2. Vérifiez la version de Node.js (doit être ≥ 18) :
   ```bash
   node --version
   ```

### Erreurs de Build

**Symptôme** : `[vite]: Rollup failed to resolve import ...`

**Solutions** :
1. Vérifiez les imports dans vos fichiers :
   ```bash
   cd frontend
   pnpm lint
   ```
2. Effacez le cache de Vite :
   ```bash
   rm -rf node_modules/.vite
   ```
3. Reconstruisez le projet :
   ```bash
   pnpm build
   ```

### Erreurs TypeScript

**Symptôme** : `TS2307: Cannot find module '...' or its corresponding type declarations.`

**Solutions** :
1. Vérifiez que toutes les dépendances sont installées :
   ```bash
   pnpm install
   ```
2. Régénérez les fichiers de déclaration TypeScript :
   ```bash
   pnpm type-check
   ```
3. Ajoutez des déclarations de type manquantes :
   ```typescript
   // src/types/missing-module.d.ts
   declare module 'missing-module';
   ```

### Erreurs CORS

**Symptôme** : `Access to XMLHttpRequest at '...' from origin '...' has been blocked by CORS policy`

**Solutions** :
1. Vérifiez la configuration CORS dans le backend :
   ```python
   # app/core/config.py
   BACKEND_CORS_ORIGINS=["http://localhost:5173","http://localhost:80"]
   ```
2. Assurez-vous que l'URL de l'API est correcte dans le frontend :
   ```
   # frontend/.env
   VITE_API_BASE_URL=http://localhost:8010/api/v1
   ```

## Problèmes Docker

### Erreurs de Build Docker

**Symptôme** : `failed to build: ERROR: ...`

**Solutions** :
1. Nettoyez les images Docker :
   ```bash
   docker system prune -a
   ```
2. Reconstruisez les images :
   ```bash
   docker compose build --no-cache
   ```

### Erreurs de Démarrage des Conteneurs

**Symptôme** : `Error response from daemon: ... port is already allocated`

**Solutions** :
1. Vérifiez les conteneurs en cours d'exécution :
   ```bash
   docker ps
   ```
2. Arrêtez les conteneurs utilisant les mêmes ports :
   ```bash
   docker stop <container_id>
   ```
3. Modifiez les ports dans `docker-compose.yml` :
   ```yaml
   ports:
     - "8011:80"  # Changez 8010 en 8011
   ```

## Problèmes Git

### Erreurs de Hook Git

**Symptôme** : `pre-commit hook failed`

**Solutions** :
1. Vérifiez les erreurs de linting :
   ```bash
   make lint
   ```
2. Corrigez le formatage du code :
   ```bash
   make format
   ```
3. Si nécessaire, contournez temporairement les hooks (à utiliser avec précaution) :
   ```bash
   git commit --no-verify -m "..."
   ```

### Erreurs de Merge/Rebase

**Symptôme** : Conflits de fusion ou de rebase

**Solutions** :
1. Utilisez un outil de résolution de conflits :
   ```bash
   git mergetool
   ```
2. Annulez l'opération en cours et recommencez :
   ```bash
   git merge --abort
   # ou
   git rebase --abort
   ```
3. Mettez à jour votre branche avec la dernière version de develop avant de fusionner :
   ```bash
   git checkout develop
   git pull
   git checkout ma-branche
   git rebase develop
   ```

## Problèmes d'Environnement

### Variables d'Environnement Manquantes

**Symptôme** : `KeyError: '...'` ou `Environment variable ... not set`

**Solutions** :
1. Copiez le fichier d'exemple :
   ```bash
   cp .env.example .env
   ```
2. Éditez le fichier `.env` avec les valeurs appropriées
3. Redémarrez l'application pour charger les nouvelles variables

### Problèmes de Permissions

**Symptôme** : `Permission denied` lors de l'exécution de scripts

**Solutions** :
1. Rendez les scripts exécutables :
   ```bash
   chmod +x script.sh
   ```
2. Vérifiez les permissions des répertoires :
   ```bash
   ls -la
   chmod -R 755 directory
   ```

## Obtenir de l'Aide Supplémentaire

Si vous rencontrez un problème qui n'est pas couvert par ce guide :

1. Consultez les issues GitHub existantes
2. Consultez la documentation officielle des outils utilisés (FastAPI, Vue.js, etc.)
3. Créez une nouvelle issue avec une description détaillée du problème, y compris :
   - Étapes pour reproduire
   - Comportement attendu vs. comportement observé
   - Logs d'erreur
   - Environnement (OS, versions des outils, etc.)
