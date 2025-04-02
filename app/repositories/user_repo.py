from sqlalchemy.orm import Session
from ..models.user import User
from ..helper.security import get_password_hash

def get_user(db: Session, user_id: int) -> User:
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str) -> User:
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, email: str, password: str, is_superadmin: bool) -> User:
    hashed_password = get_password_hash(password)
    user = User(email=email, hashed_password=hashed_password, is_superadmin=is_superadmin)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, user: User):
    db.delete(user)
    db.commit()
