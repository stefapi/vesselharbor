from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from ..schema.element import ElementCreate, ElementUpdate
from ..models.element import Element
from ..models.environment import Environment
from ..models.user import User
from ..database.session import SessionLocal
from ..repositories import element_repo, tag_repo
from ..api.users import get_current_user
from ..helper import permissions, audit, response

router = APIRouter(prefix="/elements", tags=["elements"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# TODO Check toutes les permissions dans les API endpoints, ajouter les manquantes dans le seed

# TODO bien détailler toutes les documentations dont les responses

@router.post(
    "/{environment_id}",
    response_model=dict,
    summary="Créer un élément",
    description="Crée un élément dans un environnement donné.",
    responses={
        200: {"description": "Élément créé avec succès"},
        401: {"description": "Non authentifié"},
        403: {"description": "Permission insuffisante"},
        404: {"description": "Environnement non trouvé"},
    }
)
def create_element(
    environment_id: int,
    element_in: ElementCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    env = db.query(Environment).filter_by(id=environment_id).first()
    if not env:
        raise HTTPException(status_code=404, detail="Environnement non trouvé")
    # TODO ajouter un generate_codename ici
    if not permissions.has_permission(db, current_user, env.organization_id, "element:create"):
        raise HTTPException(status_code=403, detail="Permission insuffisante pour créer un élément")

    element = element_repo.create_element(db, environment_id, element_in.name, element_in.description)
    audit.log_action(db, current_user.id, "Création élément", f"Élément '{element.name}' dans env {environment_id}")
    return response.success_response(element, "Élément créé avec succès")


@router.get(
    "/{element_id}",
    response_model=dict,
    summary="Récupérer un élément",
    description="Renvoie les informations d'un élément spécifique.",
    responses={
        200: {"description": "Élément récupéré avec succès"},
        401: {"description": "Non authentifié"},
        403: {"description": "Permission insuffisante"},
        404: {"description": "Élément non trouvé"},
    }
)
def get_element(
    element_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    element = element_repo.get_element(db, element_id)
    if not element:
        raise HTTPException(status_code=404, detail="Élément non trouvé")

    org_id = element.environment.organization_id
    if not permissions.has_permission(db, current_user, org_id, "element:read"):
        raise HTTPException(status_code=403, detail="Permission insuffisante pour visualiser cet élément")

    return response.success_response(element, "Élément récupéré")


@router.put(
    "/{element_id}",
    response_model=dict,
    summary="Mettre à jour un élément",
    description="Modifie les informations d'un élément.",
    responses={
        200: {"description": "Élément mis à jour avec succès"},
        401: {"description": "Non authentifié"},
        403: {"description": "Permission insuffisante"},
        404: {"description": "Élément non trouvé"},
    }
)
def update_element(
    element_id: int,
    element_in: ElementUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    element = element_repo.get_element(db, element_id)
    if not element:
        raise HTTPException(status_code=404, detail="Élément non trouvé")

    org_id = element.environment.organization_id
    if not permissions.has_permission(db, current_user, org_id, "element:update"):
        raise HTTPException(status_code=403, detail="Permission insuffisante pour modifier cet élément")

    original_env_id = element.environment_id

    # If environment_id is provided and different from current, check permissions for the new environment
    if element_in.environment_id is not None and original_env_id != element_in.environment_id:
        # Get the new environment to check its organization
        new_env = db.query(Environment).filter_by(id=element_in.environment_id).first()
        if not new_env:
            raise HTTPException(status_code=404, detail="Nouvel environnement non trouvé")

        # Check if user has permission to access the new environment's organization
        if not permissions.has_permission(db, current_user, new_env.organization_id, "element:update"):
            raise HTTPException(status_code=403, detail="Permission insuffisante pour déplacer l'élément vers le nouvel environnement")

    updated = element_repo.update_element(db, element, name=element_in.name, description=element_in.description, environment_id=element_in.environment_id)

    # Create appropriate audit log message
    if element_in.environment_id is not None and original_env_id != element_in.environment_id:
        audit.log_action(db, current_user.id, "Mise à jour élément", f"Mise à jour de l'élément '{updated.name}' (ID {updated.id}) - Changement d'environnement: {original_env_id} → {updated.environment_id}")
    else:
        audit.log_action(db, current_user.id, "Mise à jour élément", f"Mise à jour de l'élément '{updated.name}' (ID {updated.id})")
    return response.success_response(updated, "Élément mis à jour")


@router.delete(
    "/{element_id}",
    response_model=dict,
    summary="Supprimer un élément",
    description="Supprime un élément donné.",
    responses={
        200: {"description": "Élément supprimé avec succès"},
        401: {"description": "Non authentifié"},
        403: {"description": "Permission insuffisante"},
        404: {"description": "Élément non trouvé"},
    }
)
def delete_element(
    element_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    element = element_repo.get_element(db, element_id)
    if not element:
        raise HTTPException(status_code=404, detail="Élément non trouvé")

    org_id = element.environment.organization_id
    if not permissions.has_permission(db, current_user, org_id, "element:delete"):
        raise HTTPException(status_code=403, detail="Permission insuffisante pour supprimer cet élément")

    element_repo.delete_element(db, element)
    audit.log_action(db, current_user.id, "Suppression élément", f"Suppression de l'élément '{element.name}' (ID {element.id})")
    return response.success_response(None, "Élément supprimé")

@router.get(
    "/{element_id}/tags",
    response_model=dict,
    summary="Lister les tags d'un élément",
    description="Récupère tous les tags associés à un élément.",
    responses={
        200: {"description": "Tags récupérés avec succès"},
        401: {"description": "Non authentifié"},
        403: {"description": "Permission insuffisante"},
        404: {"description": "Élément non trouvé"}
    }
)
def list_element_tags(
    element_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Vérifier que l'élément existe
    element = db.query(Element).filter(Element.id == element_id).first()
    if not element:
        raise HTTPException(status_code=404, detail="Élément non trouvé")

    # Vérifier les permissions sur l'organisation de l'environnement de l'élément
    org_id = element.environment.organization_id
    if not permissions.has_permission(db, current_user, org_id, "element:read"):
        raise HTTPException(status_code=403, detail="Permission insuffisante pour accéder à cet élément")

    # Convertir les objets Tag en TagOut pour une sérialisation correcte
    from ..schema.tag import TagOut
    serializable_tags = [TagOut.model_validate(tag) for tag in element.tags]

    return response.success_response(serializable_tags, "Tags de l'élément récupérés avec succès")


@router.post(
    "/{element_id}/tags/{tag_id}",
    response_model=dict,
    summary="Ajouter un tag à un élément",
    description="Associe un tag existant à un élément."
)
def add_tag_to_element(
    element_id: int,
    tag_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Vérifier que l'élément existe
    element = db.query(Element).filter(Element.id == element_id).first()
    if not element:
        raise HTTPException(status_code=404, detail="Élément non trouvé")

    # Vérifier les permissions sur l'organisation de l'environnement de l'élément
    org_id = element.environment.organization_id
    if not permissions.has_permission(db, current_user, org_id, "element:update"):
        raise HTTPException(status_code=403, detail="Permission insuffisante pour modifier cet élément")

    # Vérifier que le tag existe
    tag = tag_repo.get_tag(db, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag non trouvé")

    # Vérifier si le tag est déjà associé à l'élément
    if tag in element.tags:
        return response.success_response(element, "Le tag est déjà associé à cet élément")

    # Ajouter le tag à l'élément
    element.tags.append(tag)
    db.commit()

    audit.log_action(db, current_user.id, "Ajout tag à élément", f"Tag '{tag.value}' ajouté à l'élément '{element.name}'")
    return response.success_response(element, "Tag ajouté à l'élément avec succès")


@router.delete(
    "/{element_id}/tags/{tag_id}",
    response_model=dict,
    summary="Retirer un tag d'un élément",
    description="Retire l'association entre un tag et un élément."
)
def remove_tag_from_element(
    element_id: int,
    tag_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Vérifier que l'élément existe
    element = db.query(Element).filter(Element.id == element_id).first()
    if not element:
        raise HTTPException(status_code=404, detail="Élément non trouvé")

    # Vérifier les permissions sur l'organisation de l'environnement de l'élément
    org_id = element.environment.organization_id
    if not permissions.has_permission(db, current_user, org_id, "element:update"):
        raise HTTPException(status_code=403, detail="Permission insuffisante pour modifier cet élément")

    # Vérifier que le tag existe
    tag = tag_repo.get_tag(db, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag non trouvé")

    # Vérifier si le tag est associé à l'élément
    if tag not in element.tags:
        return response.success_response(element, "Le tag n'est pas associé à cet élément")

    # Retirer le tag de l'élément
    element.tags.remove(tag)
    db.commit()

    audit.log_action(db, current_user.id, "Retrait tag d'élément", f"Tag '{tag.value}' retiré de l'élément '{element.name}'")
    return response.success_response(element, "Tag retiré de l'élément avec succès")
