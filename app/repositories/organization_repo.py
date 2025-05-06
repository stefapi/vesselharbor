# app/repositories/organization_repo.py
from sqlalchemy.orm import Session

from ..models import User
from ..models.organization import Organization

def create_organization(db: Session, name: str, description: str = None) -> Organization:
    org = Organization(name=name, description=description)
    db.add(org)
    db.commit()
    db.refresh(org)
    return org

def get_organization(db: Session, organization_id: int) -> Organization:
    return db.query(Organization).filter(Organization.id == organization_id).first()

def delete_organization(db: Session, organization: Organization):
    db.delete(organization)
    db.commit()

def list_organizations(db: Session):
    return db.query(Organization).all()

def update_organization(db: Session, organization: Organization, name: str = None, description: str = None) -> Organization:
    if name is not None:
        organization.name = name
    if description is not None:
        organization.description = description
    db.commit()
    db.refresh(organization)
    return organization

def add_user_to_organization(db: Session, organization: Organization, user: User):
    if user not in organization.users:
        organization.users.append(user)
        db.commit()
        db.refresh(organization)

def remove_user_from_organization(db: Session, organization: Organization, user: User):
    if user in organization.users:
        organization.users.remove(user)
        db.commit()
        db.refresh(organization)
