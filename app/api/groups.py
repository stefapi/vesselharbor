# app/api/groups.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from ..schema.group import GroupCreate, GroupUpdate, GroupOut
from ..schema.auth import BaseResponse, EmptyData
from ..models.group import Group
from ..models.user import User
from ..models.policy import Policy
from ..models.tag import Tag
from ..database.session import SessionLocal
from ..repositories import group_repo, user_repo, policy_repo, tag_repo
from ..api.users import get_current_user
from ..helper import permissions, audit, response
from ..schema.policy import PolicyOut
from ..schema.tag import TagOut
from ..schema.user import UserOut

router = APIRouter(prefix="/groups", tags=["groups"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("", response_model=BaseResponse[List[GroupOut]], summary="List all groups", description="Retrieves the complete list of all groups in the system (reserved for superadmins)", responses={
    200: {"description": "List of all groups retrieved successfully"},
    401: {"description": "Not authenticated"},
    403: {"description": "Insufficient permissions - reserved for superadmins"}
})
def list_all_groups(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not current_user.is_superadmin:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    groups = db.query(Group).all()
    return response.success_response([GroupOut.model_validate(group) for group in groups], "All groups retrieved")

@router.get("/{group_id}", response_model=BaseResponse[GroupOut], summary="Group details", description="Retrieves details of a specific group by its ID", responses={
    200: {"description": "Group retrieved successfully"},
    401: {"description": "Not authenticated"},
    403: {"description": "Insufficient permissions"},
    404: {"description": "Group not found"}
})
def get_group(group_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    group = group_repo.get_group(db, group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    if not permissions.has_permission(db, current_user, group.organization_id, "group:read"):
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    return response.success_response(GroupOut.model_validate(group), "Group retrieved")

@router.post("/{organization_id}", response_model=BaseResponse[GroupOut], summary="Create group", description="Creates a new group in the specified organization", responses={
    200: {"description": "Group created successfully"},
    401: {"description": "Not authenticated"},
    403: {"description": "Insufficient permissions"}
})
def create_group(organization_id: int, group_in: GroupCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not permissions.has_permission(db, current_user, organization_id, "group:create"):
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    group = group_repo.create_group(db, organization_id=organization_id, name=group_in.name, description=group_in.description)
    audit.log_action(db, current_user.id, "Group creation", f"Created group '{group.name}'")
    return response.success_response(GroupOut.model_validate(group), "Group created")

@router.put("/{group_id}", response_model=BaseResponse[GroupOut], summary="Update group", description="Updates information for an existing group", responses={
    200: {"description": "Group updated successfully"},
    401: {"description": "Not authenticated"},
    403: {"description": "Insufficient permissions"},
    404: {"description": "Group not found"}
})
def update_group(group_id: int, group_in: GroupUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    group = group_repo.get_group(db, group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    if not permissions.has_permission(db, current_user, group.organization_id, "group:update"):
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    group = group_repo.update_group(db, group, name=group_in.name, description=group_in.description)
    audit.log_action(db, current_user.id, "Group update", f"Updated group '{group.name}'")
    return response.success_response(GroupOut.model_validate(group), "Group updated")

@router.delete("/{group_id}", response_model=BaseResponse[EmptyData], summary="Delete group", description="Deletes an existing group and all its associations", responses={
    200: {"description": "Group deleted successfully"},
    401: {"description": "Not authenticated"},
    403: {"description": "Insufficient permissions or only superadmin can delete 'admin' and 'editors' groups"},
    404: {"description": "Group not found"}
})
def delete_group(group_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    group = group_repo.get_group(db, group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    if not permissions.has_permission(db, current_user, group.organization_id, "group:delete"):
        raise HTTPException(status_code=403, detail="Insufficient permissions")

    # Prevent non-superadmin users from deleting 'admin' and 'editors' groups
    if not current_user.is_superadmin and group.name in ["admin", "editors"]:
        raise HTTPException(
            status_code=403,
            detail="Only a superadmin can delete 'admin' and 'editors' groups"
        )

    group_repo.delete_group(db, group)
    audit.log_action(db, current_user.id, "Group deletion", f"Group '{group.name}' deleted")
    return response.success_response(EmptyData(), "Group deleted")


@router.get("/organization/{org_id}", response_model=BaseResponse[List[GroupOut]], summary="List organization groups", description="Retrieves all groups belonging to a specific organization", responses={
    200: {"description": "Organization group list retrieved successfully"},
    401: {"description": "Not authenticated"},
    403: {"description": "Insufficient permissions"}
})
def list_groups_by_org(org_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not permissions.has_permission(db, current_user, org_id, "group:read"):
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    groups = db.query(Group).filter(Group.organization_id == org_id).all()
    return response.success_response([GroupOut.model_validate(group) for group in groups], "Groups retrieved")

@router.get("/{group_id}/users", response_model=BaseResponse[List[UserOut]], summary="List group users", description="Retrieves all users belonging to a specific group", responses={
    200: {"description": "Group user list retrieved successfully"},
    401: {"description": "Not authenticated"},
    403: {"description": "Insufficient permissions"},
    404: {"description": "Group not found"}
})
def list_group_users(group_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    group = group_repo.get_group(db, group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    if not permissions.has_permission(db, current_user, group.organization_id, "group:read"):
        raise HTTPException(status_code=403, detail="Insufficient permissions")

    # Convert User objects to UserOut objects for proper serialization
    serializable_users = [UserOut.model_validate(user) for user in group.users]
    return response.success_response(serializable_users, "Group users retrieved")

@router.post("/{group_id}/users/{user_id}", response_model=BaseResponse[GroupOut], summary="Assign user", description="Adds a specific user to a group", responses={
    200: {"description": "User added to group successfully or already in group"},
    401: {"description": "Not authenticated"},
    403: {"description": "Insufficient permissions"},
    404: {"description": "Group or user not found"}
})
def assign_user(group_id: int, user_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    group = group_repo.get_group(db, group_id)
    user = user_repo.get_user(db, user_id)
    if not group or not user:
        raise HTTPException(status_code=404, detail="Group or user not found")
    if not permissions.has_permission(db, current_user, group.organization_id, "group:assign_user"):
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    # Check if user is already in the group
    if user in group.users:
        return response.success_response(GroupOut.model_validate(group), "User already in this group")

    group.users.append(user)
    db.commit()
    audit.log_action(db, current_user.id, "Add to group", f"User {user.email} added to group {group.name}")

    return response.success_response(GroupOut.model_validate(group), "User added to group")

@router.delete("/{group_id}/users/{user_id}", response_model=BaseResponse[GroupOut], summary="Remove user", description="Removes a specific user from a group", responses={
    200: {"description": "User removed from group successfully or was not in group"},
    401: {"description": "Not authenticated"},
    403: {"description": "Insufficient permissions"},
    404: {"description": "Group or user not found"}
})
def remove_user(group_id: int, user_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    group = group_repo.get_group(db, group_id)
    user = user_repo.get_user(db, user_id)
    if not group or not user:
        raise HTTPException(status_code=404, detail="Group or user not found")
    if not permissions.has_permission(db, current_user, group.organization_id, "group:assign_user"):
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    # Check if user is in the group
    if user not in group.users:
        return response.success_response(GroupOut.model_validate(group), "User not in this group")

    group.users.remove(user)
    db.commit()
    return response.success_response(GroupOut.model_validate(group), "User removed from group")

@router.get("/{group_id}/policy", response_model=BaseResponse[List[PolicyOut]], summary="List group policies", description="Retrieves all policies associated with a specific group", responses={
    200: {"description": "Group policy list retrieved successfully"},
    401: {"description": "Not authenticated"},
    403: {"description": "Insufficient permissions"},
    404: {"description": "Group not found"}
})
def list_group_policies(group_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    group = group_repo.get_group(db, group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    if not permissions.has_permission(db, current_user, group.organization_id, "group:read"):
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    # Convert Policy objects to PolicyOut objects for proper serialization
    serializable_policies = [PolicyOut.model_validate(policy) for policy in group.policies]
    return response.success_response(serializable_policies, "Group policies retrieved")

@router.post("/{group_id}/policy", response_model=BaseResponse[GroupOut], summary="Assign policy", description="Associates a specific policy with a group", responses={
    200: {"description": "Policy associated with group successfully"},
    401: {"description": "Not authenticated"},
    403: {"description": "Insufficient permissions"},
    404: {"description": "Group or policy not found"}
})
def assign_policy(group_id: int, policy_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    group = group_repo.get_group(db, group_id)
    policy = policy_repo.get_policy(db, policy_id)
    if not group or not policy:
        raise HTTPException(status_code=404, detail="Group or policy not found")
    if not permissions.has_permission(db, current_user, group.organization_id, "group:assign_policy"):
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    group.policies.append(policy)
    db.commit()
    return response.success_response(GroupOut.model_validate(group), "Policy associated with group")

@router.delete("/{group_id}/policy/{policy_id}", response_model=BaseResponse[GroupOut], summary="Remove policy", description="Removes a specific policy from a group", responses={
    200: {"description": "Policy removed from group successfully"},
    401: {"description": "Not authenticated"},
    403: {"description": "Insufficient permissions"},
    404: {"description": "Group or policy not found"}
})
def remove_policy(group_id: int, policy_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    group = group_repo.get_group(db, group_id)
    policy = policy_repo.get_policy(db, policy_id)
    if not group or not policy:
        raise HTTPException(status_code=404, detail="Group or policy not found")
    if not permissions.has_permission(db, current_user, group.organization_id, "group:assign_policy"):
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    if policy in group.policies:
        group.policies.remove(policy)
        db.commit()
    return response.success_response(GroupOut.model_validate(group), "Policy removed from group")

@router.get("/{group_id}/tags", response_model=BaseResponse[List[TagOut]], summary="List group tags", description="Retrieves all tags associated with a specific group", responses={
    200: {"description": "Group tag list retrieved successfully"},
    401: {"description": "Not authenticated"},
    403: {"description": "Insufficient permissions"},
    404: {"description": "Group not found"}
})
def list_group_tags(group_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    group = group_repo.get_group(db, group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    if not permissions.has_permission(db, current_user, group.organization_id, "group:read"):
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    # Convert Tag objects to TagOut objects for proper serialization
    serializable_tags = [TagOut.model_validate(tag) for tag in group.tags]
    return response.success_response(serializable_tags, "Group tags retrieved")

@router.post("/{group_id}/tags/{tag_id}", response_model=BaseResponse[GroupOut], summary="Add tag to group", description="Associates a specific tag with a group", responses={
    200: {"description": "Tag added to group successfully"},
    401: {"description": "Not authenticated"},
    403: {"description": "Insufficient permissions"},
    404: {"description": "Group or tag not found"}
})
def add_tag_to_group(group_id: int, tag_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    group = group_repo.get_group(db, group_id)
    tag = tag_repo.get_tag(db, tag_id)
    if not group or not tag:
        raise HTTPException(status_code=404, detail="Group or tag not found")
    if not permissions.has_permission(db, current_user, group.organization_id, "group:assign_tag"):
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    group.tags.append(tag)
    db.commit()
    return response.success_response(GroupOut.model_validate(group), "Tag added to group")

@router.delete("/{group_id}/tags/{tag_id}", response_model=BaseResponse[GroupOut], summary="Remove tag from group", description="Removes a specific tag from a group", responses={
    200: {"description": "Tag removed from group successfully"},
    401: {"description": "Not authenticated"},
    403: {"description": "Insufficient permissions"},
    404: {"description": "Group or tag not found"}
})
def remove_tag_from_group(group_id: int, tag_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    group = group_repo.get_group(db, group_id)
    tag = tag_repo.get_tag(db, tag_id)
    if not group or not tag:
        raise HTTPException(status_code=404, detail="Group or tag not found")
    if not permissions.has_permission(db, current_user, group.organization_id, "group:assign_tag"):
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    if tag in group.tags:
        group.tags.remove(tag)
        db.commit()
    return response.success_response(GroupOut.model_validate(group), "Tag removed from group")
