from sqlalchemy.orm import Session
from ..models.group import Group
from ..models.tag import Tag
from ..models.user import User

def create_group(db: Session, organization_id: int, name: str, description: str = None) -> Group:
    group = Group(name=name, description=description, organization_id=organization_id)
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

def list_groups_by_organization(db: Session, organization_id: int):
    return db.query(Group).filter(Group.organization_id == organization_id).all()

def add_user_to_group(db: Session, group: Group, user: User):
    if user not in group.users:
        group.users.append(user)
        db.commit()
        db.refresh(group)

def remove_user_from_group(db: Session, group: Group, user: User):
    if user in group.users:
        group.users.remove(user)
        db.commit()
        db.refresh(group)

def add_tag_to_group(db: Session, group: Group, tag: Tag):
    if tag not in group.tags:
        group.tags.append(tag)
        db.commit()
        db.refresh(group)

def remove_tag_from_group(db: Session, group: Group, tag: Tag):
    if tag in group.tags:
        group.tags.remove(tag)
        db.commit()
        db.refresh(group)
