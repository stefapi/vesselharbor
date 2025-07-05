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
from ..schema.auth import BaseResponse

router = APIRouter(prefix="/functions", tags=["functions"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get(
    "",
    response_model=BaseResponse[List[FunctionOut]],
    summary="List functions",
    description="Returns all functions if the user has required permissions.",
    responses={
        200: {"description": "Function list retrieved successfully"},
        401: {"description": "Unauthenticated"},
        403: {"description": "Insufficient permissions"}
    }
)
def list_functions(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Here we assume global access to all functions
    if not permissions.has_permission(db, current_user, None, "function:read"):
        raise HTTPException(status_code=403, detail="Insufficient permissions to list functions")
    functions = function_repo.list_functions(db)
    # Convert Function objects to FunctionOut objects for proper serialization
    serializable_functions = [FunctionOut.model_validate(func) for func in functions]
    return response.success_response(serializable_functions, "Function list retrieved")

@router.get(
    "/{function_id}",
    response_model=BaseResponse[FunctionOut],
    summary="Get a function",
    description="Returns information for a specific function.",
    responses={
        200: {"description": "Function retrieved successfully"},
        401: {"description": "Unauthenticated"},
        403: {"description": "Insufficient permissions"},
        404: {"description": "Function not found"}
    }
)
def get_function(function_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    function = function_repo.get_function(db, function_id)
    if not function:
        raise HTTPException(status_code=404, detail="Function not found")
    if not permissions.has_permission(db, current_user, None, "function:read"):
        raise HTTPException(status_code=403, detail="Insufficient permissions to read this function")
    # Convert Function object to FunctionOut object for proper serialization
    serializable_function = FunctionOut.model_validate(function)
    return response.success_response(serializable_function, "Function retrieved")
