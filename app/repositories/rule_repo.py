# app/repositories/rule_repo.py
from typing import Type

from sqlalchemy.orm import Session
from ..models.rule import Rule

def create_rule(db: Session, policy_id: int, function_id: int,
                environment_id: int = None, element_id: int = None, access_schedule: dict = None) -> Rule:
    rule = Rule(
        policy_id=policy_id,
        function_id=function_id,
        environment_id=environment_id,
        element_id=element_id,
        access_schedule=access_schedule
    )
    db.add(rule)
    db.commit()
    db.refresh(rule)
    return rule

def get_rule(db: Session, rule_id: int) -> Type[Rule] | None:
    return db.query(Rule).filter(Rule.id == rule_id).first()

def delete_rule(db: Session, rule: Rule):
    db.delete(rule)
    db.commit()

def list_rules_for_policy(db: Session, policy_id: int):
    return db.query(Rule).filter(Rule.policy_id == policy_id).all()

def update_rule(db: Session, rule: Rule,
                function_id: int = None,
                environment_id: int = None,
                element_id: int = None,
                access_schedule: dict = None) -> Rule:
    if function_id is not None:
        rule.function_id = function_id
    if environment_id is not None:
        rule.environment_id = environment_id
    if element_id is not None:
        rule.element_id = element_id
    if access_schedule is not None:
        rule.access_schedule = access_schedule
    db.commit()
    db.refresh(rule)
    return rule
