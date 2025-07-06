import os
from typing import Optional

from dotenv import load_dotenv
from sqlalchemy.orm import Session

from ..helper.security import get_password_hash
from ..models.user import User
from ..models.function import Function
from ..models.organization import Organization
from ..models.group import Group
from ..models.policy import Policy
from ..repositories import group_repo, user_repo, policy_repo, rule_repo
from ..schema.policy import PolicyCreate

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

    # Users
    {"name": "user:list", "description": "Lister les utilisateurs."},
    {"name": "user:read", "description": "Voir les utilisateurs."},
    {"name": "user:create", "description": "Créer un utilisateur."},
    {"name": "user:update", "description": "Modifier un utilisateur."},
    {"name": "user:delete", "description": "Supprimer un utilisateur."},
    {"name": "user:delete", "description": "Supprimer un utilisateur."},
    {"name": "user:update_password", "description": "Réinitialiser le mot de passe d'un utilisateur."},
    {"name": "user:assign_user", "description": "Affecter un utilisateur à un utilisateur."},
    {"name": "user:assign_policy", "description": "Affecter un policy à un utilisateur."},
    {"name": "user:read_groups", "description": "Lit les groupes d'un utilisateur."},
    {"name": "user:read_policies", "description": "Lit les policies d'un utilisateur."},
    {"name": "user:read_organizations", "description": "Lit les organisations d'un utilisateur."},
    {"name": "user:read_tags", "description": "Lit les tags d'un utilisateur."},
    {"name": "user:update_tags", "description": "Met à jour les tags d'un utilisateur."},
    # Groups
    {"name": "group:read", "description": "Voir les groupes."},
    {"name": "group:create", "description": "Créer un groupe."},
    {"name": "group:update", "description": "Modifier un groupe."},
    {"name": "group:delete", "description": "Supprimer un groupe."},
    {"name": "group:assign_user", "description": "Affecter un utilisateur à un groupe."},
    {"name": "group:assign_policy", "description": "Affecter un policy à un groupe."},

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

