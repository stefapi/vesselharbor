# app/api/groups.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from ..schema.group import GroupCreate, GroupUpdate, GroupOut
from ..models.group import Group
from ..models.user import User
from ..models.policy import Policy
from ..models.tag import Tag
from ..database.session import SessionLocal
from ..repositories import group_repo, user_repo, policy_repo, tag_repo
from ..api.users import get_current_user
from ..helper import permissions, audit, response

router = APIRouter(prefix="/groups", tags=["groups"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/{group_id}", response_model=dict, summary="Détail d'un groupe", responses={
    200: {"description": "Groupe récupéré avec succès"},
    401: {"description": "Non authentifié"},
    403: {"description": "Permission insuffisante"},
    404: {"description": "Groupe non trouvé"}
})
def get_group(group_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    group = group_repo.get_group(db, group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Groupe non trouvé")
    if not permissions.has_permission(db, current_user, group.organization_id, "group:read"):
        raise HTTPException(status_code=403, detail="Permission insuffisante")
    return response.success_response(group, "Groupe récupéré")

@router.post("/{organization_id}", response_model=dict, summary="Créer un groupe", responses={
    200: {"description": "Groupe créé avec succès"},
    401: {"description": "Non authentifié"},
    403: {"description": "Permission insuffisante"}
})
def create_group(organization_id: int, group_in: GroupCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not permissions.has_permission(db, current_user, organization_id, "group:create"):
        raise HTTPException(status_code=403, detail="Permission insuffisante")
    group = group_repo.create_group(db, organization_id=organization_id, name=group_in.name, description=group_in.description)
    audit.log_action(db, current_user.id, "Création groupe", f"Création du groupe '{group.name}'")
    return response.success_response(group, "Groupe créé")

@router.put("/{group_id}", response_model=dict, summary="Mettre à jour un groupe", responses={
    200: {"description": "Groupe mis à jour avec succès"},
    401: {"description": "Non authentifié"},
    403: {"description": "Permission insuffisante"},
    404: {"description": "Groupe non trouvé"}
})
def update_group(group_id: int, group_in: GroupUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    group = group_repo.get_group(db, group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Groupe non trouvé")
    if not permissions.has_permission(db, current_user, group.organization_id, "group:update"):
        raise HTTPException(status_code=403, detail="Permission insuffisante")
    group = group_repo.update_group(db, group, name=group_in.name, description=group_in.description)
    audit.log_action(db, current_user.id, "Mise à jour groupe", f"Mise à jour du groupe '{group.name}'")
    return response.success_response(group, "Groupe mis à jour")

@router.delete("/{group_id}", response_model=dict, summary="Supprimer un groupe", responses={
    200: {"description": "Groupe supprimé avec succès"},
    401: {"description": "Non authentifié"},
    403: {"description": "Permission insuffisante ou seul un superadmin peut supprimer les groupes 'admin' et 'editors'"},
    404: {"description": "Groupe non trouvé"}
})
def delete_group(group_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    group = group_repo.get_group(db, group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Groupe non trouvé")
    if not permissions.has_permission(db, current_user, group.organization_id, "group:delete"):
        raise HTTPException(status_code=403, detail="Permission insuffisante")

    # Prevent non-superadmin users from deleting 'admin' and 'editors' groups
    if not current_user.is_superadmin and group.name in ["admin", "editors"]:
        raise HTTPException(
            status_code=403,
            detail="Seul un superadmin peut supprimer les groupes 'admin' et 'editors'"
        )

    group_repo.delete_group(db, group)
    audit.log_action(db, current_user.id, "Suppression groupe", f"Groupe '{group.name}' supprimé")
    return response.success_response(None, "Groupe supprimé")

@router.get("", response_model=dict, summary="Lister tous les groupes", responses={
    200: {"description": "Liste de tous les groupes récupérée avec succès"},
    401: {"description": "Non authentifié"},
    403: {"description": "Permission insuffisante - réservé aux superadmins"}
})
def list_all_groups(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not current_user.is_superadmin:
        raise HTTPException(status_code=403, detail="Permission insuffisante")
    groups = db.query(Group).all()
    return response.success_response(groups, "Tous les groupes récupérés")

@router.get("/organization/{org_id}", response_model=dict, summary="Lister les groupes d'une organisation", responses={
    200: {"description": "Liste des groupes de l'organisation récupérée avec succès"},
    401: {"description": "Non authentifié"},
    403: {"description": "Permission insuffisante"}
})
def list_groups_by_org(org_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not permissions.has_permission(db, current_user, org_id, "group:list"):
        raise HTTPException(status_code=403, detail="Permission insuffisante")
    groups = db.query(Group).filter(Group.organization_id == org_id).all()
    return response.success_response(groups, "Groupes récupérés")

@router.get("/{group_id}/users", response_model=dict, summary="Lister les utilisateurs d'un groupe", responses={
    200: {"description": "Liste des utilisateurs du groupe récupérée avec succès"},
    401: {"description": "Non authentifié"},
    403: {"description": "Permission insuffisante"},
    404: {"description": "Groupe non trouvé"}
})
def list_group_users(group_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    group = group_repo.get_group(db, group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Groupe non trouvé")
    if not permissions.has_permission(db, current_user, group.organization_id, "group:read"):
        raise HTTPException(status_code=403, detail="Permission insuffisante")
    return response.success_response(group.users, "Utilisateurs du groupe récupérés")

@router.post("/{group_id}/users/{user_id}", response_model=dict, summary="Associer un utilisateur", responses={
    200: {"description": "Utilisateur ajouté au groupe avec succès"},
    401: {"description": "Non authentifié"},
    403: {"description": "Permission insuffisante"},
    404: {"description": "Groupe ou utilisateur non trouvé"}
})
def assign_user(group_id: int, user_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    group = group_repo.get_group(db, group_id)
    user = user_repo.get_user(db, user_id)
    if not group or not user:
        raise HTTPException(status_code=404, detail="Groupe ou utilisateur non trouvé")
    if not permissions.has_permission(db, current_user, group.organization_id, "group:assign_user"):
        raise HTTPException(status_code=403, detail="Permission insuffisante")
    group.users.append(user)
    db.commit()
    return response.success_response(group, "Utilisateur ajouté au groupe")

@router.delete("/{group_id}/users/{user_id}", response_model=dict, summary="Retirer un utilisateur", responses={
    200: {"description": "Utilisateur retiré du groupe avec succès"},
    401: {"description": "Non authentifié"},
    403: {"description": "Permission insuffisante"},
    404: {"description": "Groupe ou utilisateur non trouvé"}
})
def remove_user(group_id: int, user_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    group = group_repo.get_group(db, group_id)
    user = user_repo.get_user(db, user_id)
    if not group or not user:
        raise HTTPException(status_code=404, detail="Groupe ou utilisateur non trouvé")
    if not permissions.has_permission(db, current_user, group.organization_id, "group:assign_user"):
        raise HTTPException(status_code=403, detail="Permission insuffisante")
    if user in group.users:
        group.users.remove(user)
        db.commit()
    return response.success_response(group, "Utilisateur retiré du groupe")

@router.get("/{group_id}/policy", response_model=dict, summary="Lister les policies d'un groupe", responses={
    200: {"description": "Liste des policies du groupe récupérée avec succès"},
    401: {"description": "Non authentifié"},
    403: {"description": "Permission insuffisante"},
    404: {"description": "Groupe non trouvé"}
})
def list_group_policies(group_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    group = group_repo.get_group(db, group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Groupe non trouvé")
    if not permissions.has_permission(db, current_user, group.organization_id, "group:read"):
        raise HTTPException(status_code=403, detail="Permission insuffisante")
    return response.success_response(group.policies, "Policies du groupe récupérées")

@router.post("/{group_id}/policy", response_model=dict, summary="Associer une policy", responses={
    200: {"description": "Policy associée au groupe avec succès"},
    401: {"description": "Non authentifié"},
    403: {"description": "Permission insuffisante"},
    404: {"description": "Groupe ou policy non trouvée"}
})
def assign_policy(group_id: int, policy_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    group = group_repo.get_group(db, group_id)
    policy = policy_repo.get_policy(db, policy_id)
    if not group or not policy:
        raise HTTPException(status_code=404, detail="Groupe ou policy non trouvée")
    if not permissions.has_permission(db, current_user, group.organization_id, "group:assign_policy"):
        raise HTTPException(status_code=403, detail="Permission insuffisante")
    group.policies.append(policy)
    db.commit()
    return response.success_response(group, "Policy associée au groupe")

@router.delete("/{group_id}/policy/{policy_id}", response_model=dict, summary="Retirer une policy", responses={
    200: {"description": "Policy retirée du groupe avec succès"},
    401: {"description": "Non authentifié"},
    403: {"description": "Permission insuffisante"},
    404: {"description": "Groupe ou policy non trouvée"}
})
def remove_policy(group_id: int, policy_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    group = group_repo.get_group(db, group_id)
    policy = policy_repo.get_policy(db, policy_id)
    if not group or not policy:
        raise HTTPException(status_code=404, detail="Groupe ou policy non trouvée")
    if not permissions.has_permission(db, current_user, group.organization_id, "group:assign_policy"):
        raise HTTPException(status_code=403, detail="Permission insuffisante")
    if policy in group.policies:
        group.policies.remove(policy)
        db.commit()
    return response.success_response(group, "Policy retirée du groupe")

@router.get("/{group_id}/tags", response_model=dict, summary="Lister les tags d'un groupe", responses={
    200: {"description": "Liste des tags du groupe récupérée avec succès"},
    401: {"description": "Non authentifié"},
    403: {"description": "Permission insuffisante"},
    404: {"description": "Groupe non trouvé"}
})
def list_group_tags(group_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    group = group_repo.get_group(db, group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Groupe non trouvé")
    if not permissions.has_permission(db, current_user, group.organization_id, "group:read"):
        raise HTTPException(status_code=403, detail="Permission insuffisante")
    return response.success_response(group.tags, "Tags du groupe récupérés")

@router.post("/{group_id}/tags/{tag_id}", response_model=dict, summary="Ajouter un tag à un groupe", responses={
    200: {"description": "Tag ajouté au groupe avec succès"},
    401: {"description": "Non authentifié"},
    403: {"description": "Permission insuffisante"},
    404: {"description": "Groupe ou tag non trouvé"}
})
def add_tag_to_group(group_id: int, tag_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    group = group_repo.get_group(db, group_id)
    tag = tag_repo.get_tag(db, tag_id)
    if not group or not tag:
        raise HTTPException(status_code=404, detail="Groupe ou tag non trouvé")
    if not permissions.has_permission(db, current_user, group.organization_id, "group:assign_tag"):
        raise HTTPException(status_code=403, detail="Permission insuffisante")
    group.tags.append(tag)
    db.commit()
    return response.success_response(group, "Tag ajouté au groupe")

@router.delete("/{group_id}/tags/{tag_id}", response_model=dict, summary="Retirer un tag d'un groupe", responses={
    200: {"description": "Tag retiré du groupe avec succès"},
    401: {"description": "Non authentifié"},
    403: {"description": "Permission insuffisante"},
    404: {"description": "Groupe ou tag non trouvé"}
})
def remove_tag_from_group(group_id: int, tag_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    group = group_repo.get_group(db, group_id)
    tag = tag_repo.get_tag(db, tag_id)
    if not group or not tag:
        raise HTTPException(status_code=404, detail="Groupe ou tag non trouvé")
    if not permissions.has_permission(db, current_user, group.organization_id, "group:assign_tag"):
        raise HTTPException(status_code=403, detail="Permission insuffisante")
    if tag in group.tags:
        group.tags.remove(tag)
        db.commit()
    return response.success_response(group, "Tag retiré du groupe")
