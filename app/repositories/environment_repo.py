from sqlalchemy.orm import Session
from ..models.environment import Environment

def get_environment(db: Session, env_id: int) -> Environment:
    return db.query(Environment).filter(Environment.id == env_id).first()

def get_environment_by_name(db: Session, name: str) -> Environment:
    return db.query(Environment).filter(Environment.name == name).first()

def create_environment(db: Session, name: str) -> Environment:
    environment = Environment(name=name)
    db.add(environment)
    db.commit()
    db.refresh(environment)
    return environment

def delete_environment(db: Session, environment: Environment):
    db.delete(environment)
    db.commit()
