# app/repositories/tag_repo.py
from typing import Type

from sqlalchemy.orm import Session
from ..models.tag import Tag

def create_tag(db: Session, value: str) -> Tag:
    tag = Tag(value=value)
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return tag

def get_tag(db: Session, tag_id: int) -> Type[Tag] | None:
    return db.query(Tag).filter(Tag.id == tag_id).first()

def get_tag_by_value(db: Session, value: str) -> Type[Tag] | None:
    return db.query(Tag).filter(Tag.value == value).first()

def list_tags(db: Session):
    return db.query(Tag).all()

def delete_tag(db: Session, tag: Tag):
    db.delete(tag)
    db.commit()
