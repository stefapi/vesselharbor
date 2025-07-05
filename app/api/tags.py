# app/api/tags.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..models.user import User
from ..models.element import Element
from ..models.environment import Environment
from ..database.session import SessionLocal
from ..repositories import tag_repo
from ..api.users import get_current_user
from ..helper import permissions, audit, response
from ..schema.tag import TagOut, TagCreate
from ..schema.auth import BaseResponse, EmptyData
from ..schema.user import UserOut
from ..schema.group import GroupOut
from ..schema.policy import PolicyOut
from ..schema.element import ElementOut
from ..schema.environment import EnvironmentOut

router = APIRouter(prefix="/tags", tags=["tags"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get(
    "",
    response_model=BaseResponse[List[TagOut]],
    summary="List all tags",
    description="Returns the list of all tags if the user has permissions on their organization.",
    responses={
        200: {"description": "Tag list retrieved successfully"},
        401: {"description": "Not authenticated"},
        403: {"description": "Insufficient permissions"},
    }
)
def list_tags(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    all_tags = tag_repo.list_tags(db)
    accessible_tags = []

    for tag in all_tags:
        # Check permissions through policies
        if tag.policies and permissions.has_permission(db, current_user, tag.policies[0].organization_id, "tag:read"):
            accessible_tags.append(tag)
            continue

        # Check permissions through groups
        if tag.groups and permissions.has_permission(db, current_user, tag.groups[0].organization_id, "tag:read"):
            accessible_tags.append(tag)
            continue

        # Check permissions through users
        if tag.users and tag.users[0].organizations and permissions.has_permission(db, current_user, tag.users[0].organizations[0].id, "tag:read"):
            accessible_tags.append(tag)
            continue

        # Check permissions through elements
        if tag.elements and tag.elements[0].environment and permissions.has_permission(db, current_user, tag.elements[0].environment.organization_id, "tag:read"):
            accessible_tags.append(tag)
            continue

        # Check permissions through environments
        if tag.environments and permissions.has_permission(db, current_user, tag.environments[0].organization_id, "tag:read"):
            accessible_tags.append(tag)
            continue

    return response.success_response(accessible_tags, "Accessible tag list retrieved")

@router.get(
    "/{tag_id}",
    response_model=BaseResponse[TagOut],
    summary="Get a tag",
    description="Returns information for a specific tag if the user has required permissions.",
    responses={
        200: {"description": "Tag retrieved successfully"},
        401: {"description": "Not authenticated"},
        403: {"description": "Insufficient permissions"},
        404: {"description": "Tag not found"},
    }
)
def get_tag(tag_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    tag = tag_repo.get_tag(db, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")

    # Check permissions through various relationships
    org_id = None
    if tag.policies:
        org_id = tag.policies[0].organization_id
    elif tag.groups:
        org_id = tag.groups[0].organization_id
    elif tag.users and tag.users[0].organizations:
        org_id = tag.users[0].organizations[0].id
    elif tag.elements and tag.elements[0].environment:
        org_id = tag.elements[0].environment.organization_id
    elif tag.environments:
        org_id = tag.environments[0].organization_id

    if not org_id or not permissions.has_permission(db, current_user, org_id, "tag:read"):
        raise HTTPException(status_code=403, detail="Insufficient permissions to read this tag")

    return response.success_response(TagOut.model_validate(tag), "Tag retrieved successfully")

@router.post(
    "",
    response_model=BaseResponse[TagOut],
    summary="Create a tag",
    description="Creates a new tag. The user must have permissions on a specific organization.",
    responses={
        200: {"description": "Tag created successfully"},
        400: {"description": "Tag already exists"},
        401: {"description": "Not authenticated"},
        403: {"description": "Insufficient permissions"},
    }
)
def create_tag(
    tag_in: TagCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not permissions.has_permission(db, current_user, tag_in.organization_id, "tag:create"):
        raise HTTPException(status_code=403, detail="Insufficient permissions to create a tag in this organization")

    existing = tag_repo.get_tag_by_value(db, tag_in.value)
    if existing:
        raise HTTPException(status_code=400, detail="This tag already exists.")

    tag = tag_repo.create_tag(db, value=tag_in.value)
    audit.log_action(db, current_user.id, "Tag creation", f"Tag '{tag.value}' created for organization {tag_in.organization_id}")
    return response.success_response(tag, "Tag created successfully")

@router.delete(
    "/{tag_id}",
    response_model=BaseResponse[EmptyData],
    summary="Delete a tag",
    description="Deletes a tag if authorized.",
    responses={
        200: {"description": "Tag deleted successfully"},
        401: {"description": "Not authenticated"},
        403: {"description": "Insufficient permissions"},
        404: {"description": "Tag not found"},
    }
)
def delete_tag(tag_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    tag = tag_repo.get_tag(db, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")

    # Find the organization linked to the tag via policy, group, user, element or environment
    org_id = None
    if tag.policies:
        org_id = tag.policies[0].organization_id
    elif tag.groups:
        org_id = tag.groups[0].organization_id
    elif tag.users and tag.users[0].organizations:
        org_id = tag.users[0].organizations[0].id
    elif tag.elements and tag.elements[0].environment:
        org_id = tag.elements[0].environment.organization_id
    elif tag.environments:
        org_id = tag.environments[0].organization_id

    if not org_id or not permissions.has_permission(db, current_user, org_id, "tag:delete"):
        raise HTTPException(status_code=403, detail="Insufficient permissions to delete this tag")

    audit.log_action(db, current_user.id, "Tag deletion", f"Tag '{tag.value}' deleted (id={tag.id})")
    tag_repo.delete_tag(db, tag)
    return response.success_response(None, "Tag deleted successfully")

@router.get(
    "/{tag_id}/groups",
    response_model=BaseResponse[List[GroupOut]],
    summary="Groups linked to a tag",
    description="Returns groups associated with a tag.",
    responses={
        200: {"description": "Groups retrieved successfully"},
        401: {"description": "Not authenticated"},
        403: {"description": "Insufficient permissions"},
        404: {"description": "Tag not found"},
    }
)
def get_tag_groups(tag_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    tag = tag_repo.get_tag(db, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    org_id = tag.groups[0].organization_id if tag.groups else None
    if not org_id or not permissions.has_permission(db, current_user, org_id, "tag:read"):
        raise HTTPException(status_code=403, detail="Insufficient permissions to read this tag")
    return response.success_response(tag.groups, "Groups retrieved")

@router.get(
    "/{tag_id}/users",
    response_model=BaseResponse[List[UserOut]],
    summary="Users linked to a tag",
    description="Returns users associated with a tag.",
    responses={
        200: {"description": "Users retrieved successfully"},
        401: {"description": "Not authenticated"},
        403: {"description": "Insufficient permissions"},
        404: {"description": "Tag not found"},
    }
)
def get_tag_users(tag_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    tag = tag_repo.get_tag(db, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    org_id = tag.users[0].organizations[0].id if tag.users and tag.users[0].organizations else None
    if not org_id or not permissions.has_permission(db, current_user, org_id, "tag:read"):
        raise HTTPException(status_code=403, detail="Insufficient permissions to read this tag")
    return response.success_response(tag.users, "Users retrieved")

@router.get(
    "/{tag_id}/policies",
    response_model=BaseResponse[List[PolicyOut]],
    summary="Policies linked to a tag",
    description="Returns policies associated with a tag.",
    responses={
        200: {"description": "Policies retrieved successfully"},
        401: {"description": "Not authenticated"},
        403: {"description": "Insufficient permissions"},
        404: {"description": "Tag not found"},
    }
)
def get_tag_policies(tag_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    tag = tag_repo.get_tag(db, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    org_id = tag.policies[0].organization_id if tag.policies else None
    if not org_id or not permissions.has_permission(db, current_user, org_id, "tag:read"):
        raise HTTPException(status_code=403, detail="Insufficient permissions to read this tag")
    return response.success_response(tag.policies, "Policies retrieved")

@router.get(
    "/{tag_id}/elements",
    response_model=BaseResponse[List[ElementOut]],
    summary="Elements linked to a tag",
    description="Returns elements associated with a tag.",
    responses={
        200: {"description": "Elements retrieved successfully"},
        401: {"description": "Not authenticated"},
        403: {"description": "Insufficient permissions"},
        404: {"description": "Tag not found"},
    }
)
def get_tag_elements(tag_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    tag = tag_repo.get_tag(db, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")

    # Check if the tag has elements
    if not tag.elements:
        return response.success_response([], "No elements associated with this tag")

    # Check permissions on the environment organization of the first element
    org_id = tag.elements[0].environment.organization_id if tag.elements and tag.elements[0].environment else None
    if not org_id or not permissions.has_permission(db, current_user, org_id, "tag:read"):
        raise HTTPException(status_code=403, detail="Insufficient permissions to read this tag")

    return response.success_response(tag.elements, "Elements retrieved")

@router.get(
    "/{tag_id}/environments",
    response_model=BaseResponse[List[EnvironmentOut]],
    summary="Environments linked to a tag",
    description="Returns environments associated with a tag.",
    responses={
        200: {"description": "Environments retrieved successfully"},
        401: {"description": "Not authenticated"},
        403: {"description": "Insufficient permissions"},
        404: {"description": "Tag not found"},
    }
)
def get_tag_environments(tag_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    tag = tag_repo.get_tag(db, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")

    # Check if the tag has environments
    if not tag.environments:
        return response.success_response([], "No environments associated with this tag")

    # Check permissions on the organization of the first environment
    org_id = tag.environments[0].organization_id if tag.environments else None
    if not org_id or not permissions.has_permission(db, current_user, org_id, "tag:read"):
        raise HTTPException(status_code=403, detail="Insufficient permissions to read this tag")

    return response.success_response(tag.environments, "Environments retrieved")
