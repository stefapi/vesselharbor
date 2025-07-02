# Workflow Git

Ce document décrit le workflow Git recommandé pour ce projet, incluant la stratégie de branches, les conventions de messages de commit, et le processus de pull request.

## Stratégie de Branches

Nous utilisons une stratégie de branches basée sur GitFlow, adaptée pour nos besoins :

### Branches Principales

- **main** : Code de production stable. Toutes les versions déployées en production proviennent de cette branche.
- **develop** : Branche d'intégration principale pour le développement. Toutes les fonctionnalités terminées sont fusionnées ici.

### Branches Temporaires

- **feature/xxx** : Pour le développement de nouvelles fonctionnalités (ex: `feature/user-authentication`).
- **bugfix/xxx** : Pour la correction de bugs qui ne sont pas critiques (ex: `bugfix/login-validation`).
- **hotfix/xxx** : Pour les corrections urgentes directement depuis `main` (ex: `hotfix/security-vulnerability`).
- **release/x.y.z** : Pour la préparation des versions à déployer (ex: `release/1.2.0`).

## Workflow de Base

1. **Création d'une branche de fonctionnalité** :
   ```bash
   git checkout develop
   git pull
   git checkout -b feature/ma-fonctionnalite
   ```

2. **Développement et commits réguliers** :
   ```bash
   git add .
   git commit -m "feat: ajoute la fonctionnalité X"
   ```

3. **Mise à jour avec develop** :
   ```bash
   git checkout develop
   git pull
   git checkout feature/ma-fonctionnalite
   git rebase develop
   ```

4. **Soumission de la pull request** :
   - Pousser la branche vers le dépôt distant
   ```bash
   git push -u origin feature/ma-fonctionnalite
   ```
   - Créer une pull request via l'interface GitHub/GitLab

5. **Après approbation et fusion** :
   ```bash
   git checkout develop
   git pull
   git branch -d feature/ma-fonctionnalite
   ```

## Conventions de Messages de Commit

Nous suivons les conventions de [Conventional Commits](https://www.conventionalcommits.org/) :

```
<type>[scope optional]: <description>

[corps optionnel]

[pied de page(s) optionnel(s)]
```

### Types de Commit

- **feat** : Nouvelle fonctionnalité
- **fix** : Correction de bug
- **docs** : Modifications de la documentation
- **style** : Formatage, point-virgules manquants, etc. (pas de changement de code)
- **refactor** : Refactorisation du code
- **test** : Ajout ou correction de tests
- **chore** : Tâches de maintenance, mises à jour de dépendances, etc.
- **perf** : Améliorations de performance

### Exemples

```
feat(auth): ajoute l'authentification par OAuth

Implémente l'authentification OAuth avec Google et GitHub.
Inclut la gestion des tokens et la redirection après connexion.

Closes #123
```

```
fix: corrige la validation des formulaires d'inscription

Résout un problème où les messages d'erreur ne s'affichaient pas correctement.
```

## Processus de Pull Request

### Création

1. Assurez-vous que votre branche est à jour avec `develop`
2. Poussez votre branche vers le dépôt distant
3. Créez une pull request via l'interface GitHub/GitLab
4. Remplissez le modèle de PR avec :
   - Description des changements
   - Numéros d'issues liées
   - Captures d'écran (si applicable)
   - Points d'attention pour les reviewers

### Revue

1. Au moins un approbateur est requis
2. Tous les tests automatisés doivent passer
3. Le code doit respecter les standards de qualité du projet
4. Les commentaires doivent être adressés par des commits supplémentaires ou des réponses

### Fusion

1. Utilisez la stratégie "Squash and merge" pour garder l'historique propre
2. Assurez-vous que le message de commit squashé suit les conventions
3. Supprimez la branche après la fusion

## Gestion des Versions

Nous utilisons le [Semantic Versioning](https://semver.org/) (SemVer) pour la numérotation des versions :

- **MAJOR** : Changements incompatibles avec les versions précédentes
- **MINOR** : Ajouts de fonctionnalités rétrocompatibles
- **PATCH** : Corrections de bugs rétrocompatibles

## Hooks Git

Nous utilisons des hooks Git pour automatiser certaines tâches :

- **pre-commit** : Exécute les linters et formateurs
- **commit-msg** : Vérifie que le message de commit suit les conventions
- **pre-push** : Exécute les tests unitaires

Pour installer les hooks :

```bash
# Si vous utilisez Husky
npm install
# ou manuellement
cp .junie/git-hooks/* .git/hooks/
chmod +x .git/hooks/*
```

## Résolution de Conflits

1. Rebasez votre branche sur la branche cible (généralement `develop`)
   ```bash
   git checkout develop
   git pull
   git checkout ma-branche
   git rebase develop
   ```

2. Résolvez les conflits dans chaque fichier
   ```bash
   # Après avoir résolu les conflits
   git add .
   git rebase --continue
   ```

3. Poussez les changements (force push nécessaire après rebase)
   ```bash
   git push --force-with-lease
   ```
