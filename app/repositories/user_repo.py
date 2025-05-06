from sqlalchemy.orm import Session
from ..models.user import User
from ..models.tag import Tag
from ..models.organization import Organization
from ..helper.security import get_password_hash

def get_user(db: Session, user_id: int) -> User:
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str) -> User:
    return db.query(User).filter(User.email == email).first()

def create_user(
    db: Session,
    email: str,
    username: str,
    first_name: str,
    last_name: str,
    password: str,
    is_superadmin: bool = False
) -> User:
    hashed_password = get_password_hash(password)
    user = User(
        email=email,
        username=username,
        first_name=first_name,
        last_name=last_name,
        hashed_password=hashed_password,
        is_superadmin=is_superadmin
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, user: User):
    db.delete(user)
    db.commit()

def update_user(
    db: Session,
    user: User,
    email: str = None,
    username: str = None,
    first_name: str = None,
    last_name: str = None,
    password: str = None,
    is_superadmin: bool = None
) -> User:
    if email is not None:
        user.email = email
    if username is not None:
        user.username = username
    if first_name is not None:
        user.first_name = first_name
    if last_name is not None:
        user.last_name = last_name
    if is_superadmin is not None:
        user.is_superadmin = is_superadmin
    if password is not None:
        user.hashed_password = get_password_hash(password)
    db.commit()
    db.refresh(user)
    return user

def add_tag_to_user(db: Session, user: User, tag: Tag):
    if tag not in user.tags:
        user.tags.append(tag)
        db.commit()
        db.refresh(user)

def remove_tag_from_user(db: Session, user: User, tag: Tag):
    if tag in user.tags:
        user.tags.remove(tag)
        db.commit()
        db.refresh(user)

def add_user_to_organization(db: Session, user: User, organization: Organization):
    if organization not in user.organizations:
        user.organizations.append(organization)
        db.commit()
        db.refresh(user)

def remove_user_from_organization(db: Session, user: User, organization: Organization):
    if organization in user.organizations:
        user.organizations.remove(organization)
        db.commit()
        db.refresh(user)