DEFAULT_GROUPS = [
    {"name": "Administrators", "description": "Groupe des administrateurs avec tous les privilèges."},
    {"name": "Users", "description": "Groupe des utilisateurs standard."},
    {"name": "Viewers", "description": "Groupe avec accès en lecture seule."},
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

def seed_default_groups(db: Session, organization: Organization):
    """Crée les groupes par défaut pour l'organisation"""
    for group_data in DEFAULT_GROUPS:
        existing = db.query(Group).filter(
            Group.name == group_data["name"],
            Group.organization_id == organization.id
        ).first()
        if not existing:
            group_repo.create_group(
                db,
                organization_id=organization.id,
                name=group_data["name"],
                description=group_data["description"]
            )
            print(f"✅ Groupe '{group_data['name']}' créé pour l'organisation '{organization.name}'")

def seed_default_policies_and_rules(db: Session, organization: Organization):
    """Crée les policies par défaut avec leurs règles pour chaque groupe"""

    # Récupérer les groupes
    admin_group = db.query(Group).filter(
        Group.name == "Administrators",
        Group.organization_id == organization.id
    ).first()

    users_group = db.query(Group).filter(
        Group.name == "Users",
        Group.organization_id == organization.id
    ).first()

    viewers_group = db.query(Group).filter(
        Group.name == "Viewers",
        Group.organization_id == organization.id
    ).first()

    if not admin_group or not users_group or not viewers_group:
        print("⚠️ Groupes par défaut non trouvés, impossible de créer les policies")
        return

    # Récupérer les fonctions
    admin_function = db.query(Function).filter(Function.name == "admin").first()

    # Fonctions pour les utilisateurs standard
    user_functions = db.query(Function).filter(Function.name.in_([
        "env:read", "element:read", "user:read_groups", "user:read_policies",
        "user:read_organizations", "user:read_tags"
    ])).all()

    # Fonctions pour les viewers (lecture seule)
    viewer_functions = db.query(Function).filter(Function.name.in_([
        "env:read", "element:read", "user:read", "group:read", "policy:read",
        "tag:read", "organization:read"
    ])).all()

    # Créer la policy pour les Administrators
    admin_policy_name = f"Admin Policy - {organization.name}"
    existing_admin_policy = db.query(Policy).filter(
        Policy.name == admin_policy_name,
        Policy.organization_id == organization.id
    ).first()

    if not existing_admin_policy and admin_function:
        admin_policy = policy_repo.create_policy(db, PolicyCreate(
            name=admin_policy_name,
            description="Policy complète pour les administrateurs",
            organization_id=organization.id
        ))

        # Ajouter la règle admin (accès complet)
        rule_repo.create_rule(db, admin_policy.id, admin_function.id)

        # Associer la policy au groupe Administrators
        policy_repo.add_group(db, admin_policy, admin_group)
        print(f"✅ Policy '{admin_policy_name}' créée avec règle admin")

    # Créer la policy pour les Users
    users_policy_name = f"Users Policy - {organization.name}"
    existing_users_policy = db.query(Policy).filter(
        Policy.name == users_policy_name,
        Policy.organization_id == organization.id
    ).first()

    if not existing_users_policy and user_functions:
        users_policy = policy_repo.create_policy(db, PolicyCreate(
            name=users_policy_name,
            description="Policy standard pour les utilisateurs",
            organization_id=organization.id
        ))

        # Ajouter les règles pour les utilisateurs
        for func in user_functions:
            rule_repo.create_rule(db, users_policy.id, func.id)

        # Associer la policy au groupe Users
        policy_repo.add_group(db, users_policy, users_group)
        print(f"✅ Policy '{users_policy_name}' créée avec {len(user_functions)} règles")

    # Créer la policy pour les Viewers
    viewers_policy_name = f"Viewers Policy - {organization.name}"
    existing_viewers_policy = db.query(Policy).filter(
        Policy.name == viewers_policy_name,
        Policy.organization_id == organization.id
    ).first()

    if not existing_viewers_policy and viewer_functions:
        viewers_policy = policy_repo.create_policy(db, PolicyCreate(
            name=viewers_policy_name,
            description="Policy en lecture seule pour les viewers",
            organization_id=organization.id
        ))

        # Ajouter les règles pour les viewers
        for func in viewer_functions:
            rule_repo.create_rule(db, viewers_policy.id, func.id)

        # Associer la policy au groupe Viewers
        policy_repo.add_group(db, viewers_policy, viewers_group)
        print(f"✅ Policy '{viewers_policy_name}' créée avec {len(viewer_functions)} règles")

def seed_superadmin(db: Session, organization: Organization):
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
        db.refresh(new_admin)

        # Attacher le superadmin à l'organisation par défaut
        user_repo.add_user_to_organization(db, new_admin, organization)
        print(f"✅ Superadmin seedé et attaché à l'organisation '{organization.name}'")

        # Ajouter le superadmin au groupe Administrators
        admin_group = db.query(Group).filter(
            Group.name == "Administrators",
            Group.organization_id == organization.id
        ).first()
        if admin_group:
            group_repo.add_user_to_group(db, admin_group, new_admin)
            print(f"✅ Superadmin ajouté au groupe 'Administrators'")
    else:
        # Si le superadmin existe déjà, vérifier qu'il est bien attaché à l'organisation
        if organization not in existing.organizations:
            user_repo.add_user_to_organization(db, existing, organization)
            print(f"✅ Superadmin existant attaché à l'organisation '{organization.name}'")

        # Vérifier qu'il est dans le groupe Administrators
        admin_group = db.query(Group).filter(
            Group.name == "Administrators",
            Group.organization_id == organization.id
        ).first()
        if admin_group and existing not in admin_group.users:
            group_repo.add_user_to_group(db, admin_group, existing)
            print(f"✅ Superadmin existant ajouté au groupe 'Administrators'")

def seed(db: Session):
    seed_functions(db)
    organization = seed_organization(db)
    seed_default_groups(db, organization)
    seed_default_policies_and_rules(db, organization)
    seed_superadmin(db, organization)
