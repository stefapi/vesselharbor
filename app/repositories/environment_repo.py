# app/repositories/environment_repo.py
from sqlalchemy.orm import Session
from ..models.environment import Environment
from . import element_repo
from ..models.tag import Tag


def get_environment(db: Session, env_id: int) -> Environment:
    return db.query(Environment).filter(Environment.id == env_id).first()

def get_environment_by_name(db: Session, name: str) -> Environment:
    return db.query(Environment).filter(Environment.name == name).first()

def create_environment(db: Session, name: str, organization_id: int = None, description: str = None) -> Environment:
    # If organization_id is not provided, create a test organization for backward compatibility with tests
    if organization_id is None:
        from ..models.organization import Organization
        test_org = Organization(name=f"test_org_for_{name}", description=f"Test organization for {name}")
        db.add(test_org)
        db.commit()
        db.refresh(test_org)
        organization_id = test_org.id

    environment = Environment(name=name, organization_id=organization_id, description=description)
    db.add(environment)
    db.commit()
    db.refresh(environment)
    return environment

def delete_environment(db: Session, environment: Environment):
    # Delete all elements related to this environment
    elements = element_repo.list_elements_by_environment(db, environment.id)
    for element in elements:
        element_repo.delete_element(db, element)

    # Delete the environment (rules will be deleted automatically due to CASCADE)
    db.delete(environment)
    db.commit()

def add_tag_to_environment(db: Session, environment: Environment, tag: Tag):
    if tag not in environment.tags:
        environment.tags.append(tag)
        db.commit()
        db.refresh(environment)

def remove_tag_from_environment(db: Session, environment: Environment, tag: Tag):
    if tag in environment.tags:
        environment.tags.remove(tag)
        db.commit()
        db.refresh(environment)

        # Check if the tag is still referenced by any entity
        from ..repositories import tag_repo
        if not tag_repo.is_tag_referenced(db, tag):
            # If the tag is no longer referenced, delete it
            tag_repo.delete_tag(db, tag)
