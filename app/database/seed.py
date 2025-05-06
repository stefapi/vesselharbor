import os
from typing import Optional

from dotenv import load_dotenv
from sqlalchemy.orm import Session

from ..helper.security import get_password_hash
from ..models.user import User
from ..models.function import Function
from ..models.organization import Organization

# Charger les variables d'environnement
load_dotenv()

DEFAULT_FUNCTIONS = [
    # Permissions d'administration générale
    {"name": "admin", "description": "Accès complet à toutes les fonctions d'administration."},

    # Environments
    {"name": "env:read", "description": "Lire les informations d’un environnement."},
    {"name": "env:create", "description": "Créer un environnement."},
    {"name": "env:update", "description": "Mettre à jour un environnement."},
    {"name": "env:delete", "description": "Supprimer un environnement."},

    # Elements
    {"name": "element:read", "description": "Lire les éléments d’un environnement."},
    {"name": "element:create", "description": "Créer un élément."},
    {"name": "element:update", "description": "Mettre à jour un élément."},
    {"name": "element:delete", "description": "Supprimer un élément."},

    # Groups
    {"name": "group:read", "description": "Voir les groupes."},
    {"name": "group:create", "description": "Créer un groupe."},
    {"name": "group:update", "description": "Modifier un groupe."},
    {"name": "group:delete", "description": "Supprimer un groupe."},
    {"name": "group:assign_user", "description": "Affecter un utilisateur à un groupe."},

    # Tags
    {"name": "tag:read", "description": "Voir les tags."},
    {"name": "tag:create", "description": "Créer un tag."},
    {"name": "tag:delete", "description": "Supprimer un tag."},

    # Policies
    {"name": "policy:read", "description": "Voir les policies."},
    {"name": "policy:create", "description": "Créer une policy."},
    {"name": "policy:update", "description": "Modifier une policy."},
    {"name": "policy:delete", "description": "Supprimer une policy."},

    # Rules
    {"name": "rule:read", "description": "Voir les règles."},
    {"name": "rule:create", "description": "Créer une règle."},
    {"name": "rule:update", "description": "Mettre à jour une règle."},
    {"name": "rule:delete", "description": "Supprimer une règle."},

    # Organizations
    {"name": "organization:read", "description": "Voir les organisations."},
    {"name": "organization:create", "description": "Créer une organisation."},
    {"name": "organization:update", "description": "Mettre à jour une organisation."},
    {"name": "organization:delete", "description": "Supprimer une organisation."},
]

def get_env_var(name: str) -> Optional[str]:
    """Helper pour récupérer une variable d'environnement avec vérification"""
    value = os.environ.get(name)
    if not value or value.strip() == "":
        return None
    return value.strip()

def seed_functions(db: Session):
    for func_data in DEFAULT_FUNCTIONS:
        existing = db.query(Function).filter(Function.name == func_data["name"]).first()
        if not existing:
            db.add(Function(**func_data))
    db.commit()

def seed_organization(db: Session) -> Organization:
    """Crée une organisation par défaut s'il n'en existe aucune"""
    org = db.query(Organization).filter(Organization.name == "Default Org").first()
    if not org:
        org = Organization(name="Default Org", description="Organisation par défaut pour initialisation.")
        db.add(org)
        db.commit()
        db.refresh(org)
    return org

def seed_superadmin(db: Session):
    email = get_env_var("SUPERADMIN_EMAIL")
    password = get_env_var("SUPERADMIN_PASSWORD")
    if not email or not password:
        print("⚠️ SUPERADMIN_EMAIL ou SUPERADMIN_PASSWORD non défini dans le .env")
        return

    existing = db.query(User).filter(User.email == email, User.is_superadmin == True).first()
    if not existing:
        new_admin = User(
            username=email.split("@")[0],
            email=email,
            first_name="Super",
            last_name="Admin",
            hashed_password=get_password_hash(password),
            is_superadmin=True
        )
        db.add(new_admin)
        db.commit()
        print("✅ Superadmin seedé")

def seed(db: Session):
    seed_functions(db)
    seed_organization(db)
    seed_superadmin(db)
