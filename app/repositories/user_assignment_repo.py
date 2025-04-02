from sqlalchemy.orm import Session
from ..models.user_assignment import UserAssignment

def create_assignment(db: Session, user_id: int, group_id: int, element_id: int = None) -> UserAssignment:
    assignment = UserAssignment(user_id=user_id, group_id=group_id, element_id=element_id)
    db.add(assignment)
    db.commit()
    db.refresh(assignment)
    return assignment

def get_assignment(db: Session, assignment_id: int) -> UserAssignment:
    return db.query(UserAssignment).filter(UserAssignment.id == assignment_id).first()

def list_assignments(db: Session, user_id: int = None, group_id: int = None, element_id: int = None):
    query = db.query(UserAssignment)
    if user_id:
        query = query.filter(UserAssignment.user_id == user_id)
    if group_id is not None:
        query = query.filter(UserAssignment.group_id == group_id)
    if element_id is not None:
        query = query.filter(UserAssignment.element_id == element_id)
    return query.all()

def delete_assignment(db: Session, assignment: UserAssignment):
    db.delete(assignment)
    db.commit()
