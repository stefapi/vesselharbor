# app/api/tags.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..models.user import User
from ..models.element import Element
from ..models.environment import Environment
from ..database.session import SessionLocal
from ..repositories import tag_repo
from ..api.users import get_current_user
from ..helper import permissions, audit, response
from ..schema.tag import TagOut, TagCreate

router = APIRouter(prefix="/tags", tags=["tags"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get(
    "",
    response_model=dict,
    summary="Lister tous les tags",
    description="Renvoie la liste de tous les tags si l'utilisateur a les droits sur leur organisation."
)
def list_tags(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    all_tags = tag_repo.list_tags(db)
    accessible_tags = []

    for tag in all_tags:
        # Check permissions through policies
        if tag.policies and permissions.has_permission(db, current_user, tag.policies[0].organization_id, "tag:read"):
            accessible_tags.append(tag)
            continue

        # Check permissions through groups
        if tag.groups and permissions.has_permission(db, current_user, tag.groups[0].organization_id, "tag:read"):
            accessible_tags.append(tag)
            continue

        # Check permissions through users
        if tag.users and tag.users[0].organizations and permissions.has_permission(db, current_user, tag.users[0].organizations[0].id, "tag:read"):
            accessible_tags.append(tag)
            continue

        # Check permissions through elements
        if tag.elements and tag.elements[0].environment and permissions.has_permission(db, current_user, tag.elements[0].environment.organization_id, "tag:read"):
            accessible_tags.append(tag)
            continue

        # Check permissions through environments
        if tag.environments and permissions.has_permission(db, current_user, tag.environments[0].organization_id, "tag:read"):
            accessible_tags.append(tag)
            continue

    return response.success_response(accessible_tags, "Liste des tags accessible récupérée")

@router.post(
    "",
    response_model=dict,
    summary="Créer un tag",
    description="Crée un nouveau tag. L'utilisateur doit avoir les droits sur une organisation spécifique.",
    responses={400: {"description": "Tag existant"}}
)
def create_tag(
    tag_in: TagCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not permissions.has_permission(db, current_user, tag_in.organization_id, "tag:create"):
        raise HTTPException(status_code=403, detail="Permission insuffisante pour créer un tag dans cette organisation")

    existing = tag_repo.get_tag_by_value(db, tag_in.value)
    if existing:
        raise HTTPException(status_code=400, detail="Ce tag existe déjà.")

    tag = tag_repo.create_tag(db, value=tag_in.value)
    audit.log_action(db, current_user.id, "Création tag", f"Tag '{tag.value}' créé pour l'organisation {tag_in.organization_id}")
    return response.success_response(tag, "Tag créé avec succès")

@router.delete(
    "/{tag_id}",
    response_model=dict,
    summary="Supprimer un tag",
    description="Supprime un tag s'il est autorisé."
)
def delete_tag(tag_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    tag = tag_repo.get_tag(db, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag non trouvé")

    # On cherche l'organisation liée au tag via une policy, un groupe, un user, un élément ou un environnement
    org_id = None
    if tag.policies:
        org_id = tag.policies[0].organization_id
    elif tag.groups:
        org_id = tag.groups[0].organization_id
    elif tag.users and tag.users[0].organizations:
        org_id = tag.users[0].organizations[0].id
    elif tag.elements and tag.elements[0].environment:
        org_id = tag.elements[0].environment.organization_id
    elif tag.environments:
        org_id = tag.environments[0].organization_id

    if not org_id or not permissions.has_permission(db, current_user, org_id, "tag:delete"):
        raise HTTPException(status_code=403, detail="Permission insuffisante pour supprimer ce tag")

    audit.log_action(db, current_user.id, "Suppression tag", f"Tag '{tag.value}' supprimé (id={tag.id})")
    tag_repo.delete_tag(db, tag)
    return response.success_response(None, "Tag supprimé avec succès")

@router.get(
    "/{tag_id}/groups",
    response_model=dict,
    summary="Groupes liés à un tag",
    description="Renvoie les groupes associés à un tag."
)
def get_tag_groups(tag_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    tag = tag_repo.get_tag(db, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag non trouvé")
    org_id = tag.groups[0].organization_id if tag.groups else None
    if not org_id or not permissions.has_permission(db, current_user, org_id, "tag:read"):
        raise HTTPException(status_code=403, detail="Permission insuffisante pour lire ce tag")
    return response.success_response(tag.groups, "Groupes récupérés")

@router.get(
    "/{tag_id}/users",
    response_model=dict,
    summary="Utilisateurs liés à un tag",
    description="Renvoie les utilisateurs associés à un tag."
)
def get_tag_users(tag_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    tag = tag_repo.get_tag(db, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag non trouvé")
    org_id = tag.users[0].organizations[0].id if tag.users and tag.users[0].organizations else None
    if not org_id or not permissions.has_permission(db, current_user, org_id, "tag:read"):
        raise HTTPException(status_code=403, detail="Permission insuffisante pour lire ce tag")
    return response.success_response(tag.users, "Utilisateurs récupérés")

@router.get(
    "/{tag_id}/policies",
    response_model=dict,
    summary="Policies liées à un tag",
    description="Renvoie les policies associées à un tag."
)
def get_tag_policies(tag_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    tag = tag_repo.get_tag(db, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag non trouvé")
    org_id = tag.policies[0].organization_id if tag.policies else None
    if not org_id or not permissions.has_permission(db, current_user, org_id, "tag:read"):
        raise HTTPException(status_code=403, detail="Permission insuffisante pour lire ce tag")
    return response.success_response(tag.policies, "Policies récupérées")

@router.get(
    "/{tag_id}/elements",
    response_model=dict,
    summary="Éléments liés à un tag",
    description="Renvoie les éléments associés à un tag."
)
def get_tag_elements(tag_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    tag = tag_repo.get_tag(db, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag non trouvé")

    # Vérifier si le tag a des éléments
    if not tag.elements:
        return response.success_response([], "Aucun élément associé à ce tag")

    # Vérifier les permissions sur l'organisation de l'environnement du premier élément
    org_id = tag.elements[0].environment.organization_id if tag.elements and tag.elements[0].environment else None
    if not org_id or not permissions.has_permission(db, current_user, org_id, "tag:read"):
        raise HTTPException(status_code=403, detail="Permission insuffisante pour lire ce tag")

    return response.success_response(tag.elements, "Éléments récupérés")

@router.get(
    "/{tag_id}/environments",
    response_model=dict,
    summary="Environnements liés à un tag",
    description="Renvoie les environnements associés à un tag."
)
def get_tag_environments(tag_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    tag = tag_repo.get_tag(db, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag non trouvé")

    # Vérifier si le tag a des environnements
    if not tag.environments:
        return response.success_response([], "Aucun environnement associé à ce tag")

    # Vérifier les permissions sur l'organisation du premier environnement
    org_id = tag.environments[0].organization_id if tag.environments else None
    if not org_id or not permissions.has_permission(db, current_user, org_id, "tag:read"):
        raise HTTPException(status_code=403, detail="Permission insuffisante pour lire ce tag")

    return response.success_response(tag.environments, "Environnements récupérés")
