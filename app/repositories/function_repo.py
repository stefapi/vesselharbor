# app/repositories/function_repo.py
from sqlalchemy.orm import Session
from ..models.function import Function

def list_functions(db: Session):
    return db.query(Function).all()

def get_function(db: Session, function_id: int):
    return db.query(Function).filter(Function.id == function_id).first()

def create_function(db: Session, name: str, description: str = None) -> Function:
    func = Function(name=name, description=description)
    db.add(func)
    db.commit()
    db.refresh(func)
    return func

def update_function(db: Session, func: Function, name: str = None, description: str = None) -> Function:
    if name:
        func.name = name
    if description is not None:
        func.description = description
    db.commit()
    db.refresh(func)
    return func

def delete_function(db: Session, func: Function):
    db.delete(func)
    db.commit()
