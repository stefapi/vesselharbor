from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from ..schema.element import ElementCreate, ElementUpdate, ElementOut
from ..models.element import Element
from ..models.user import User
from ..database.session import SessionLocal
from ..repositories import element_repo
from ..api.users import get_current_user
from ..helper import permissions, audit, response

router = APIRouter(prefix="/elements", tags=["elements"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post(
    "/{environment_id}",
    response_model=dict,
    summary="Créer un élément",
    description="Crée un élément dans un environnement donné.",
    responses={
        403: {"description": "Permission insuffisante"},
        500: {"description": "Erreur interne"}
    }
)
def create_element(environment_id: int, element_in: ElementCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not permissions.has_permission(db, current_user, environment_id, "element:create"):
        raise HTTPException(status_code=403, detail="Permission insuffisante pour créer un élément")
    element = element_repo.create_element(db, environment_id=environment_id, name=element_in.name, description=element_in.description)
    audit.log_action(db, current_user.id, "Création élément", f"Création de l'élément '{element.name}' dans l'environnement {environment_id}")
    return response.success_response(element, "Élément créé avec succès")

@router.get(
    "/{element_id}",
    response_model=dict,
    summary="Récupérer un élément",
    description="Renvoie les informations d'un élément spécifique.",
    responses={
        404: {"description": "Élément non trouvé"},
        403: {"description": "Permission insuffisante"}
    }
)
def get_element(element_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    element = element_repo.get_element(db, element_id)
    if not element:
        raise HTTPException(status_code=404, detail="Élément non trouvé")
    if not permissions.has_permission(db, current_user, element.environment_id, "env:read"):
        raise HTTPException(status_code=403, detail="Permission insuffisante pour visualiser cet élément")
    return response.success_response(element, "Élément récupéré")

@router.put(
    "/{element_id}",
    response_model=dict,
    summary="Mettre à jour un élément",
    description="Modifie les informations d'un élément.",
    responses={
        404: {"description": "Élément non trouvé"},
        403: {"description": "Permission insuffisante"}
    }
)
def update_element(element_id: int, element_in: ElementUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    element = element_repo.get_element(db, element_id)
    if not element:
        raise HTTPException(status_code=404, detail="Élément non trouvé")
    if not permissions.has_permission(db, current_user, element.environment_id, "element:update"):
        raise HTTPException(status_code=403, detail="Permission insuffisante pour modifier cet élément")
    element = element_repo.update_element(db, element, name=element_in.name, description=element_in.description)
    audit.log_action(db, current_user.id, "Mise à jour élément", f"Mise à jour de l'élément '{element.name}' (ID {element.id})")
    return response.success_response(element, "Élément mis à jour")

@router.delete(
    "/{element_id}",
    response_model=dict,
    summary="Supprimer un élément",
    description="Supprime un élément donné.",
    responses={
        404: {"description": "Élément non trouvé"},
        403: {"description": "Permission insuffisante"}
    }
)
def delete_element(element_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    element = element_repo.get_element(db, element_id)
    if not element:
        raise HTTPException(status_code=404, detail="Élément non trouvé")
    if not permissions.has_permission(db, current_user, element.environment_id, "element:delete"):
        raise HTTPException(status_code=403, detail="Permission insuffisante pour supprimer cet élément")
    element_repo.delete_element(db, element)
    audit.log_action(db, current_user.id, "Suppression élément", f"Suppression de l'élément '{element.name}' (ID {element.id})")
    return response.success_response(None, "Élément supprimé")

@router.get(
    "/environment/{environment_id}",
    response_model=dict,
    summary="Lister les éléments d'un environnement",
    description="Liste les éléments d'un environnement avec pagination et filtrage par nom.",
    responses={
        403: {"description": "Permission insuffisante"}
    }
)
def list_elements(
    environment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    name: Optional[str] = None
):
    if not permissions.has_permission(db, current_user, environment_id, "env:read"):
        raise HTTPException(status_code=403, detail="Permission insuffisante pour lister les éléments de cet environnement")
    query = db.query(Element).filter(Element.environment_id == environment_id)
    if name:
        query = query.filter(Element.name.ilike(f"%{name}%"))
    elements = query.offset(skip).limit(limit).all()
    return response.success_response(elements, "Liste des éléments récupérée")
