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
    description="Renvoie toutes les fonctions si l'utilisateur a les droits requis.",
    responses={
        200: {"description": "Liste des fonctions récupérée avec succès"},
        401: {"description": "Non authentifié"},
        403: {"description": "Permission insuffisante"}
    }
)
def list_functions(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Ici on suppose que l'accès est global à toutes les fonctions
    if not permissions.has_permission(db, current_user, None, "function:read"):
        raise HTTPException(status_code=403, detail="Permission insuffisante pour lister les fonctions")
    functions = function_repo.list_functions(db)
    # Convert Function objects to FunctionOut objects for proper serialization
    serializable_functions = [FunctionOut.model_validate(func) for func in functions]
    return response.success_response(serializable_functions, "Liste des fonctions récupérée")

@router.get(
    "/{function_id}",
    response_model=dict,
    summary="Récupérer une fonction",
    description="Renvoie les informations d'une fonction spécifique.",
    responses={
        200: {"description": "Fonction récupérée avec succès"},
        401: {"description": "Non authentifié"},
        403: {"description": "Permission insuffisante"},
        404: {"description": "Fonction non trouvée"}
    }
)
def get_function(function_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    function = function_repo.get_function(db, function_id)
    if not function:
        raise HTTPException(status_code=404, detail="Fonction non trouvée")
    if not permissions.has_permission(db, current_user, None, "function:read"):
        raise HTTPException(status_code=403, detail="Permission insuffisante pour lire cette fonction")
    # Convert Function object to FunctionOut object for proper serialization
    serializable_function = FunctionOut.model_validate(function)
    return response.success_response(serializable_function, "Fonction récupérée")
