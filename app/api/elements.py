from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, List

from ..schema.element import ElementCreate, ElementUpdate, ElementOut
from ..schema.tag import TagOut
from ..schema.auth import BaseResponse, EmptyData
from ..models.element import Element
from ..models.environment import Environment
from ..models.user import User
from ..database.session import SessionLocal
from ..repositories import element_repo, tag_repo, physical_host_repo
from ..api.users import get_current_user
from ..helper import permissions, audit, response
from ..helper.animalname import generate_codename
from ..schema.physical_host import PhysicalHostOut

router = APIRouter(prefix="/elements", tags=["elements"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# TODO Check toutes les permissions dans les API endpoints, ajouter les manquantes dans le seed

# TODO bien détailler toutes les documentations dont les responses

@router.post(
    "/{environment_id}",
    response_model=BaseResponse[ElementOut],
    summary="Create an element",
    description="Creates an element in a given environment.",
    responses={
        200: {"description": "Element created successfully"},
        401: {"description": "Not authenticated"},
        403: {"description": "Insufficient permission"},
        404: {"description": "Environment not found"},
    }
)
def create_element(
    environment_id: int,
    element_in: ElementCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    env = db.query(Environment).filter_by(id=environment_id).first()
    if not env:
        raise HTTPException(status_code=404, detail="Environment not found")

    # Generate a codename if no name is provided or if name is empty
    if not element_in.name or element_in.name.strip() == "":
        element_in.name = generate_codename()

    # Check if an element with the same name already exists
    existing_elem = db.query(Element).filter(Element.name == element_in.name).first()
    if existing_elem:
        raise HTTPException(status_code=400, detail="An element with this name already exists")

    if not permissions.has_permission(db, current_user, env.organization_id, "element:create"):
        raise HTTPException(status_code=403, detail="Insufficient permission to create an element")

    try:
        # Create the element with a sub-component
        element = element_repo.create_element_with_subcomponent(
            db,
            environment_id,
            element_in.name,
            element_in.description,
            element_in.subcomponent_type,
            element_in.subcomponent_data
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    # Get physical hosts associated with the element's environment
    physical_hosts = physical_host_repo.list_physical_hosts_by_environment(db, environment_id)

    # Create a serializable element with environment_physical_hosts
    serializable_element = ElementOut.model_validate(element)
    serializable_element.environment_physical_hosts = [PhysicalHostOut.model_validate(host) for host in physical_hosts]

    audit.log_action(db, current_user.id, "Element creation", f"Element '{element.name}' in env {environment_id}")
    return response.success_response(serializable_element, "Element created successfully")


@router.get(
    "/{element_id}",
    response_model=BaseResponse[ElementOut],
    summary="Get an element",
    description="Returns information about a specific element.",
    responses={
        200: {"description": "Element retrieved successfully"},
        401: {"description": "Not authenticated"},
        403: {"description": "Insufficient permission"},
        404: {"description": "Element not found"},
    }
)
def get_element(
    element_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    element = element_repo.get_element(db, element_id)
    if not element:
        raise HTTPException(status_code=404, detail="Element not found")

    org_id = element.environment.organization_id
    if not permissions.has_permission(db, current_user, org_id, "element:read"):
        raise HTTPException(status_code=403, detail="Insufficient permission to view this element")

    # Get physical hosts associated with the element's environment
    physical_hosts = physical_host_repo.list_physical_hosts_by_environment(db, element.environment_id)

    # Create a serializable element with environment_physical_hosts
    serializable_element = ElementOut.model_validate(element)
    serializable_element.environment_physical_hosts = [PhysicalHostOut.model_validate(host) for host in physical_hosts]

    return response.success_response(serializable_element, "Element retrieved")


@router.put(
    "/{element_id}",
    response_model=BaseResponse[ElementOut],
    summary="Update an element",
    description="Modifies the information of an element.",
    responses={
        200: {"description": "Element updated successfully"},
        401: {"description": "Not authenticated"},
        403: {"description": "Insufficient permission"},
        404: {"description": "Element not found"},
    }
)
def update_element(
    element_id: int,
    element_in: ElementUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    element = element_repo.get_element(db, element_id)
    if not element:
        raise HTTPException(status_code=404, detail="Element not found")

    org_id = element.environment.organization_id
    if not permissions.has_permission(db, current_user, org_id, "element:update"):
        raise HTTPException(status_code=403, detail="Insufficient permission to modify this element")

    original_env_id = element.environment_id

    # If environment_id is provided and different from current, check permissions for the new environment
    if element_in.environment_id is not None and original_env_id != element_in.environment_id:
        # Get the new environment to check its organization
        new_env = db.query(Environment).filter_by(id=element_in.environment_id).first()
        if not new_env:
            raise HTTPException(status_code=404, detail="New environment not found")

        # Check if user has permission to access the new environment's organization
        if not permissions.has_permission(db, current_user, new_env.organization_id, "element:update"):
            raise HTTPException(status_code=403, detail="Insufficient permission to move element to new environment")

    updated = element_repo.update_element(db, element, name=element_in.name, description=element_in.description, environment_id=element_in.environment_id)

    # Get physical hosts associated with the element's environment
    environment_id = updated.environment_id
    physical_hosts = physical_host_repo.list_physical_hosts_by_environment(db, environment_id)

    # Create a serializable element with environment_physical_hosts
    serializable_element = ElementOut.model_validate(updated)
    serializable_element.environment_physical_hosts = [PhysicalHostOut.model_validate(host) for host in physical_hosts]

    # Check if the element has at least one sub-component
    if not element_repo.has_subcomponent(updated):
        # Rollback the transaction if the element doesn't have any sub-components
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="An element must have at least one sub-component (network, vm, storage_pool, etc.)"
        )

    # Create appropriate audit log message
    if element_in.environment_id is not None and original_env_id != element_in.environment_id:
        audit.log_action(db, current_user.id, "Element update", f"Update of element '{updated.name}' (ID {updated.id}) - Environment change: {original_env_id} → {updated.environment_id}")
    else:
        audit.log_action(db, current_user.id, "Element update", f"Update of element '{updated.name}' (ID {updated.id})")
    return response.success_response(serializable_element, "Element updated")


@router.delete(
    "/{element_id}",
    response_model=BaseResponse[EmptyData],
    summary="Delete an element",
    description="Deletes a given element.",
    responses={
        200: {"description": "Element deleted successfully"},
        401: {"description": "Not authenticated"},
        403: {"description": "Insufficient permission"},
        404: {"description": "Element not found"},
    }
)
def delete_element(
    element_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    element = element_repo.get_element(db, element_id)
    if not element:
        raise HTTPException(status_code=404, detail="Element not found")

    org_id = element.environment.organization_id
    if not permissions.has_permission(db, current_user, org_id, "element:delete"):
        raise HTTPException(status_code=403, detail="Insufficient permission to delete this element")

    # Check if the element has at least one sub-component
    if not element_repo.has_subcomponent(element):
        # This is just a sanity check, as elements without sub-components shouldn't exist
        # according to our new constraint
        raise HTTPException(
            status_code=400,
            detail="Cannot delete an element without sub-components (this element should not exist)"
        )

    element_repo.delete_element(db, element)
    audit.log_action(db, current_user.id, "Element deletion", f"Deletion of element '{element.name}' (ID {element.id})")
    return response.success_response(None, "Element deleted")

@router.get(
    "/{element_id}/tags",
    response_model=BaseResponse[List[TagOut]],
    summary="List element tags",
    description="Retrieves all tags associated with an element.",
    responses={
        200: {"description": "Tags retrieved successfully"},
        401: {"description": "Not authenticated"},
        403: {"description": "Insufficient permission"},
        404: {"description": "Element not found"}
    }
)
def list_element_tags(
    element_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check that the element exists
    element = db.query(Element).filter(Element.id == element_id).first()
    if not element:
        raise HTTPException(status_code=404, detail="Element not found")

    # Check permissions on the element's environment organization
    org_id = element.environment.organization_id
    if not permissions.has_permission(db, current_user, org_id, "element:read"):
        raise HTTPException(status_code=403, detail="Insufficient permission to access this element")

    # Convert Tag objects to TagOut for proper serialization
    serializable_tags = [TagOut.model_validate(tag) for tag in element.tags]

    return response.success_response(serializable_tags, "Element tags retrieved successfully")


@router.post(
    "/{element_id}/tags/{tag_id}",
    response_model=BaseResponse[ElementOut],
    summary="Add a tag to an element",
    description="Associates an existing tag with an element.",
    responses={
        200: {"description": "Tag added to element successfully"},
        401: {"description": "Not authenticated"},
        403: {"description": "Insufficient permission"},
        404: {"description": "Element or tag not found"},
    }
)
def add_tag_to_element(
    element_id: int,
    tag_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check that the element exists
    element = db.query(Element).filter(Element.id == element_id).first()
    if not element:
        raise HTTPException(status_code=404, detail="Element not found")

    # Check permissions on the element's environment organization
    org_id = element.environment.organization_id
    if not permissions.has_permission(db, current_user, org_id, "element:update"):
        raise HTTPException(status_code=403, detail="Insufficient permission to modify this element")

    # Check that the tag exists
    tag = tag_repo.get_tag(db, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")

    # Check if the tag is already associated with the element
    if tag in element.tags:
        return response.success_response(element, "Tag is already associated with this element")

    # Add the tag to the element
    element.tags.append(tag)
    db.commit()

    audit.log_action(db, current_user.id, "Add tag to element", f"Tag '{tag.value}' added to element '{element.name}'")
    return response.success_response(element, "Tag added to element successfully")


@router.delete(
    "/{element_id}/tags/{tag_id}",
    response_model=BaseResponse[ElementOut],
    summary="Remove a tag from an element",
    description="Removes the association between a tag and an element.",
    responses={
        200: {"description": "Tag removed from element successfully"},
        401: {"description": "Not authenticated"},
        403: {"description": "Insufficient permission"},
        404: {"description": "Element or tag not found"},
    }
)
def remove_tag_from_element(
    element_id: int,
    tag_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check that the element exists
    element = db.query(Element).filter(Element.id == element_id).first()
    if not element:
        raise HTTPException(status_code=404, detail="Element not found")

    # Check permissions on the element's environment organization
    org_id = element.environment.organization_id
    if not permissions.has_permission(db, current_user, org_id, "element:update"):
        raise HTTPException(status_code=403, detail="Insufficient permission to modify this element")

    # Check that the tag exists
    tag = tag_repo.get_tag(db, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")

    # Check if the tag is associated with the element
    if tag not in element.tags:
        return response.success_response(element, "Tag is not associated with this element")

    # Remove the tag from the element
    element.tags.remove(tag)
    db.commit()

    audit.log_action(db, current_user.id, "Remove tag from element", f"Tag '{tag.value}' removed from element '{element.name}'")
    return response.success_response(element, "Tag removed from element successfully")
