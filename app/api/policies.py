from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

from ..database.session import SessionLocal
from ..models.user import User
from ..repositories import policy_repo, user_repo, group_repo, tag_repo
from ..schema.policy import PolicyCreate, PolicyUpdate
from ..api.users import get_current_user
from ..helper import permissions, audit, response

router = APIRouter(prefix="/policies", tags=["policies"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("", response_model=dict)
def list_policies(
    organization_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not permissions.has_permission(db, current_user, organization_id, "policy:read"):
        raise HTTPException(status_code=403, detail="Permission insuffisante")
    policies = policy_repo.list_policies(db, organization_id, skip, limit)
    return response.success_response(policies, "Policies récupérées")

@router.get("/{policy_id}", response_model=dict)
def get_policy(policy_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    policy = policy_repo.get_policy(db, policy_id)
    if not policy:
        raise HTTPException(status_code=404, detail="Policy non trouvée")
    if not permissions.has_permission(db, current_user, policy.organization_id, "policy:read"):
        raise HTTPException(status_code=403, detail="Permission insuffisante")
    return response.success_response(policy, "Policy récupérée")

@router.post("", response_model=dict)
def create_policy(policy_in: PolicyCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not permissions.has_permission(db, current_user, policy_in.organization_id, "policy:create"):
        raise HTTPException(status_code=403, detail="Permission insuffisante")
    policy = policy_repo.create_policy(db, policy_in)
    audit.log_action(db, current_user.id, "Création policy", f"Policy '{policy.name}' créée")
    return response.success_response(policy, "Policy créée")

@router.put("/{policy_id}", response_model=dict)
def update_policy(policy_id: int, policy_in: PolicyUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    policy = policy_repo.get_policy(db, policy_id)
    if not policy:
        raise HTTPException(status_code=404, detail="Policy non trouvée")
    if not permissions.has_permission(db, current_user, policy.organization_id, "policy:update"):
        raise HTTPException(status_code=403, detail="Permission insuffisante")
    policy = policy_repo.update_policy(db, policy, policy_in)
    audit.log_action(db, current_user.id, "Mise à jour policy", f"Policy '{policy.name}' mise à jour")
    return response.success_response(policy, "Policy mise à jour")

@router.delete("/{policy_id}", response_model=dict)
def delete_policy(policy_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    policy = policy_repo.get_policy(db, policy_id)
    if not policy:
        raise HTTPException(status_code=404, detail="Policy non trouvée")
    if not permissions.has_permission(db, current_user, policy.organization_id, "policy:delete"):
        raise HTTPException(status_code=403, detail="Permission insuffisante")
    policy_repo.delete_policy(db, policy)
    audit.log_action(db, current_user.id, "Suppression policy", f"Policy '{policy.name}' supprimée")
    return response.success_response(None, "Policy supprimée")

# Gestion des relations : users, groups, tags

@router.post("/{policy_id}/users/{user_id}", response_model=dict)
def add_user(policy_id: int, user_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    policy = policy_repo.get_policy(db, policy_id)
    user = user_repo.get_user(db, user_id)
    if not policy or not user:
        raise HTTPException(status_code=404, detail="Policy ou user non trouvé")
    if not permissions.has_permission(db, current_user, policy.organization_id, "policy:update"):
        raise HTTPException(status_code=403, detail="Permission insuffisante")
    policy_repo.add_user(db, policy, user)
    return response.success_response(None, "Utilisateur ajouté à la policy")

@router.delete("/{policy_id}/users/{user_id}", response_model=dict)
def remove_user(policy_id: int, user_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    policy = policy_repo.get_policy(db, policy_id)
    user = user_repo.get_user(db, user_id)
    if not policy or not user:
        raise HTTPException(status_code=404, detail="Policy ou user non trouvé")
    if not permissions.has_permission(db, current_user, policy.organization_id, "policy:update"):
        raise HTTPException(status_code=403, detail="Permission insuffisante")
    policy_repo.remove_user(db, policy, user)
    return response.success_response(None, "Utilisateur retiré de la policy")

@router.post("/{policy_id}/groups/{group_id}", response_model=dict)
def add_group(policy_id: int, group_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    policy = policy_repo.get_policy(db, policy_id)
    group = group_repo.get_group(db, group_id)
    if not policy or not group:
        raise HTTPException(status_code=404, detail="Policy ou groupe non trouvé")
    if not permissions.has_permission(db, current_user, policy.organization_id, "policy:update"):
        raise HTTPException(status_code=403, detail="Permission insuffisante")
    policy_repo.add_group(db, policy, group)
    return response.success_response(None, "Groupe ajouté à la policy")

@router.delete("/{policy_id}/groups/{group_id}", response_model=dict)
def remove_group(policy_id: int, group_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    policy = policy_repo.get_policy(db, policy_id)
    group = group_repo.get_group(db, group_id)
    if not policy or not group:
        raise HTTPException(status_code=404, detail="Policy ou groupe non trouvé")
    if not permissions.has_permission(db, current_user, policy.organization_id, "policy:update"):
        raise HTTPException(status_code=403, detail="Permission insuffisante")
    policy_repo.remove_group(db, policy, group)
    return response.success_response(None, "Groupe retiré de la policy")

@router.post("/{policy_id}/tags/{tag_id}", response_model=dict)
def add_tag(policy_id: int, tag_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    policy = policy_repo.get_policy(db, policy_id)
    tag = tag_repo.get_tag(db, tag_id)
    if not policy or not tag:
        raise HTTPException(status_code=404, detail="Policy ou tag non trouvé")
    if not permissions.has_permission(db, current_user, policy.organization_id, "policy:update"):
        raise HTTPException(status_code=403, detail="Permission insuffisante")
    policy_repo.add_tag(db, policy, tag)
    return response.success_response(None, "Tag ajouté à la policy")

@router.delete("/{policy_id}/tags/{tag_id}", response_model=dict)
def remove_tag(policy_id: int, tag_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    policy = policy_repo.get_policy(db, policy_id)
    tag = tag_repo.get_tag(db, tag_id)
    if not policy or not tag:
        raise HTTPException(status_code=404, detail="Policy ou tag non trouvé")
    if not permissions.has_permission(db, current_user, policy.organization_id, "policy:update"):
        raise HTTPException(status_code=403, detail="Permission insuffisante")
    policy_repo.remove_tag(db, policy, tag)
    return response.success_response(None, "Tag retiré de la policy")
