from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List

from ..database.session import SessionLocal
from ..models.user import User
from ..repositories import policy_repo, user_repo, group_repo, tag_repo, rule_repo
from ..schema.policy import PolicyCreate, PolicyUpdate, PolicyOut
from ..schema.user import UserOut
from ..schema.group import GroupOut
from ..schema.rule import RuleOut
from ..schema.auth import BaseResponse, EmptyData
from ..api.users import get_current_user
from ..helper import permissions, audit, response

router = APIRouter(prefix="/policies", tags=["policies"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("", response_model=BaseResponse[List[PolicyOut]],
    summary="List policies",
    description="Retrieves the list of policies for a given organization with pagination.",
    responses={
    200: {"description": "Policies retrieved successfully"},
    401: {"description": "Unauthenticated"},
    403: {"description": "Insufficient permissions"}
})
def list_policies(
    organization_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not permissions.has_permission(db, current_user, organization_id, "policy:read"):
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    policies = policy_repo.list_policies(db, organization_id, skip, limit)
    return response.success_response(policies, "Policies retrieved")

@router.get("/{policy_id}", response_model=BaseResponse[PolicyOut],
    summary="Get policy",
    description="Retrieves details of a specific policy by its ID.",
    responses={
    200: {"description": "Policy retrieved successfully"},
    401: {"description": "Unauthenticated"},
    403: {"description": "Insufficient permissions"},
    404: {"description": "Policy not found"}
})
def get_policy(policy_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    policy = policy_repo.get_policy(db, policy_id)
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")
    if not permissions.has_permission(db, current_user, policy.organization_id, "policy:read"):
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    return response.success_response(policy, "Policy retrieved")

@router.post("", response_model=BaseResponse[PolicyOut],
    summary="Create policy",
    description="Creates a new policy in the specified organization.",
    responses={
    200: {"description": "Policy created successfully"},
    401: {"description": "Unauthenticated"},
    403: {"description": "Insufficient permissions"}
})
def create_policy(policy_in: PolicyCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not permissions.has_permission(db, current_user, policy_in.organization_id, "policy:create"):
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    policy = policy_repo.create_policy(db, policy_in)
    audit.log_action(db, current_user.id, "Policy creation", f"Policy '{policy.name}' created")
    return response.success_response(policy, "Policy created")

@router.put("/{policy_id}", response_model=BaseResponse[PolicyOut],
    summary="Update policy",
    description="Modifies information of an existing policy.",
    responses={
    200: {"description": "Policy updated successfully"},
    401: {"description": "Unauthenticated"},
    403: {"description": "Insufficient permissions"},
    404: {"description": "Policy not found"}
})
def update_policy(policy_id: int, policy_in: PolicyUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    policy = policy_repo.get_policy(db, policy_id)
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")
    if not permissions.has_permission(db, current_user, policy.organization_id, "policy:update"):
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    policy = policy_repo.update_policy(db, policy, policy_in)
    audit.log_action(db, current_user.id, "Policy update", f"Policy '{policy.name}' updated")
    return response.success_response(policy, "Policy updated")

@router.delete("/{policy_id}", response_model=BaseResponse[EmptyData],
    summary="Delete policy",
    description="Permanently deletes an existing policy.",
    responses={
    200: {"description": "Policy deleted successfully"},
    401: {"description": "Unauthenticated"},
    403: {"description": "Insufficient permissions"},
    404: {"description": "Policy not found"}
})
def delete_policy(policy_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    policy = policy_repo.get_policy(db, policy_id)
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")
    if not permissions.has_permission(db, current_user, policy.organization_id, "policy:delete"):
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    policy_repo.delete_policy(db, policy)
    audit.log_action(db, current_user.id, "Policy deletion", f"Policy '{policy.name}' deleted")
    return response.success_response(None, "Policy deleted")

# Relationship management: users, groups, tags

@router.get("/{policy_id}/users", response_model=BaseResponse[List[UserOut]],
    summary="List policy users",
    description="Retrieves all users associated with a specific policy.",
    responses={
    200: {"description": "Policy users retrieved successfully"},
    401: {"description": "Unauthenticated"},
    403: {"description": "Insufficient permissions"},
    404: {"description": "Policy not found"}
})
def list_policy_users(policy_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    policy = policy_repo.get_policy(db, policy_id)
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")
    if not permissions.has_permission(db, current_user, policy.organization_id, "policy:read"):
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    return response.success_response(policy.users, "Policy users retrieved")

@router.post("/{policy_id}/users/{user_id}", response_model=BaseResponse[EmptyData],
    summary="Add user to policy",
    description="Associates a specific user with a policy to grant defined permissions.",
    responses={
    200: {"description": "User added to policy successfully"},
    401: {"description": "Unauthenticated"},
    403: {"description": "Insufficient permissions"},
    404: {"description": "Policy or user not found"}
})
def add_user(policy_id: int, user_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    policy = policy_repo.get_policy(db, policy_id)
    user = user_repo.get_user(db, user_id)
    if not policy or not user:
        raise HTTPException(status_code=404, detail="Policy or user not found")
    if not permissions.has_permission(db, current_user, policy.organization_id, "policy:update"):
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    policy_repo.add_user(db, policy, user)
    return response.success_response(None, "User added to policy")

@router.delete("/{policy_id}/users/{user_id}", response_model=BaseResponse[EmptyData],
    summary="Remove user from policy",
    description="Disassociates a user from a policy, revoking associated permissions.",
    responses={
    200: {"description": "User removed from policy successfully"},
    401: {"description": "Unauthenticated"},
    403: {"description": "Insufficient permissions"},
    404: {"description": "Policy or user not found"}
})
def remove_user(policy_id: int, user_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    policy = policy_repo.get_policy(db, policy_id)
    user = user_repo.get_user(db, user_id)
    if not policy or not user:
        raise HTTPException(status_code=404, detail="Policy or user not found")
    if not permissions.has_permission(db, current_user, policy.organization_id, "policy:update"):
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    policy_repo.remove_user(db, policy, user)
    return response.success_response(None, "User removed from policy")

@router.get("/{policy_id}/groups", response_model=BaseResponse[List[GroupOut]],
    summary="List policy groups",
    description="Retrieves all groups associated with a specific policy.",
    responses={
    200: {"description": "Policy groups retrieved successfully"},
    401: {"description": "Unauthenticated"},
    403: {"description": "Insufficient permissions"},
    404: {"description": "Policy not found"}
})
def list_policy_groups(policy_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    policy = policy_repo.get_policy(db, policy_id)
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")
    if not permissions.has_permission(db, current_user, policy.organization_id, "policy:read"):
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    return response.success_response(policy.groups, "Policy groups retrieved")

@router.post("/{policy_id}/groups/{group_id}", response_model=BaseResponse[EmptyData],
    summary="Add group to policy",
    description="Associates a group with a policy, granting defined permissions to all group members.",
    responses={
    200: {"description": "Group added to policy successfully"},
    401: {"description": "Unauthenticated"},
    403: {"description": "Insufficient permissions"},
    404: {"description": "Policy or group not found"}
})
def add_group(policy_id: int, group_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    policy = policy_repo.get_policy(db, policy_id)
    group = group_repo.get_group(db, group_id)
    if not policy or not group:
        raise HTTPException(status_code=404, detail="Policy or group not found")
    if not permissions.has_permission(db, current_user, policy.organization_id, "policy:update"):
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    policy_repo.add_group(db, policy, group)
    return response.success_response(None, "Group added to policy")

@router.get("/{policy_id}/rules", response_model=BaseResponse[List[RuleOut]],
    summary="List policy rules",
    description="Retrieves all rules associated with a specific policy",
    responses={
    200: {"description": "Rules retrieved successfully"},
    401: {"description": "Unauthenticated"},
    403: {"description": "Insufficient permissions"},
    404: {"description": "Policy not found"}
})
def list_rules(policy_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    policy = policy_repo.get_policy(db, policy_id)
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")
    if not permissions.has_permission(db, current_user, policy.organization_id, "rule:read"):
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    rules = rule_repo.list_rules_for_policy(db, policy_id)
    return response.success_response(rules, "Rules retrieved")

@router.delete("/{policy_id}/groups/{group_id}", response_model=BaseResponse[EmptyData],
    summary="Remove group from policy",
    description="Disassociates a group from a policy, revoking associated permissions from all group members.",
    responses={
    200: {"description": "Group removed from policy successfully"},
    401: {"description": "Unauthenticated"},
    403: {"description": "Insufficient permissions"},
    404: {"description": "Policy or group not found"}
})
def remove_group(policy_id: int, group_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    policy = policy_repo.get_policy(db, policy_id)
    group = group_repo.get_group(db, group_id)
    if not policy or not group:
        raise HTTPException(status_code=404, detail="Policy or group not found")
    if not permissions.has_permission(db, current_user, policy.organization_id, "policy:update"):
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    policy_repo.remove_group(db, policy, group)
    return response.success_response(None, "Group removed from policy")

@router.post("/{policy_id}/tags/{tag_id}", response_model=BaseResponse[EmptyData],
    summary="Add tag to policy",
    description="Associates a tag with a policy, applying the policy to all resources with this tag.",
    responses={
    200: {"description": "Tag added to policy successfully"},
    401: {"description": "Unauthenticated"},
    403: {"description": "Insufficient permissions"},
    404: {"description": "Policy or tag not found"}
})
def add_tag(policy_id: int, tag_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    policy = policy_repo.get_policy(db, policy_id)
    tag = tag_repo.get_tag(db, tag_id)
    if not policy or not tag:
        raise HTTPException(status_code=404, detail="Policy or tag not found")
    if not permissions.has_permission(db, current_user, policy.organization_id, "policy:update"):
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    policy_repo.add_tag(db, policy, tag)
    return response.success_response(None, "Tag added to policy")

@router.delete("/{policy_id}/tags/{tag_id}", response_model=BaseResponse[EmptyData],
    summary="Remove tag from policy",
    description="Disassociates a tag from a policy, removing policy application from resources with this tag.",
    responses={
    200: {"description": "Tag removed from policy successfully"},
    401: {"description": "Unauthenticated"},
    403: {"description": "Insufficient permissions"},
    404: {"description": "Policy or tag not found"}
})
def remove_tag(policy_id: int, tag_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    policy = policy_repo.get_policy(db, policy_id)
    tag = tag_repo.get_tag(db, tag_id)
    if not policy or not tag:
        raise HTTPException(status_code=404, detail="Policy or tag not found")
    if not permissions.has_permission(db, current_user, policy.organization_id, "policy:update"):
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    policy_repo.remove_tag(db, policy, tag)
    return response.success_response(None, "Tag removed from policy")
