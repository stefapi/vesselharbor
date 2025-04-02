from sqlalchemy.orm import Session
from ..models.group import Group
from ..models.user_assignment import UserAssignment

def create_group(db: Session, environment_id: int, name: str, description: str = None) -> Group:
    group = Group(name=name, description=description, environment_id=environment_id)
    db.add(group)
    db.commit()
    db.refresh(group)
    return group

def get_group(db: Session, group_id: int) -> Group:
    return db.query(Group).filter(Group.id == group_id).first()

def update_group(db: Session, group: Group, name: str = None, description: str = None) -> Group:
    if name is not None:
        group.name = name
    if description is not None:
        group.description = description
    db.commit()
    db.refresh(group)
    return group

def delete_group(db: Session, group: Group):
    db.delete(group)
    db.commit()

def list_groups_by_environment(db: Session, environment_id: int):
    return db.query(Group).filter(Group.environment_id == environment_id).all()

def assign_user_to_group(db: Session, group, user):
    # On suppose que l'utilisateur doit déjà être affecté à l'environnement
    ue = db.query(UserAssignment).filter(
         UserAssignment.user_id == user.id,
         UserAssignment.environment_id == group.environment_id
    ).first()
    if ue:
         ue.group_id = group.id
         db.commit()
         db.refresh(ue)
    else:
         raise Exception("L'utilisateur n'est pas affecté à l'environnement de ce groupe.")

def remove_user_from_group(db: Session, group, user):
    ue = db.query(UserAssignment).filter(
         UserAssignment.user_id == user.id,
         UserAssignment.environment_id == group.environment_id,
         UserAssignment.group_id == group.id
    ).first()
    if ue:
         ue.group_id = None
         db.commit()
         db.refresh(ue)

