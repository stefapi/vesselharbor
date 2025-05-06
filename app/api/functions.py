# app/api/functions.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..models.function import Function
from ..models.user import User
from ..database.session import SessionLocal
from ..api.users import get_current_user
from ..helper import permissions, audit, response
from ..repositories import function_repo
from ..schema.function import FunctionOut, FunctionCreate, FunctionUpdate

router = APIRouter(prefix="/functions", tags=["functions"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get(
    "",
    response_model=dict,
    summary="Lister les fonctions",
    description="Renvoie toutes les fonctions si l'utilisateur a les droits requis."
)
def list_functions(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Ici on suppose que l'accès est global à toutes les fonctions
    if not permissions.has_global_permission(current_user, "function:read"):
        raise HTTPException(status_code=403, detail="Permission insuffisante pour lister les fonctions")
    functions = function_repo.list_functions(db)
    return response.success_response(functions, "Liste des fonctions récupérée")

@router.get(
    "/{function_id}",
    response_model=dict,
    summary="Récupérer une fonction",
    description="Renvoie les informations d'une fonction spécifique."
)
def get_function(function_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    function = function_repo.get_function(db, function_id)
    if not function:
        raise HTTPException(status_code=404, detail="Fonction non trouvée")
    if not permissions.has_global_permission(current_user, "function:read"):
        raise HTTPException(status_code=403, detail="Permission insuffisante pour lire cette fonction")
    return response.success_response(function, "Fonction récupérée")

@router.post(
    "",
    response_model=dict,
    summary="Créer une fonction",
    description="Crée une nouvelle fonction.",
)
def create_function(data: FunctionCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not permissions.has_global_permission(current_user, "function:create"):
        raise HTTPException(status_code=403, detail="Permission insuffisante pour créer une fonction")
    function = function_repo.create_function(db, name=data.name, description=data.description)
    audit.log_action(db, current_user.id, "Création fonction", f"Fonction créée : {function.name}")
    return response.success_response(function, "Fonction créée avec succès")

@router.put(
    "/{function_id}",
    response_model=dict,
    summary="Mettre à jour une fonction",
    description="Met à jour une fonction existante."
)
def update_function(function_id: int, data: FunctionUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    function = function_repo.get_function(db, function_id)
    if not function:
        raise HTTPException(status_code=404, detail="Fonction non trouvée")
    if not permissions.has_global_permission(current_user, "function:update"):
        raise HTTPException(status_code=403, detail="Permission insuffisante pour modifier cette fonction")
    function = function_repo.update_function(db, function, name=data.name, description=data.description)
    audit.log_action(db, current_user.id, "Mise à jour fonction", f"Fonction mise à jour : {function.name}")
    return response.success_response(function, "Fonction mise à jour avec succès")

@router.delete(
    "/{function_id}",
    response_model=dict,
    summary="Supprimer une fonction",
    description="Supprime une fonction."
)
def delete_function(function_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    function = function_repo.get_function(db, function_id)
    if not function:
        raise HTTPException(status_code=404, detail="Fonction non trouvée")
    if not permissions.has_global_permission(current_user, "function:delete"):
        raise HTTPException(status_code=403, detail="Permission insuffisante pour supprimer cette fonction")
    audit.log_action(db, current_user.id, "Suppression fonction", f"Fonction supprimée : {function.name}")
    function_repo.delete_function(db, function)
    return response.success_response(None, "Fonction supprimée avec succès")
