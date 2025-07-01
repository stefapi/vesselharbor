# app/repositories/element_repo.py
from sqlalchemy.orm import Session
from ..models.element import Element
from ..models.tag import Tag


def create_element(db: Session, environment_id: int, name: str, description: str = None) -> Element:
    element = Element(name=name, description=description, environment_id=environment_id)
    db.add(element)
    db.commit()
    db.refresh(element)
    return element

def get_element(db: Session, element_id: int) -> Element:
    return db.query(Element).filter(Element.id == element_id).first()

def update_element(db: Session, element: Element, name: str = None, description: str = None, environment_id: int = None) -> Element:
    if name is not None:
        element.name = name
    if description is not None:
        element.description = description
    if environment_id is not None:
        element.environment_id = environment_id
    db.commit()
    db.refresh(element)
    return element

def delete_element(db: Session, element: Element):
    db.delete(element)
    db.commit()

def list_elements_by_environment(db: Session, environment_id: int):
    return db.query(Element).filter(Element.environment_id == environment_id).all()

def add_tag_to_element(db: Session, element: Element, tag: Tag):
    if tag not in element.tags:
        element.tags.append(tag)
        db.commit()
        db.refresh(element)

def remove_tag_from_element(db: Session, element: Element, tag: Tag):
    if tag in element.tags:
        element.tags.remove(tag)
        db.commit()
        db.refresh(element)

        # Check if the tag is still referenced by any entity
        from ..repositories import tag_repo
        if not tag_repo.is_tag_referenced(db, tag):
            # If the tag is no longer referenced, delete it
            tag_repo.delete_tag(db, tag)
