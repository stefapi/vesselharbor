from typing import List, Optional, Type
from sqlalchemy.orm import Session
from ..models.policy import Policy
from ..models.user import User
from ..models.group import Group
from ..models.tag import Tag
from ..schema.policy import PolicyCreate, PolicyUpdate


def create_policy(db: Session, policy_in: PolicyCreate) -> Policy:
    policy = Policy(
        name=policy_in.name,
        description=policy_in.description,
        access_schedule=policy_in.access_schedule,
        organization_id=policy_in.organization_id,
    )
    db.add(policy)
    db.commit()
    db.refresh(policy)
    return policy


def get_policy(db: Session, policy_id: int) -> Optional[Type[Policy]]:
    return db.query(Policy).filter(Policy.id == policy_id).first()


def list_policies(db: Session, organization_id: int = None, skip: int = 0, limit: int = 100) -> List[Policy]:
    query = db.query(Policy)
    if organization_id is not None:
        query = query.filter(Policy.organization_id == organization_id)
    return query.offset(skip).limit(limit).all()


def update_policy(db: Session, policy: Policy, policy_in: PolicyUpdate) -> Policy:
    for field, value in policy_in.dict(exclude_unset=True).items():
        setattr(policy, field, value)
    db.commit()
    db.refresh(policy)
    return policy


def delete_policy(db: Session, policy: Policy):
    db.delete(policy)
    db.commit()


# --- Users ---
def add_user(db: Session, policy: Policy, user: User):
    if user not in policy.users:
        policy.users.append(user)
        db.commit()
        db.refresh(policy)


def remove_user(db: Session, policy: Policy, user: User):
    if user in policy.users:
        policy.users.remove(user)
        db.commit()
        db.refresh(policy)


# --- Groups ---
def add_group(db: Session, policy: Policy, group: Group):
    if group not in policy.groups:
        policy.groups.append(group)
        db.commit()
        db.refresh(policy)


def remove_group(db: Session, policy: Policy, group: Group):
    if group in policy.groups:
        policy.groups.remove(group)
        db.commit()
        db.refresh(policy)


# --- Tags ---
def add_tag(db: Session, policy: Policy, tag: Tag):
    if tag not in policy.tags:
        policy.tags.append(tag)
        db.commit()
        db.refresh(policy)


def remove_tag(db: Session, policy: Policy, tag: Tag):
    if tag in policy.tags:
        policy.tags.remove(tag)
        db.commit()
        db.refresh(policy)
