from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List

from ..models.user_assignment import UserAssignment
from ..models.user import User
from ..models.group import Group
from ..models.element import Element
from ..database.session import SessionLocal
from ..api.users import get_current_user
from ..repositories import user_assignment_repo
from ..helper import permissions, audit, response
from ..schema.user_assignment import UserAssignmentOut

router = APIRouter(prefix="/user-assignments", tags=["user_assignments"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class UpdateAssignment(BaseModel):
    element_id: Optional[int] = None

@router.put(
    "/{assignment_id}",
    response_model=dict,
    summary="Mettre à jour une affectation",
    description="Met à jour l'affectation d'un utilisateur à un groupe en ajoutant ou retirant l'affectation à un élément.",
    responses={
        404: {"description": "Affectation ou élément non trouvé"},
        403: {"description": "Permission insuffisante"}
    }
)
def update_user_assignment(
    assignment_id: int,
    update: UpdateAssignment,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    assignment = user_assignment_repo.get_assignment(db, assignment_id)
    if not assignment:
        raise HTTPException(status_code=404, detail="Affectation introuvée")
    target_env = assignment.group.environment_id if assignment.group and assignment.group.environment_id is not None else 0
    if not permissions.has_permission(db, current_user, target_env, "env:update"):
        raise HTTPException(status_code=403, detail="Permission insuffisante pour modifier l'affectation")
    if update.element_id is not None:
        element = db.query(Element).filter(Element.id == update.element_id).first()
        if not element:
            raise HTTPException(status_code=404, detail="Élément non trouvé")
        if assignment.group.environment_id is not None and element.environment_id != assignment.group.environment_id:
            raise HTTPException(status_code=400, detail="L'élément n'appartient pas au même environnement")
        assignment.element_id = element.id
    else:
        assignment.element_id = None
    db.commit()
    db.refresh(assignment)
    audit.log_action(db, current_user.id, "Mise à jour affectation",
                     f"Affectation {assignment.id} mise à jour: element_id={assignment.element_id}")
    return response.success_response(
        {"assignment_id": assignment.id, "element_id": assignment.element_id},
        "Affectation mise à jour"
    )

@router.get(
    "/",
    response_model=dict,
    summary="Lister les affectations",
    description="Liste les affectations (user_assignments) avec pagination et filtrage.",
    responses={}
)
def list_user_assignments(
    user_id: Optional[int] = None,
    group_id: Optional[int] = None,
    element_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    assignments = user_assignment_repo.list_assignments(db, user_id=user_id, group_id=group_id, element_id=element_id)
    assignments = assignments[skip: skip + limit]
    return response.success_response(assignments, "Liste des affectations récupérée")
