from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from ..schema.environment import EnvironmentCreate, EnvironmentOut
from ..models.environment import Environment
from ..models.user import User
from ..models.user_assignment import UserAssignment  # Anciennement UserEnvironment
from ..database.session import SessionLocal
from ..repositories import environment_repo, group_repo, function_repo
from ..api.users import get_current_user
from ..helper import permissions, audit, response

router = APIRouter(prefix="/environments", tags=["environments"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post(
    "/",
    response_model=dict,
    summary="Créer un environnement",
    description=(
            "Crée un nouvel environnement, puis crée automatiquement un groupe 'Admins' associé à cet environnement. "
            "Le groupe 'Admins' se voit affecter la fonction 'admin'. Enfin, l'utilisateur qui crée l'environnement est "
            "automatiquement associé à ce groupe via la table UserAssignment."
    ),
    responses={
        400: {"description": "Erreur de validation"},
        500: {"description": "Erreur interne du serveur"}
    }
)
def create_environment(
        env: EnvironmentCreate,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    # Création de l'environnement
    environment = environment_repo.create_environment(db, name=env.name)

    # Création du groupe "Admins" associé à cet environnement
    admin_group = group_repo.create_group(db, environment_id=environment.id, name="Admins",
                                          description="Groupe admin par défaut")

    # Récupération de la fonction 'admin'
    admin_function = function_repo.get_function_by_name(db, "admin")
    if not admin_function:
        raise HTTPException(status_code=500, detail="La fonction 'admin' n'existe pas dans la base")

    # Affectation de la fonction 'admin' au groupe (si cette opération n'est pas déjà incluse dans create_group)
    group_repo.add_function_to_group(db, group=admin_group, function=admin_function)

    # Affectation automatique du créateur à ce groupe via UserAssignment
    new_assignment = UserAssignment(user_id=current_user.id, group_id=admin_group.id)
    db.add(new_assignment)
    db.commit()
    db.refresh(new_assignment)

    audit.log_action(
        db,
        current_user.id,
        "Création environnement",
        f"Environnement '{environment.name}' (ID {environment.id}) créé et utilisateur '{current_user.email}' affecté dans le groupe 'Admins' (ID {admin_group.id})"
    )

    return response.success_response(environment, "Environnement créé avec succès")


@router.put(
    "/{environment_id}",
    response_model=dict,
    summary="Mettre à jour un environnement",
    description="Modifie le nom d'un environnement. La permission est vérifiée via le groupe associé.",
    responses={
        404: {"description": "Environnement non trouvé"},
        403: {"description": "Permission insuffisante"}
    }
)
def update_environment(
        environment_id: int,
        env: EnvironmentCreate,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    environment = environment_repo.get_environment(db, environment_id)
    if not environment:
        raise HTTPException(status_code=404, detail="Environnement non trouvé")
    if not permissions.has_permission(db, current_user, environment_id, "env:update"):
        raise HTTPException(status_code=403, detail="Permission insuffisante pour modifier cet environnement")
    environment.name = env.name
    db.commit()
    db.refresh(environment)
    audit.log_action(
        db,
        current_user.id,
        "Mise à jour environnement",
        f"Mise à jour de l'environnement '{environment.name}' (ID {environment.id})"
    )
    return response.success_response(environment, "Environnement mis à jour")


@router.delete(
    "/{environment_id}",
    response_model=dict,
    summary="Supprimer un environnement",
    description="Supprime un environnement donné. Seuls les utilisateurs disposant de la permission peuvent effectuer cette opération.",
    responses={
        404: {"description": "Environnement non trouvé"},
        403: {"description": "Permission insuffisante"}
    }
)
def delete_environment(
        environment_id: int,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    environment = environment_repo.get_environment(db, environment_id)
    if not environment:
        raise HTTPException(status_code=404, detail="Environnement non trouvé")
    if not permissions.has_permission(db, current_user, environment_id, "env:delete"):
        raise HTTPException(status_code=403, detail="Permission insuffisante pour supprimer cet environnement")
    environment_repo.delete_environment(db, environment)
    audit.log_action(
        db,
        current_user.id,
        "Suppression environnement",
        f"Suppression de l'environnement '{environment.name}' (ID {environment.id})"
    )
    return response.success_response(None, "Environnement supprimé")


@router.get(
    "/",
    response_model=dict,
    summary="Lister les environnements",
    description=(
            "Liste les environnements avec pagination et filtrage par nom. "
            "Les superadmins voient tous les environnements, tandis que les autres utilisateurs voient uniquement "
            "ceux auxquels ils sont affectés via leur groupe (global ou spécifique)."
    ),
    responses={
        403: {"description": "Non autorisé"}
    }
)
def list_environments(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 100,
        name: Optional[str] = None
):
    if current_user.is_superadmin:
        query = db.query(Environment)
        if name:
            query = query.filter(Environment.name.ilike(f"%{name}%"))
        environments = query.offset(skip).limit(limit).all()
    else:
        # Pour les utilisateurs non superadmin, on récupère les environnements via les affectations (UserAssignment)
        from ..models.group import Group  # Import local pour éviter la circularité
        environments = (
            db.query(Environment)
            .join(Group, Environment.id == Group.environment_id)
            .join(UserAssignment, Group.id == UserAssignment.group_id)
            .filter(UserAssignment.user_id == current_user.id)
            .offset(skip)
            .limit(limit)
            .all()
        )
    return response.success_response(environments, "Liste des environnements récupérée")
