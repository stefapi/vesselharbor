from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..api.users import get_current_user
from ..database.session import SessionLocal
from ..helper import response, permissions, audit
from ..helper.cosmicname import generate_codename
from ..models.environment import Environment
from ..models.function import Function
from ..models.group import Group
from ..models.organization import Organization
from ..models.user import User
from ..repositories import tag_repo, policy_repo, rule_repo, group_repo
from ..schema.auth import BaseResponse, EmptyData
from ..schema.element import ElementOut
from ..schema.environment import EnvironmentOut
from ..schema.group import GroupOut
from ..schema.organization import OrganizationOut, OrganizationCreate, OrganizationUpdate
from ..schema.policy import PolicyOut, PolicyCreate
from ..schema.tag import TagOut
from ..schema.user import UserOut

router = APIRouter(prefix="/organizations", tags=["organizations"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("", response_model=BaseResponse[List[OrganizationOut]], summary="List organizations", description="Retrieve list of organizations accessible to the user", responses={
    200: {"description": "Organization list retrieved successfully"},
    401: {"description": "Unauthenticated"}
})
def list_organizations(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    orgs = db.query(Organization).all()
    # Convert Organization objects to OrganizationOut objects for proper serialization
    serializable_orgs = [
        OrganizationOut.model_validate(org) for org in orgs if permissions.has_permission(db, current_user, org.id, "organization:read")
    ]
    return response.success_response(serializable_orgs, "Visible organizations retrieved")

@router.get("/{org_id}", response_model=BaseResponse[OrganizationOut], summary="Organization details", description="Retrieve details of a specific organization", responses={
    200: {"description": "Organization details retrieved successfully"},
    401: {"description": "Unauthenticated"},
    403: {"description": "Insufficient permissions"},
    404: {"description": "Organization not found"}
})
def get_organization(org_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    org = db.query(Organization).get(org_id)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    if not permissions.has_permission(db, current_user, org.id, "organization:read"):
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    # Convert Organization object to OrganizationOut object for proper serialization
    serializable_org = OrganizationOut.model_validate(org)
    return response.success_response(serializable_org, "Organization retrieved")

@router.post("", response_model=BaseResponse[OrganizationOut], summary="Create organization", description="Create a new organization and configure default groups/policies", responses={
    200: {"description": "Organization created successfully"},
    400: {"description": "An organization with this name already exists"},
    401: {"description": "Unauthenticated"},
    403: {"description": "You are already administrator of an organization"},
    500: {"description": "Server error - admin function not found"}
})
def create_organization(org_in: OrganizationCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if org_in.name == '':
        org_in.name = generate_codename()
    # Check if an organization with the same name already exists
    existing_org = db.query(Organization).filter(Organization.name == org_in.name).first()
    if existing_org:
        raise HTTPException(status_code=400, detail="An organization with this name already exists")

    # Check if user is already admin of another organization (unless superadmin)
    if not current_user.is_superadmin:
        # Query all admin groups to see if current user is already an admin somewhere
        admin_groups = db.query(Group).filter(Group.name == "admin").all()
        for admin_group in admin_groups:
            if current_user in admin_group.users:
                raise HTTPException(
                    status_code=403,
                    detail="You are already administrator of another organization. A user can only be administrator of one organization."
                )

    # Create the organization
    org = Organization(name=org_in.name, description=org_in.description)
    db.add(org)
    db.commit()
    db.refresh(org)

    # Add the user to the organization
    # Get the user from the same session as the organization to avoid session conflicts
    user_in_session = db.query(User).get(current_user.id)
    if user_in_session not in org.users:
        org.users.append(user_in_session)
        db.commit()

    # Create admin function
    admin_function = db.query(Function).filter(Function.name == "admin").first()
    if not admin_function:
        raise HTTPException(status_code=500, detail="Admin function not found")

    # Create admin policy for the organization
    admin_policy = policy_repo.create_policy(db, PolicyCreate(
        name=f"Admin {org.name}",
        description=f"Administration policy for {org.name}",
        organization_id=org.id
    ))

    # Create an admin rule for the policy
    rule_repo.create_rule(db, admin_policy.id, admin_function.id)

    # Create readonly policy for the organization
    readonly_policy = policy_repo.create_policy(db, PolicyCreate(
        name=f"Readonly {org.name}",
        description=f"Read-only policy for {org.name}",
        organization_id=org.id
    ))

    # Add read-only rules to the policy
    read_functions = ["organization:read", "env:read", "element:read", "group:read", "tag:read", "policy:read", "rule:read"]
    for func_name in read_functions:
        func = db.query(Function).filter(Function.name == func_name).first()
        if func:
            rule_repo.create_rule(db, readonly_policy.id, func.id)

    # Create 'admin' group
    admin_group = group_repo.create_group(db, org.id, "admin", "Organization administrators")
    # Assign admin policy to 'admin' group
    policy_repo.add_group(db, admin_policy, admin_group)

    # Create 'editors' group
    editors_group = group_repo.create_group(db, org.id, "editors", "Editors with read-only access")
    # Assign readonly policy to 'editors' group
    policy_repo.add_group(db, readonly_policy, editors_group)

    # If the user is not a superadmin, make them an admin of the organization
    if not current_user.is_superadmin:
        # Add the creator to the admin group
        # Get the user from the same session as the group to avoid session conflicts
        user_in_session = db.query(User).get(current_user.id)
        group_repo.add_user_to_group(db, admin_group, user_in_session)

    audit.log_action(db, current_user.id, "Organization creation", f"Organization '{org.name}'")
    # Convert Organization object to OrganizationOut object for proper serialization
    serializable_org = OrganizationOut.model_validate(org)
    return response.success_response(serializable_org, "Organization created")

@router.put("/{org_id}", response_model=BaseResponse[OrganizationOut], summary="Update organization", description="Update information of an existing organization", responses={
    200: {"description": "Organization updated successfully"},
    400: {"description": "An organization with this name already exists"},
    401: {"description": "Unauthenticated"},
    403: {"description": "Insufficient permissions"},
    404: {"description": "Organization not found"}
})
def update_organization(org_id: int, org_in: OrganizationUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    org = db.query(Organization).get(org_id)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    if not permissions.has_permission(db, current_user, org.id, "organization:update"):
        raise HTTPException(status_code=403, detail="Insufficient permissions")

    # Check if another organization with the same name already exists
    existing_org = db.query(Organization).filter(Organization.name == org_in.name, Organization.id != org_id).first()
    if existing_org:
        raise HTTPException(status_code=400, detail="An organization with this name already exists")

    org.name = org_in.name
    org.description = org_in.description
    db.commit()
    audit.log_action(db, current_user.id, "Organization update", f"Organization '{org.name}'")
    # Convert Organization object to OrganizationOut object for proper serialization
    serializable_org = OrganizationOut.model_validate(org)
    return response.success_response(serializable_org, "Organization updated")

@router.delete("/{org_id}", response_model=BaseResponse[EmptyData], summary="Delete organization", description="Delete an existing organization and all associated data", responses={
    200: {"description": "Organization deleted successfully"},
    401: {"description": "Unauthenticated"},
    403: {"description": "Insufficient permissions or users belong to other organizations"},
    404: {"description": "Organization not found"}
})
def delete_organization(org_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    org = db.query(Organization).get(org_id)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    if not permissions.has_permission(db, current_user, org.id, "organization:delete"):
        raise HTTPException(status_code=403, detail="Insufficient permissions")

    # If the user is not a superadmin, check if any user in the organization belongs to other organizations
    if not current_user.is_superadmin:
        for user in org.users:
            if len(user.organizations) <= 1:
                raise HTTPException(
                    status_code=403,
                    detail="Cannot delete organization because some users belong to other organizations"
                )

    db.delete(org)
    db.commit()
    audit.log_action(db, current_user.id, "Organization deletion", f"Organization '{org.name}'")
    return response.success_response(None, "Organization deleted")

# --- Users ---

@router.post("/{org_id}/users/{user_id}", response_model=BaseResponse[List[UserOut]], summary="Add user to organization", description="Add specified user to an organization", responses={
    200: {"description": "User added to organization successfully"},
    401: {"description": "Unauthenticated"},
    403: {"description": "Insufficient permissions"},
    404: {"description": "Organization or user not found"}
})
def add_user_to_organization(org_id: int, user_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    org = db.query(Organization).get(org_id)
    user = db.query(User).get(user_id)
    if not org or not user:
        raise HTTPException(status_code=404, detail="Organization or user not found")
    if not permissions.has_permission(db, current_user, org.id, "organization:update"):
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    if user not in org.users:
        org.users.append(user)
        db.commit()
        audit.log_action(db, current_user.id, "User added", f"User {user.email} added to organization {org.name}")
    # Convert User objects to UserOut objects for proper serialization
    serializable_users = [UserOut.model_validate(user) for user in org.users]
    return response.success_response(serializable_users, "User added")

@router.delete("/{org_id}/users/{user_id}", response_model=BaseResponse[List[UserOut]], summary="Remove user from organization", description="Remove specified user from an organization", responses={
    200: {"description": "User removed from organization successfully"},
    401: {"description": "Unauthenticated"},
    403: {"description": "Insufficient permissions"},
    404: {"description": "Organization or user not found"},
    409: {"description": "Cannot remove last administrator from the organization"}
})
def remove_user_from_organization(org_id: int, user_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    org = db.query(Organization).get(org_id)
    user = db.query(User).get(user_id)
    if not org or not user:
        raise HTTPException(status_code=404, detail="Organization or user not found")
    if not permissions.has_permission(db, current_user, org.id, "organization:update"):
        raise HTTPException(status_code=403, detail="Insufficient permissions")

    # Check if user is in the admin group
    admin_group = db.query(Group).filter(Group.organization_id == org.id, Group.name == "admin").first()
    is_admin = admin_group and user in admin_group.users

    # If user is an admin, check if there's at least one other admin
    if is_admin:
        admin_count = len(admin_group.users)
        if admin_count <= 1:
            raise HTTPException(
                status_code=409,
                detail="Cannot remove the last administrator from the organization"
            )

    if user in org.users:
        org.users.remove(user)
        db.commit()
        audit.log_action(db, current_user.id, "User removed", f"User {user.email} removed from organization {org.name}")

    # Convert User objects to UserOut objects for proper serialization
    serializable_users = [UserOut.model_validate(user) for user in org.users]
    return response.success_response(serializable_users, "User removed")

# --- Tags ---

@router.get("/{org_id}/tags", response_model=BaseResponse[List[TagOut]], summary="List organization tags", description="Retrieve all tags associated with an organization", responses={
    200: {"description": "Organization tags retrieved successfully"},
    401: {"description": "Unauthenticated"},
    403: {"description": "Insufficient permissions"}
})
def list_organization_tags(org_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not permissions.has_permission(db, current_user, org_id, "tag:read"):
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    tags = [tag for tag in tag_repo.list_tags(db) if any(
        p.organization_id == org_id for p in tag.policies
    ) or any(
        g.organization_id == org_id for g in tag.groups
    )]
    # Convert Tag objects to TagOut objects for proper serialization
    serializable_tags = [TagOut.model_validate(tag) for tag in tags]
    return response.success_response(serializable_tags, "Organization tags retrieved")

# --- Policies ---

@router.get("/{org_id}/policies", response_model=BaseResponse[List[PolicyOut]], summary="List organization policies", description="Retrieve all policies associated with an organization", responses={
    200: {"description": "Organization policies retrieved successfully"},
    401: {"description": "Unauthenticated"},
    403: {"description": "Insufficient permissions"},
    404: {"description": "Organization not found"}
})
def list_organization_policies(org_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    org = db.query(Organization).get(org_id)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    if not permissions.has_permission(db, current_user, org.id, "policy:read"):
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    # Convert Policy objects to PolicyOut objects for proper serialization
    serializable_policies = [PolicyOut.model_validate(policy) for policy in org.policies]
    return response.success_response(serializable_policies, "Policies retrieved")

# --- Groups ---

@router.get("/{org_id}/groups", response_model=BaseResponse[List[GroupOut]], summary="List organization groups", description="Retrieve all groups associated with an organization", responses={
    200: {"description": "Organization groups retrieved successfully"},
    401: {"description": "Unauthenticated"},
    403: {"description": "Insufficient permissions"},
    404: {"description": "Organization not found"}
})
def list_organization_groups(org_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    org = db.query(Organization).get(org_id)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    if not permissions.has_permission(db, current_user, org.id, "group:read"):
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    # Convert Group objects to GroupOut objects for proper serialization
    serializable_groups = [GroupOut.model_validate(group) for group in org.groups]
    return response.success_response(serializable_groups, "Groups retrieved")

@router.get("/{org_id}/environments", response_model=BaseResponse[List[EnvironmentOut]], summary="List organization environments", description="Retrieve all environments associated with an organization", responses={
    200: {"description": "Organization environments retrieved successfully"},
    401: {"description": "Unauthenticated"},
    404: {"description": "Organization not found"}
})
def list_organization_environments(org_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    org = db.query(Organization).get(org_id)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")

    # Query environments for this organization
    query = db.query(Environment).filter(Environment.organization_id == org_id)
    environments = query.all()

    # Filter by permission
    if not current_user.is_superadmin:
        environments = [
            env for env in environments
            if permissions.has_permission(db, current_user, env.organization_id, "env:read")
        ]

    # Convert Environment objects to EnvironmentOut objects for proper serialization
    serializable_environments = [EnvironmentOut.model_validate(env) for env in environments]
    return response.success_response(serializable_environments, "Organization environments retrieved")

@router.get("/{org_id}/users", response_model=BaseResponse[List[UserOut]], summary="List organization users", description="Retrieve all users with access to a specific organization.", responses={
    200: {"description": "Organization users retrieved successfully"},
    401: {"description": "Unauthenticated"},
    403: {"description": "Insufficient permissions"},
    404: {"description": "Organization not found"}
})
def list_organization_users(org_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    org = db.query(Organization).get(org_id)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    if not permissions.has_permission(db, current_user, org.id, "organization:read"):
        raise HTTPException(status_code=403, detail="Insufficient permissions")

    # Convert User objects to UserOut objects for proper serialization
    serializable_users = [UserOut.model_validate(user) for user in org.users]
    return response.success_response(serializable_users, "Organization users retrieved")

@router.get("/{org_id}/elements", response_model=BaseResponse[List[ElementOut]], summary="List organization elements", description="Retrieve all elements in an organization accessible to the user, with pagination and name filtering.", responses={
    200: {"description": "Organization elements retrieved successfully"},
    401: {"description": "Unauthenticated"},
    404: {"description": "Organization not found"}
})
def list_organization_elements(
    org_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    name: Optional[str] = None
):
    org = db.query(Organization).get(org_id)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")

    # Get all elements from the organization
    all_elements = org.elements

    # Filter elements based on user permissions
    accessible_elements = []
    for element in all_elements:
        # Check if user has permission to read this element
        if permissions.has_permission(db, current_user, element.environment.organization_id, "element:read"):
            # Filter by name if provided
            if name and name.lower() not in element.name.lower():
                continue
            accessible_elements.append(element)

    # Apply pagination
    paginated_elements = accessible_elements[skip:skip + limit]

    # Convert Element objects to ElementOut objects for proper serialization
    serializable_elements = [ElementOut.model_validate(element) for element in paginated_elements]
    return response.success_response(serializable_elements, "Organization elements retrieved")
