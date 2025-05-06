# app/repositories/element_repo.py
from sqlalchemy.orm import Session
from ..models.element import Element

def create_element(db: Session, environment_id: int, name: str, description: str = None) -> Element:
    element = Element(name=name, description=description, environment_id=environment_id)
    db.add(element)
    db.commit()
    db.refresh(element)
    return element

def get_element(db: Session, element_id: int) -> Element:
    return db.query(Element).filter(Element.id == element_id).first()

def update_element(db: Session, element: Element, name: str = None, description: str = None) -> Element:
    if name is not None:
        element.name = name
    if description is not None:
        element.description = description
    db.commit()
    db.refresh(element)
    return element

def delete_element(db: Session, element: Element):
    db.delete(element)
    db.commit()

def list_elements_by_environment(db: Session, environment_id: int):
    return db.query(Element).filter(Element.environment_id == environment_id).all()
