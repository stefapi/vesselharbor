import os
from typing import Optional

from dotenv import load_dotenv
from sqlalchemy.orm import Session

from ..helper.security import get_password_hash
from ..models import User
from ..models.function import Function

# Charger les variables d'environnement
load_dotenv()

# Liste des fonctions élémentaires à insérer dans la table des fonctions
DEFAULT_FUNCTIONS = [
    {"name": "admin", "description": "Accès complet à toutes les fonctions d'administration."},
    {"name": "env:read", "description": "Visualiser un environnement."},
    {"name": "env:update", "description": "Modifier un environnement."},
    {"name": "env:delete", "description": "Supprimer un environnement."},
    {"name": "element:create", "description": "Créer un élément dans un environnement."},
    {"name": "element:update", "description": "Mettre à jour un élément dans un environnement."},
    {"name": "element:delete", "description": "Supprimer un élément dans un environnement."},
    {"name": "group:create", "description": "Créer un groupe dans un environnement."},
    {"name": "group:update", "description": "Modifier un groupe."},
    {"name": "group:delete", "description": "Supprimer un groupe."},
    {"name": "group:assign_user", "description": "Affecter un utilisateur à un groupe."},
    {"name": "group:assign_function", "description": "Affecter une fonction à un groupe."},
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
            new_func = Function(name=func_data["name"], description=func_data.get("description"))
            db.add(new_func)
    db.commit()

def seed_superadmin(db: Session):
    # Récupération des variables avec vérification
    email = get_env_var("SUPERADMIN_EMAIL")
    password = get_env_var("SUPERADMIN_PASSWORD")

    # Vérification de la présence des variables
    if not all([email, password]):
        return
    # Vérifier si le superadmin existe déjà
    existing_admin = db.query(User).filter(
        User.email == email,
        User.is_superadmin == True
    ).first()

    if not existing_admin:
        new_admin = User(
            email=email,
            hashed_password=get_password_hash(password),
            is_superadmin=True
        )
        db.add(new_admin)
        db.commit()

def seed(db: Session):
    seed_functions(db)
    seed_superadmin(db)
