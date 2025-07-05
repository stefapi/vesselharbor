# app/api/environments.py

from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..api.users import get_current_user
from ..database.session import SessionLocal
from ..helper import permissions, audit, response
from ..helper.animalname import generate_codename
from ..models import Element
from ..models.application import Application
from ..models.container_cluster import ContainerCluster
from ..models.container_node import ContainerNode
from ..models.domain import Domain
from ..models.environment import Environment
from ..models.network import Network
from ..models.organization import Organization
from ..models.stack import Stack
from ..models.storage_pool import StoragePool
from ..models.user import User
from ..models.vm import VM
from ..models.volume import Volume
from ..repositories import environment_repo, group_repo, function_repo, tag_repo, physical_host_repo
from ..schema.element import ElementOut
from ..schema.environment import EnvironmentCreate, EnvironmentOut
from ..schema.physical_host import PhysicalHostOut
from ..schema.user import UserOut
from ..schema.tag import TagOut
from ..schema.auth import BaseResponse, EmptyData

router = APIRouter(prefix="/environments", tags=["environments"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get(
    "",
    response_model=BaseResponse[List[EnvironmentOut]],
    summary="List environments",
    description="Lists environments filtered by name or organization (superadmins see everything, others only what they have permission to read).",
    responses={
        200: {"description": "Environment list retrieved successfully"},
        401: {"description": "Not authenticated"},
        403: {"description": "Insufficient permission"}
    }
)
def list_environments(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    name: Optional[str] = None,
    organization_name: Optional[str] = None
):
    query = db.query(Environment).join(Organization)

    if name:
        query = query.filter(Environment.name.ilike(f"%{name}%"))
    if organization_name:
        query = query.filter(Organization.name.ilike(f"%{organization_name}%"))

    environments = query.offset(skip).limit(limit).all()

    # Filter by permissions
    if not current_user.is_superadmin:
        environments = [
            env for env in environments
            if permissions.has_permission(db, current_user, env.organization_id, "env:read")
        ]

    return response.success_response(environments, "Environment list retrieved")

@router.get(
    "/{environment_id}",
    response_model=BaseResponse[EnvironmentOut],
    summary="Environment details",
    description="Returns environment details if the user has access.",
    responses={
        200: {"description": "Environment retrieved successfully"},
        401: {"description": "Not authenticated"},
        403: {"description": "Insufficient permission"},
        404: {"description": "Environment not found"}
    }
)
def get_environment(
    environment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    environment = environment_repo.get_environment(db, environment_id)
    if not environment:
        raise HTTPException(status_code=404, detail="Environment not found")
    if not permissions.has_permission(db, current_user, environment.organization_id, "env:read"):
        raise HTTPException(status_code=403, detail="Insufficient permission")
    return response.success_response(environment, "Environment retrieved")

@router.get(
    "/{environment_id}/physical-hosts",
    response_model=BaseResponse[List[PhysicalHostOut]],
    summary="List physical hosts of an environment",
    description="Returns the list of physical hosts associated with an environment if the user has access to it.",
    responses={
        200: {"description": "Physical hosts list retrieved successfully"},
        401: {"description": "Not authenticated"},
        403: {"description": "Insufficient permission"},
        404: {"description": "Environment not found"}
    }
)
def get_environment_physical_hosts(
    environment_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    environment = environment_repo.get_environment(db, environment_id)
    if not environment:
        raise HTTPException(status_code=404, detail="Environment not found")
    if not permissions.has_permission(db, current_user, environment.organization_id, "env:read"):
        raise HTTPException(status_code=403, detail="Insufficient permission")

    physical_hosts = physical_host_repo.list_physical_hosts_by_environment(db, environment_id, skip, limit)
    return response.success_response(
        [PhysicalHostOut.model_validate(host) for host in physical_hosts],
        "Physical hosts list retrieved"
    )

@router.post(
    "",
    response_model=BaseResponse[EnvironmentOut],
    summary="Create an environment",
    description="Creates an environment attached to an organization. Assigns an admin policy to the creator if needed.",
    responses={
        200: {"description": "Environment created successfully"},
        401: {"description": "Not authenticated"},
        403: {"description": "Insufficient permission"},
        500: {"description": "The 'admin' function is missing"}
    }
)
def create_environment(
    env: EnvironmentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not permissions.has_permission(db, current_user, env.organization_id, "env:create"):
        raise HTTPException(status_code=403, detail="Insufficient permission to create an environment")

    # TODO add generate codename here
    environment = environment_repo.create_environment(
        db,
        name=env.name,
        organization_id=env.organization_id,
        description=env.description
    )

    # Create Admins group for this environment (optional if access policy already exists)
    admin_group = group_repo.create_group(
        db,
        name="Admins",
        description="Default admin group",
        organization_id=env.organization_id
    )

    # 'admin' function
    admin_function = function_repo.get_function_by_name(db, "admin")
    if not admin_function:
        raise HTTPException(status_code=500, detail="The 'admin' function is missing")

    group_repo.add_function_to_group(db, admin_group, admin_function)

    # Check: is the user already an environment admin via group/policy?
    is_already_admin = permissions.has_permission(db, current_user, environment.id, "env:update")

    if not is_already_admin:
        # Create a "creator" policy with `admin` rule on this env
        from ..models.rule import Rule
        from ..repositories import policy_repo

        policy_name = f"Policy {environment.name} - creator"
        policy = policy_repo.create_policy(
            db,
            name=policy_name,
            organization_id=env.organization_id,
            description=f"Automatic policy for the creator of environment {environment.name}"
        )

        # Add rule for this environment
        rule = Rule(policy=policy, environment_id=environment.id, function=admin_function)
        db.add(rule)

        # Add user to policy
        # Get the user from the same session as the policy to avoid session conflicts
        user_in_session = db.query(User).get(current_user.id)
        policy.users.append(user_in_session)

        db.commit()
        db.refresh(policy)

    audit.log_action(
        db,
        current_user.id,
        "Environment creation",
        f"Environment '{environment.name}' created (ID {environment.id})"
    )

    return response.success_response(environment, "Environment created successfully")

@router.put(
    "/{environment_id}",
    response_model=BaseResponse[EnvironmentOut],
    summary="Update an environment",
    description="Updates an environment if it exists and the user has permission.",
    responses={
        200: {"description": "Environment updated successfully"},
        401: {"description": "Not authenticated"},
        403: {"description": "Insufficient permission"},
        404: {"description": "Environment not found"}
    }
)
def update_environment(
    environment_id: int,
    env: EnvironmentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    environment = environment_repo.get_environment(db, environment_id)
    if not environment:
        raise HTTPException(status_code=404, detail="Environment not found")

    if not permissions.has_permission(db, current_user, environment.organization_id, "env:update"):
        raise HTTPException(status_code=403, detail="Insufficient permission")

    environment.name = env.name
    environment.description = env.description
    # We don't update organization_id as it would require additional permission checks and might break relationships

    db.commit()
    db.refresh(environment)

    audit.log_action(db, current_user.id, "Environment update", f"Environment '{environment.name}' updated")
    return response.success_response(environment, "Environment updated")

@router.delete(
    "/{environment_id}",
    response_model=BaseResponse[EmptyData],
    summary="Delete an environment",
    description="Deletes an environment if the user has the required permissions.",
    responses={
        200: {"description": "Environment deleted successfully"},
        401: {"description": "Not authenticated"},
        403: {"description": "Insufficient permission"},
        404: {"description": "Environment not found"}
    }
)
def delete_environment(
    environment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    environment = environment_repo.get_environment(db, environment_id)
    if not environment:
        raise HTTPException(status_code=404, detail="Environment not found")

    if not permissions.has_permission(db, current_user, environment.organization_id, "env:delete"):
        raise HTTPException(status_code=403, detail="Insufficient permission")

    environment_repo.delete_environment(db, environment)

    audit.log_action(db, current_user.id, "Environment deletion", f"Environment {environment.name} deleted")
    return response.success_response(None, "Environment deleted")

@router.get(
    "/generate-name",
    response_model=BaseResponse[str],
    summary="Generate a random name",
    description="Generates a unique name from an animal or an adjective.",
    responses={
        200: {"description": "Name generated successfully"},
        401: {"description": "Not authenticated"}
    }
)
def generate_environment_codename(
    current_user: User = Depends(get_current_user),
    prefix_length: int = Query(0, ge=0, le=6),
    use_adjective: bool = Query(True),
    use_adverb: bool = Query(False),
    suffix_length: int = Query(0, ge=0, le=6),
    separator: str = Query("-", max_length=2),
    style: Optional[str] = Query(None)
):
    name = generate_codename(
        prefix_length=prefix_length,
        use_adjective=use_adjective,
        use_adverb=use_adverb,
        suffix_length=suffix_length,
        separator=separator,
        style=style
    )
    return response.success_response(name, "Name generated successfully")

@router.get(
    "/{environment_id}/users",
    response_model=BaseResponse[List[UserOut]],
    summary="Users linked to an environment",
    description="Returns all users who have access to an environment via a policy (via rules).",
    responses={
        200: {"description": "Users retrieved successfully"},
        401: {"description": "Not authenticated"},
        403: {"description": "Insufficient permission"},
        404: {"description": "Environment not found"}
    }
)
def get_environment_users(
    environment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    environment = environment_repo.get_environment(db, environment_id)
    if not environment:
        raise HTTPException(status_code=404, detail="Environment not found")

    if not permissions.has_permission(db, current_user, environment.organization_id, "env:read"):
        raise HTTPException(status_code=403, detail="Insufficient permission")

    return response.success_response(environment.users, "Users retrieved")


@router.get(
    "/{environment_id}/elements",
    response_model=BaseResponse[List[ElementOut]],
    summary="List elements of an environment",
    description="Lists the elements of an environment with pagination and filtering by name and type.",
    responses={
        200: {"description": "Elements list retrieved successfully"},
        401: {"description": "Not authenticated"},
        403: {"description": "Insufficient permission"},
        404: {"description": "Environment not found"},
        400: {"description": "Invalid element type"},
    }
)
def list_elements(
    environment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    name: Optional[str] = None,
    element_type: Optional[str] = Query(None, description="Element type to filter (network, vm, storage_pool, volume, domain, container_node, container_cluster, stack, application)")
):
    env = db.query(Environment).filter_by(id=environment_id).first()
    if not env:
        raise HTTPException(status_code=404, detail="Environment not found")

    if not permissions.has_permission(db, current_user, env.organization_id, "element:read"):
        raise HTTPException(status_code=403, detail="Insufficient permission to list elements")

    query = db.query(Element).filter(Element.environment_id == environment_id)

    # Filter by element type if specified
    if element_type:
        if element_type == "network":
            query = query.join(Network, Element.id == Network.element_id)
        elif element_type == "vm":
            query = query.join(VM, Element.id == VM.element_id)
        elif element_type == "storage_pool":
            query = query.join(StoragePool, Element.id == StoragePool.element_id)
        elif element_type == "volume":
            query = query.join(Volume, Element.id == Volume.element_id)
        elif element_type == "domain":
            query = query.join(Domain, Element.id == Domain.element_id)
        elif element_type == "container_node":
            query = query.join(ContainerNode, Element.id == ContainerNode.element_id)
        elif element_type == "container_cluster":
            query = query.join(ContainerCluster, Element.id == ContainerCluster.element_id)
        elif element_type == "stack":
            query = query.join(Stack, Element.id == Stack.element_id)
        elif element_type == "application":
            query = query.join(Application, Element.id == Application.element_id)
        else:
            raise HTTPException(status_code=400, detail=f"Invalid element type: {element_type}")

    # Filter by name if specified
    if name:
        query = query.filter(Element.name.ilike(f"%{name}%"))

    # Apply pagination
    elements = query.offset(skip).limit(limit).all()

    # Convert elements to ElementOut for serialization
    serializable_elements = [ElementOut.model_validate(element) for element in elements]

    return response.success_response(serializable_elements, "Elements list retrieved")

@router.get(
    "/{environment_id}/tags",
    response_model=BaseResponse[List[TagOut]],
    summary="List environment tags",
    description="Retrieves all tags associated with an environment.",
    responses={
        200: {"description": "Tags retrieved successfully"},
        401: {"description": "Not authenticated"},
        403: {"description": "Insufficient permission"},
        404: {"description": "Environment not found"}
    }
)
def list_environment_tags(
    environment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check that the environment exists
    environment = db.query(Environment).filter(Environment.id == environment_id).first()
    if not environment:
        raise HTTPException(status_code=404, detail="Environment not found")

    # Check permissions on the environment's organization
    org_id = environment.organization_id
    if not permissions.has_permission(db, current_user, org_id, "env:read"):
        raise HTTPException(status_code=403, detail="Insufficient permission to access this environment")

    # Convert Tag objects to TagOut for proper serialization
    from ..schema.tag import TagOut
    serializable_tags = [TagOut.model_validate(tag) for tag in environment.tags]

    return response.success_response(serializable_tags, "Environment tags retrieved successfully")


@router.post(
    "/{environment_id}/tags/{tag_id}",
    response_model=BaseResponse[EnvironmentOut],
    summary="Add a tag to an environment",
    description="Associates an existing tag with an environment.",
    responses={
        200: {"description": "Tag added to environment successfully"},
        401: {"description": "Not authenticated"},
        403: {"description": "Insufficient permission"},
        404: {"description": "Environment or tag not found"}
    }
)
def add_tag_to_environment(
    environment_id: int,
    tag_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check that the environment exists
    environment = db.query(Environment).filter(Environment.id == environment_id).first()
    if not environment:
        raise HTTPException(status_code=404, detail="Environment not found")

    # Check permissions on the environment's organization
    org_id = environment.organization_id
    if not permissions.has_permission(db, current_user, org_id, "env:update"):
        raise HTTPException(status_code=403, detail="Insufficient permission to modify this environment")

    # Verify tag exists
    tag = tag_repo.get_tag(db, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")

    # Verify if tag is already associated with environment
    if tag in environment.tags:
        return response.success_response(environment, "Tag is already associated with this environment")

    # Add the tag to the environment
    environment.tags.append(tag)
    db.commit()

    audit.log_action(db, current_user.id, "Add tag to environment", f"Tag '{tag.value}' added to environment '{environment.name}'")
    return response.success_response(environment, "Tag added to environment successfully")

@router.delete(
    "/{environment_id}/tags/{tag_id}",
    response_model=BaseResponse[EnvironmentOut],
    summary="Remove a tag from an environment",
    description="Removes association between a tag and an environment.",
    responses={
        200: {"description": "Tag removed from environment successfully"},
        401: {"description": "Not authenticated"},
        403: {"description": "Insufficient permission"},
        404: {"description": "Environment or tag not found"}
    }
)
def remove_tag_from_environment(
    environment_id: int,
    tag_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check that the environment exists
    environment = db.query(Environment).filter(Environment.id == environment_id).first()
    if not environment:
        raise HTTPException(status_code=404, detail="Environment not found")

    # Check permissions on the environment's organization
    org_id = environment.organization_id
    if not permissions.has_permission(db, current_user, org_id, "env:update"):
        raise HTTPException(status_code=403, detail="Insufficient permission to modify this environment")

    # Verify tag exists
    tag = tag_repo.get_tag(db, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")

    # Verify if tag is associated with environment
    if tag not in environment.tags:
        return response.success_response(environment, "Tag is not associated with this environment")

    # Remove the tag from the environment
    environment.tags.remove(tag)
    db.commit()

    audit.log_action(db, current_user.id, "Remove tag from environment", f"Tag '{tag.value}' removed from environment '{environment.name}'")
    return response.success_response(environment, "Tag removed from environment successfully")

@router.get(
    "/{environment_id}/networks",
    response_model=BaseResponse[List[ElementOut]],
    summary="List networks of an environment",
    description="Lists network-type elements in an environment with pagination and name filtering.",
    responses={
        200: {"description": "Networks list retrieved successfully"},
        401: {"description": "Not authenticated"},
        403: {"description": "Insufficient permission"},
        404: {"description": "Environment not found"},
    }
)
def list_networks(
    environment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    name: Optional[str] = None
):
    # Check that the environment exists
    env = db.query(Environment).filter_by(id=environment_id).first()
    if not env:
        raise HTTPException(status_code=404, detail="Environment not found")

    # Check permissions
    if not permissions.has_permission(db, current_user, env.organization_id, "element:read"):
        raise HTTPException(status_code=403, detail="Insufficient permission to list networks")

    # Build query for network-type elements
    query = db.query(Element).join(Network, Element.id == Network.element_id).filter(Element.environment_id == environment_id)

    # Filter by name if specified
    if name:
        query = query.filter(Element.name.ilike(f"%{name}%"))

    # Apply pagination
    elements = query.offset(skip).limit(limit).all()

    # Convert elements to ElementOut for serialization
    serializable_elements = [ElementOut.model_validate(element) for element in elements]

    return response.success_response(serializable_elements, "Networks list retrieved")

@router.get(
    "/{environment_id}/vms",
    response_model=BaseResponse[List[ElementOut]],
    summary="List virtual machines of an environment",
    description="Lists virtual machine-type elements in an environment with pagination and name filtering.",
    responses={
        200: {"description": "Virtual machines list retrieved successfully"},
        401: {"description": "Not authenticated"},
        403: {"description": "Insufficient permission"},
        404: {"description": "Environment not found"},
    }
)
def list_vms(
    environment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    name: Optional[str] = None
):
    # Check that the environment exists
    env = db.query(Environment).filter_by(id=environment_id).first()
    if not env:
        raise HTTPException(status_code=404, detail="Environment not found")

    # Check permissions
    if not permissions.has_permission(db, current_user, env.organization_id, "element:read"):
        raise HTTPException(status_code=403, detail="Insufficient permission to list virtual machines")

    # Build query for VM-type elements
    query = db.query(Element).join(VM, Element.id == VM.element_id).filter(Element.environment_id == environment_id)

    # Filter by name if specified
    if name:
        query = query.filter(Element.name.ilike(f"%{name}%"))

    # Apply pagination
    elements = query.offset(skip).limit(limit).all()

    # Convert elements to ElementOut for serialization
    serializable_elements = [ElementOut.model_validate(element) for element in elements]

    return response.success_response(serializable_elements, "Virtual machines list retrieved")

@router.get(
    "/{environment_id}/storage-pools",
    response_model=BaseResponse[List[ElementOut]],
    summary="List storage pools of an environment",
    description="Lists storage pool-type elements in an environment with pagination and name filtering.",
    responses={
        200: {"description": "Storage pools list retrieved successfully"},
        401: {"description": "Not authenticated"},
        403: {"description": "Insufficient permission"},
        404: {"description": "Environment not found"},
    }
)
def list_storage_pools(
    environment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    name: Optional[str] = None
):
    # Check that the environment exists
    env = db.query(Environment).filter_by(id=environment_id).first()
    if not env:
        raise HTTPException(status_code=404, detail="Environment not found")

    # Check permissions
    if not permissions.has_permission(db, current_user, env.organization_id, "element:read"):
        raise HTTPException(status_code=403, detail="Insufficient permission to list storage pools")

    # Build query for StoragePool-type elements
    query = db.query(Element).join(StoragePool, Element.id == StoragePool.element_id).filter(Element.environment_id == environment_id)

    # Filter by name if specified
    if name:
        query = query.filter(Element.name.ilike(f"%{name}%"))

    # Apply pagination
    elements = query.offset(skip).limit(limit).all()

    # Convert elements to ElementOut for serialization
    serializable_elements = [ElementOut.model_validate(element) for element in elements]

    return response.success_response(serializable_elements, "Storage pools list retrieved")

@router.get(
    "/{environment_id}/volumes",
    response_model=BaseResponse[List[ElementOut]],
    summary="List volumes of an environment",
    description="Lists volume-type elements in an environment with pagination and name filtering.",
    responses={
        200: {"description": "Volumes list retrieved successfully"},
        401: {"description": "Not authenticated"},
        403: {"description": "Insufficient permission"},
        404: {"description": "Environment not found"},
    }
)
def list_volumes(
    environment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    name: Optional[str] = None
):
    # Check that the environment exists
    env = db.query(Environment).filter_by(id=environment_id).first()
    if not env:
        raise HTTPException(status_code=404, detail="Environment not found")

    # Check permissions
    if not permissions.has_permission(db, current_user, env.organization_id, "element:read"):
        raise HTTPException(status_code=403, detail="Insufficient permission to list volumes")

    # Build query for Volume-type elements
    query = db.query(Element).join(Volume, Element.id == Volume.element_id).filter(Element.environment_id == environment_id)

    # Filter by name if specified
    if name:
        query = query.filter(Element.name.ilike(f"%{name}%"))

    # Apply pagination
    elements = query.offset(skip).limit(limit).all()

    # Convert elements to ElementOut for serialization
    serializable_elements = [ElementOut.model_validate(element) for element in elements]

    return response.success_response(serializable_elements, "Volumes list retrieved")

@router.get(
    "/{environment_id}/domains",
    response_model=BaseResponse[List[ElementOut]],
    summary="List domains of an environment",
    description="Lists domain-type elements in an environment with pagination and name filtering.",
    responses={
        200: {"description": "Domains list retrieved successfully"},
        401: {"description": "Not authenticated"},
        403: {"description": "Insufficient permission"},
        404: {"description": "Environment not found"},
    }
)
def list_domains(
    environment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    name: Optional[str] = None
):
    # Check that the environment exists
    env = db.query(Environment).filter_by(id=environment_id).first()
    if not env:
        raise HTTPException(status_code=404, detail="Environment not found")

    # Check permissions
    if not permissions.has_permission(db, current_user, env.organization_id, "element:read"):
        raise HTTPException(status_code=403, detail="Insufficient permission to list domains")

    # Build query for Domain-type elements
    query = db.query(Element).join(Domain, Element.id == Domain.element_id).filter(Element.environment_id == environment_id)

    # Filter by name if specified
    if name:
        query = query.filter(Element.name.ilike(f"%{name}%"))

    # Apply pagination
    elements = query.offset(skip).limit(limit).all()

    # Convert elements to ElementOut for serialization
    serializable_elements = [ElementOut.model_validate(element) for element in elements]

    return response.success_response(serializable_elements, "Domains list retrieved")

@router.get(
    "/{environment_id}/container-nodes",
    response_model=BaseResponse[List[ElementOut]],
    summary="List container nodes of an environment",
    description="Lists container node-type elements in an environment with pagination and name filtering.",
    responses={
        200: {"description": "Container nodes list retrieved successfully"},
        401: {"description": "Not authenticated"},
        403: {"description": "Insufficient permission"},
        404: {"description": "Environment not found"},
    }
)
def list_container_nodes(
    environment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    name: Optional[str] = None
):
    # Check that the environment exists
    env = db.query(Environment).filter_by(id=environment_id).first()
    if not env:
        raise HTTPException(status_code=404, detail="Environment not found")

    # Check permissions
    if not permissions.has_permission(db, current_user, env.organization_id, "element:read"):
        raise HTTPException(status_code=403, detail="Insufficient permission to list container nodes")

    # Build query for ContainerNode-type elements
    query = db.query(Element).join(ContainerNode, Element.id == ContainerNode.element_id).filter(Element.environment_id == environment_id)

    # Filter by name if specified
    if name:
        query = query.filter(Element.name.ilike(f"%{name}%"))

    # Apply pagination
    elements = query.offset(skip).limit(limit).all()

    # Convert elements to ElementOut for serialization
    serializable_elements = [ElementOut.model_validate(element) for element in elements]

    return response.success_response(serializable_elements, "Container nodes list retrieved")

@router.get(
    "/{environment_id}/container-clusters",
    response_model=BaseResponse[List[ElementOut]],
    summary="List container clusters of an environment",
    description="Lists container cluster-type elements in an environment with pagination and name filtering.",
    responses={
        200: {"description": "Container clusters list retrieved successfully"},
        401: {"description": "Not authenticated"},
        403: {"description": "Insufficient permission"},
        404: {"description": "Environment not found"},
    }
)
def list_container_clusters(
    environment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    name: Optional[str] = None
):
    # Check that the environment exists
    env = db.query(Environment).filter_by(id=environment_id).first()
    if not env:
        raise HTTPException(status_code=404, detail="Environment not found")

    # Check permissions
    if not permissions.has_permission(db, current_user, env.organization_id, "element:read"):
        raise HTTPException(status_code=403, detail="Insufficient permission to list container clusters")

    # Build query for ContainerCluster-type elements
    query = db.query(Element).join(ContainerCluster, Element.id == ContainerCluster.element_id).filter(Element.environment_id == environment_id)

    # Filter by name if specified
    if name:
        query = query.filter(Element.name.ilike(f"%{name}%"))

    # Apply pagination
    elements = query.offset(skip).limit(limit).all()

    # Convert elements to ElementOut for serialization
    serializable_elements = [ElementOut.model_validate(element) for element in elements]

    return response.success_response(serializable_elements, "Container clusters list retrieved")

@router.get(
    "/{environment_id}/stacks",
    response_model=BaseResponse[List[ElementOut]],
    summary="List stacks of an environment",
    description="Lists stack-type elements in an environment with pagination and name filtering.",
    responses={
        200: {"description": "Stacks list retrieved successfully"},
        401: {"description": "Not authenticated"},
        403: {"description": "Insufficient permission"},
        404: {"description": "Environment not found"},
    }
)
def list_stacks(
    environment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    name: Optional[str] = None
):
    # Check that the environment exists
    env = db.query(Environment).filter_by(id=environment_id).first()
    if not env:
        raise HTTPException(status_code=404, detail="Environment not found")

    # Check permissions
    if not permissions.has_permission(db, current_user, env.organization_id, "element:read"):
        raise HTTPException(status_code=403, detail="Insufficient permission to list stacks")

    # Build query for Stack-type elements
    query = db.query(Element).join(Stack, Element.id == Stack.element_id).filter(Element.environment_id == environment_id)

    # Filter by name if specified
    if name:
        query = query.filter(Element.name.ilike(f"%{name}%"))

    # Apply pagination
    elements = query.offset(skip).limit(limit).all()

    # Convert elements to ElementOut for serialization
    serializable_elements = [ElementOut.model_validate(element) for element in elements]

    return response.success_response(serializable_elements, "Stacks list retrieved")

@router.get(
    "/{environment_id}/applications",
    response_model=BaseResponse[List[ElementOut]],
    summary="List applications of an environment",
    description="Lists application-type elements in an environment with pagination and name filtering.",
    responses={
        200: {"description": "Applications list retrieved successfully"},
        401: {"description": "Not authenticated"},
        403: {"description": "Insufficient permission"},
        404: {"description": "Environment not found"},
    }
)
def list_applications(
    environment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    name: Optional[str] = None
):
    # Check that the environment exists
    env = db.query(Environment).filter_by(id=environment_id).first()
    if not env:
        raise HTTPException(status_code=404, detail="Environment not found")

    # Check permissions
    if not permissions.has_permission(db, current_user, env.organization_id, "element:read"):
        raise HTTPException(status_code=403, detail="Insufficient permission to list applications")

    # Build query for Application-type elements
    query = db.query(Element).join(Application, Element.id == Application.element_id).filter(Element.environment_id == environment_id)

    # Filter by name if specified
    if name:
        query = query.filter(Element.name.ilike(f"%{name}%"))

    # Apply pagination
    elements = query.offset(skip).limit(limit).all()

    # Convert elements to ElementOut for serialization
    serializable_elements = [ElementOut.model_validate(element) for element in elements]

    return response.success_response(serializable_elements, "Applications list retrieved")
