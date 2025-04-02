from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from ..models import UserAssignment
from ..schema.group import GroupCreate, GroupUpdate, GroupOut
from ..schema.function import FunctionCreate
from ..models.group import Group
from ..models.user import User
from ..database.session import SessionLocal
from ..repositories import group_repo, function_repo
from ..api.users import get_current_user
from ..helper import permissions, audit, response

router = APIRouter(prefix="/groups", tags=["groups"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post(
    "/{environment_id}",
    response_model=dict,
    summary="Créer un groupe",
    description="Crée un nouveau groupe dans un environnement donné.",
    responses={
        403: {"description": "Permission insuffisante"},
        500: {"description": "Erreur interne"}
    }
)
def create_group(environment_id: int, group_in: GroupCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not permissions.has_permission(db, current_user, environment_id, "group:create"):
        raise HTTPException(status_code=403, detail="Permission insuffisante pour créer un groupe")
    group = group_repo.create_group(db, environment_id=environment_id, name=group_in.name, description=group_in.description)
    audit.log_action(db, current_user.id, "Création groupe", f"Création du groupe '{group.name}' dans l'environnement {environment_id}")
    return response.success_response(group, "Groupe créé avec succès")

@router.put(
    "/{group_id}",
    response_model=dict,
    summary="Mettre à jour un groupe",
    description="Modifie les informations d'un groupe.",
    responses={
        404: {"description": "Groupe non trouvé"},
        403: {"description": "Permission insuffisante"}
    }
)
def update_group(group_id: int, group_in: GroupUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    group = group_repo.get_group(db, group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Groupe non trouvé")
    if not permissions.has_permission(db, current_user, group.environment_id, "group:update"):
        raise HTTPException(status_code=403, detail="Permission insuffisante pour modifier ce groupe")
    group = group_repo.update_group(db, group, name=group_in.name, description=group_in.description)
    audit.log_action(db, current_user.id, "Mise à jour groupe", f"Mise à jour du groupe '{group.name}' (ID {group.id})")
    return response.success_response(group, "Groupe mis à jour")

@router.delete(
    "/{group_id}",
    response_model=dict,
    summary="Supprimer un groupe",
    description="Supprime un groupe donné.",
    responses={
        404: {"description": "Groupe non trouvé"},
        403: {"description": "Permission insuffisante"}
    }
)
def delete_group(group_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    group = group_repo.get_group(db, group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Groupe non trouvé")
    if not permissions.has_permission(db, current_user, group.environment_id, "group:delete"):
        raise HTTPException(status_code=403, detail="Permission insuffisante pour supprimer ce groupe")
    group_repo.delete_group(db, group)
    audit.log_action(db, current_user.id, "Suppression groupe", f"Suppression du groupe '{group.name}' (ID {group.id})")
    return response.success_response(None, "Groupe supprimé")

@router.post(
    "/{group_id}/functions",
    response_model=dict,
    summary="Affecter une fonction à un groupe",
    description="Affecte une fonction globale à un groupe.",
    responses={
        404: {"description": "Groupe non trouvé"},
        403: {"description": "Permission insuffisante"}
    }
)
def add_function_to_group(group_id: int, func_in: FunctionCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    group = group_repo.get_group(db, group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Groupe non trouvé")
    if not permissions.has_permission(db, current_user, group.environment_id, "group:assign_function"):
        raise HTTPException(status_code=403, detail="Permission insuffisante pour affecter une fonction à ce groupe")
    func = function_repo.create_function(db, name=func_in.name, description=func_in.description)
    group.functions.append(func)
    db.commit()
    db.refresh(group)
    audit.log_action(db, current_user.id, "Affectation fonction groupe", f"Affectation de la fonction '{func.name}' au groupe '{group.name}' (ID {group.id})")
    return response.success_response(group, "Fonction affectée au groupe")

@router.delete(
    "/{group_id}/functions/{function_id}",
    response_model=dict,
    summary="Retirer une fonction d'un groupe",
    description="Supprime l'affectation d'une fonction d'un groupe.",
    responses={
        404: {"description": "Groupe ou fonction non trouvée"},
        403: {"description": "Permission insuffisante"}
    }
)
def remove_function_from_group(group_id: int, function_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    group = group_repo.get_group(db, group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Groupe non trouvé")
    if not permissions.has_permission(db, current_user, group.environment_id, "group:assign_function"):
        raise HTTPException(status_code=403, detail="Permission insuffisante pour retirer une fonction de ce groupe")
    func = next((f for f in group.functions if f.id == function_id), None)
    if not func:
        raise HTTPException(status_code=404, detail="Fonction non trouvée dans le groupe")
    group.functions.remove(func)
    db.commit()
    db.refresh(group)
    audit.log_action(db, current_user.id, "Retrait fonction groupe", f"Retrait de la fonction '{func.name}' du groupe '{group.name}' (ID {group.id})")
    return response.success_response(group, "Fonction retirée du groupe")

@router.post(
    "/{group_id}/users/{user_id}",
    response_model=dict,
    summary="Affecter un utilisateur à un groupe",
    description="Affecte un utilisateur à un groupe via la table user_assignments.",
    responses={
        404: {"description": "Groupe ou utilisateur non trouvé"},
        403: {"description": "Permission insuffisante"},
        400: {"description": "L'utilisateur est déjà affecté à ce groupe"}
    }
)
def assign_user_to_group(group_id: int, user_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    group = group_repo.get_group(db, group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Groupe non trouvé")
    target_env = group.environment_id if group.environment_id is not None else 0
    if not permissions.has_permission(db, current_user, target_env, "group:assign_user"):
        raise HTTPException(status_code=403, detail="Permission insuffisante pour affecter un utilisateur à ce groupe")
    from ..repositories import user_repo
    user = user_repo.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    # Vérifier si une affectation existe déjà pour ce groupe
    existing = db.query(UserAssignment).filter(
        UserAssignment.user_id == user.id,
        UserAssignment.group_id == group.id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="L'utilisateur est déjà affecté à ce groupe")
    new_assignment = UserAssignment(user_id=user.id, group_id=group.id)
    db.add(new_assignment)
    db.commit()
    db.refresh(new_assignment)
    audit.log_action(db, current_user.id, "Affectation utilisateur groupe",
                     f"Affectation de l'utilisateur '{user.email}' au groupe '{group.name}' (ID {group.id})")
    return response.success_response(group, "Utilisateur affecté au groupe")


@router.delete(
    "/{group_id}/users/{user_id}",
    response_model=dict,
    summary="Désaffecter un utilisateur d'un groupe",
    description="Supprime l'affectation d'un utilisateur à un groupe.",
    responses={
        404: {"description": "Groupe ou utilisateur non trouvé"},
        403: {"description": "Permission insuffisante"}
    }
)
def remove_user_from_group(group_id: int, user_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    group = group_repo.get_group(db, group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Groupe non trouvé")
    target_env = group.environment_id if group.environment_id is not None else 0
    if not permissions.has_permission(db, current_user, target_env, "group:assign_user"):
        raise HTTPException(status_code=403, detail="Permission insuffisante pour désaffecter un utilisateur de ce groupe")
    from ..repositories import user_repo
    user = user_repo.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    assignment = db.query(UserAssignment).filter(
        UserAssignment.user_id == user.id,
        UserAssignment.group_id == group.id
    ).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Affectation introuvée")
    db.delete(assignment)
    db.commit()
    audit.log_action(db, current_user.id, "Désaffectation utilisateur groupe",
                     f"Désaffectation de l'utilisateur '{user.email}' du groupe '{group.name}' (ID {group.id})")
    return response.success_response(group, "Utilisateur désaffecté du groupe")
@router.get(
    "/environment/{environment_id}",
    response_model=dict,
    summary="Lister les groupes d'un environnement",
    description="Liste les groupes d'un environnement avec pagination et filtrage par nom.",
    responses={
        403: {"description": "Permission insuffisante"}
    }
)
def list_groups(
    environment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    name: Optional[str] = None
):
    if not permissions.has_permission(db, current_user, environment_id, "group:list"):
        raise HTTPException(status_code=403, detail="Permission insuffisante pour lister les groupes de cet environnement")
    query = db.query(Group).filter(Group.environment_id == environment_id)
    if name:
        query = query.filter(Group.name.ilike(f"%{name}%"))
    groups = query.offset(skip).limit(limit).all()
    return response.success_response(groups, "Liste des groupes récupérée")
