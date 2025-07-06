from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from ..database.session import SessionLocal
from ..schema.user import UserCreate, UserOut, UserUpdate, ChangePassword, ChangeSuperadmin
from ..schema.auth import BaseResponse, EmptyData
from ..schema.group import GroupOut
from ..schema.policy import PolicyOut
from ..schema.organization import OrganizationOut
from ..schema.tag import TagOut
from ..models.user import User
from ..repositories import user_repo, tag_repo, group_repo
from ..api.auth import get_current_user
from ..helper import audit, response, security, permissions, email
from datetime import timedelta
import secrets

router = APIRouter(prefix="/users", tags=["users"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("", response_model=BaseResponse[UserOut],
    summary="Create a user in free mode",
    description="Creates a new user in free mode in the system. The first user created automatically becomes superadmin.",
    responses={
         200: {"description": "User created successfully"},
         400: {"description": "Email already registered"},
     }
)
def register_user(user_in: UserCreate, db: Session = Depends(get_db)):
    # TODO: Add flag to allow/forbid free creation
    # TODO: Implement email confirmation for free creation (send email + validation endpoint)

    if user_repo.get_user_by_email(db, user_in.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    is_superadmin = db.query(User).first() is None
    user = user_repo.create_user(db, email=user_in.email, username=user_in.username, first_name=user_in.first_name, last_name=user_in.last_name,password=user_in.password, is_superadmin=is_superadmin)
    audit.log_action(db, user.id, "User creation", f"Creation of user {user.email}")
    return response.success_response(UserOut.model_validate(user), "User created successfully")

@router.post("/{organization_id}", response_model=BaseResponse[UserOut], summary="Create a user",
             description="Creates a new user in the system. It is attached to an Organization",
             responses={
    200: {"description": "User created successfully"},
    400: {"description": "Email already registered"},
    401: {"description": "Not authenticated"},
    403: {"description": "Insufficient permission"}
})
def create_user(organization_id: int, user_in: UserCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not permissions.has_permission(db, current_user, organization_id, "user:create"):
        raise HTTPException(status_code=403, detail="Insufficient permission")
    if user_repo.get_user_by_email(db, user_in.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    # Check if organization exists
    from ..repositories import organization_repo
    organization = organization_repo.get_organization(db, organization_id)
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")

    is_superadmin = False
    user = user_repo.create_user(db, email=user_in.email, username=user_in.username, first_name=user_in.first_name,
                                 last_name=user_in.last_name, password=user_in.password, is_superadmin=is_superadmin)

    # Associate user with organization
    user_repo.add_user_to_organization(db, user, organization)

    audit.log_action(db, user.id, "User creation", f"Creation of user {user.email} in organization {organization.name}")
    return response.success_response(UserOut.model_validate(user), "User created successfully")

@router.get("", response_model=BaseResponse[List[UserOut]],
    summary="List users",
    description="Retrieves the list of users with pagination and optional filtering by email.",
    responses={
    200: {"description": "Users retrieved successfully"},
    401: {"description": "Not authenticated"},
    403: {"description": "Insufficient permission"}
})
def list_users(current_user: User = Depends(get_current_user), db: Session = Depends(get_db), skip: int = 0, limit: int = 100, email: Optional[str] = None):
    if not permissions.has_permission(db, current_user, None, "user:list"):
        raise HTTPException(status_code=403, detail="Insufficient permission")
    query = db.query(User)
    if email:
        query = query.filter(User.email.ilike(f"%{email}%"))
    users = query.offset(skip).limit(limit).all()
    return response.success_response([UserOut.model_validate(user) for user in users], "Users list")

@router.get("/{user_id}", response_model=BaseResponse[UserOut],
    summary="Get a user",
    description="Retrieves detailed information of a specific user by their ID.",
    responses={
        200: {"description": "User retrieved successfully"},
        401: {"description": "Not authenticated"},
        403: {"description": "Insufficient permission"},
        404: {"description": "User not found"}
})
def get_user(user_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    user = user_repo.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if current_user.id != user_id and  not permissions.has_permission(db, current_user, None, "user:read"):
        raise HTTPException(status_code=403, detail="Insufficient permission")
    return response.success_response(UserOut.model_validate(user), "User retrieved successfully")

@router.put(
    "/{user_id}",
    response_model=BaseResponse[UserOut],
    summary="Update user information",
    description="Modifies the personal information of an existing user (last name, first name, email, username).",
    responses={
        200: {"description": "User updated successfully"},
        400: {"description": "Update failed"},
        401: {"description": "Not authenticated"},
        403: {"description": "Modification not authorized"},
        404: {"description": "User not found"},
    }
)
def update_user(user_id: int, user_in: UserUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    user = user_repo.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if current_user.id != user_id:
        if not permissions.has_permission(db, current_user, None, "user:update"):
            raise HTTPException(status_code=403, detail="Modification not authorized")
    try:
        user.first_name = user_in.first_name
        user.last_name = user_in.last_name
        user.username = user_in.username
        user.email = user_in.email
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail="Update failed")
    audit.log_action(db, current_user.id, "User update", f"Update of user {user.email} (ID {user.id})")
    return response.success_response(UserOut.model_validate(user), "User updated")

@router.delete("/{user_id}", response_model=BaseResponse[EmptyData],
    summary="Delete a user",
    description="Permanently deletes a user from the system. A user cannot delete themselves, and the last superadmin cannot be deleted.",
    responses={
        200: {"description": "User deleted successfully"},
        400: {"description": "You cannot delete yourself or other deletion restriction"},
        401: {"description": "Not authenticated"},
        403: {"description": "Modification not authorized"},
        404: {"description": "User not found"},
    })
def delete_user(user_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.id == user_id:
        raise HTTPException(status_code=400, detail="You cannot delete yourself")
    user = user_repo.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not permissions.has_permission(db, current_user, None, "user:delete"):
        raise HTTPException(status_code=403, detail="Not authorized")
    if user.is_superadmin:
        other_super = db.query(User).filter(User.is_superadmin == True, User.id != user.id).first()
        if not other_super:
            raise HTTPException(status_code=400, detail="Cannot delete the last superadmin")
    user_repo.delete_user(db, user)
    audit.log_action(db, current_user.id, "User deletion", f"Deletion of user {user.email}")
    return response.success_response(EmptyData(), "User deleted")

@router.put("/{user_id}/password", response_model=BaseResponse[EmptyData],
    summary="Change password",
    description="Allows a user to change their own password or an administrator to reset another user's password.",
    responses={
        200: {"description": "Password updated successfully"},
        400: {"description": "Incorrect passwords"},
        401: {"description": "Not authenticated"},
        403: {"description": "Modification not authorized"},
        404: {"description": "User not found"},
    })
def change_password(user_id: int, cp: ChangePassword, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    user = user_repo.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if permissions.has_permission(db, current_user, None, "user:update_password") and current_user.id != user_id:
        if cp.new_password and user.is_superadmin:
            user.hashed_password = security.get_password_hash(cp.new_password)
            db.commit()
            return response.success_response(EmptyData(), "Password reset by admin")
        elif cp.send_email:
            token = security.create_password_reset_token(user.id)
            email.send_reset_email(user.email, token)
            return response.success_response(EmptyData(), "Reset email sent")
        elif user.is_superadmin:
            new_pass = secrets.token_urlsafe(20)
            user.hashed_password = security.get_password_hash(new_pass)
            db.commit()
            return response.success_response({"new_password": new_pass}, "Password generated")
        else:
            raise HTTPException(status_code=403, detail="Not authorized")
    else:
        if current_user.id != user_id:
            raise HTTPException(status_code=403, detail="Not authorized")
        if cp.old_password is None or cp.new_password is None:
            raise HTTPException(status_code=400, detail="Passwords cannot be empty")
        if not security.verify_password(cp.old_password, user.hashed_password):
            raise HTTPException(status_code=400, detail="Current password incorrect")
        user.hashed_password = security.get_password_hash(cp.new_password)
        db.commit()
        return response.success_response(EmptyData(), "Password updated")

@router.put("/{user_id}/superadmin", response_model=BaseResponse[EmptyData],
    summary="Modify superadmin status",
    description="Allows a superadmin to modify another user's superadmin status. A superadmin cannot modify their own status, and the last superadmin cannot be demoted.",
    responses={
        200: {"description": "User updated successfully"},
        400: {"description": "Cannot remove last superadmin"},
        401: {"description": "Not authenticated"},
        403: {"description": "Modification not authorized"},
        404: {"description": "User not found"},
    })
def change_superadmin(user_id: int, change: ChangeSuperadmin, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Only superadmins can change superadmin status
    if not current_user.is_superadmin:
        raise HTTPException(status_code=403, detail="Not authorized")
    # Users can't change their own superadmin status
    if current_user.id == user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    user = user_repo.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.is_superadmin and not change.is_superadmin:
        # Check not really useful - third-party superadmin is removed by the logged-in superadmin
        other_super = db.query(User).filter(User.is_superadmin == True, User.id != user_id).first()
        if not other_super:
            raise HTTPException(status_code=400, detail="Cannot remove last superadmin")
    user.is_superadmin = change.is_superadmin
    db.commit()
    audit.log_action(db, current_user.id, "Superadmin modification", f"Status changed for {user.email}")
    return response.success_response(EmptyData(), "Superadmin status updated")

@router.get("/{user_id}/groups", response_model=BaseResponse[List[GroupOut]],
    summary="User groups",
    description="Retrieves the list of groups the user belongs to.",
    responses={
        200: {"description": "Groups retrieved"},
        401: {"description": "Not authenticated"},
        403: {"description": "Read not authorized"},
        404: {"description": "User not found"},
    })
def list_user_groups(user_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.id != user_id and not permissions.has_permission(db, current_user, None, "user:read_groups"):
        raise HTTPException(status_code=403, detail="Not authorized")
    user = user_repo.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return response.success_response([GroupOut.model_validate(group) for group in user.groups], "Groups retrieved")

@router.get("/{user_id}/policies", response_model=BaseResponse[List[PolicyOut]],
    summary="User policies",
    description="Retrieves the list of policies directly associated with the user.",
    responses={
        200: {"description": "Policies retrieved"},
        401: {"description": "Not authenticated"},
        403: {"description": "Read not authorized"},
        404: {"description": "User not found"},
    })
def list_user_policies(user_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.id != user_id and not permissions.has_permission(db, current_user, None, "user:read_policies"):
        raise HTTPException(status_code=403, detail="Not authorized")
    user = user_repo.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return response.success_response([PolicyOut.model_validate(policy) for policy in user.policies], "Policies retrieved")

@router.get("/{user_id}/organizations", response_model=BaseResponse[List[OrganizationOut]],
    summary="User organizations",
    description="Retrieves the list of organizations the user is associated with.",
    responses={
        200: {"description": "Organizations retrieved"},
        401: {"description": "Not authenticated"},
        403: {"description": "Read not authorized"},
        404: {"description": "User not found"},
    })
def list_user_organizations(user_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.id != user_id and not permissions.has_permission(db, current_user, None, "user:read_organizations"):
        raise HTTPException(status_code=403, detail="Not authorized")
    user = user_repo.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return response.success_response([OrganizationOut.model_validate(org) for org in user.organizations], "Organizations retrieved")

@router.get("/{user_id}/tags", response_model=BaseResponse[List[TagOut]],
    summary="List user tags",
    description="Retrieves the list of tags associated with a specific user.",
    responses={
        200: {"description": "Tags retrieved"},
        401: {"description": "Not authenticated"},
        403: {"description": "Read not authorized"},
        404: {"description": "User not found"},
    })
def list_user_tags(user_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.id != user_id and not permissions.has_permission(db, current_user, None, "user:read_tags"):
        raise HTTPException(status_code=403, detail="Not authorized")
    user = user_repo.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return response.success_response([TagOut.model_validate(tag) for tag in user.tags], "Tags retrieved")

@router.post("/{user_id}/tags/{tag_id}", response_model=BaseResponse[UserOut],
    summary="Associate tag with user",
    description="Adds a specific tag to a user for categorization or special attributes.",
    responses={
        200: {"description": "Tag added"},
        401: {"description": "Not authenticated"},
        403: {"description": "Add not authorized"},
        404: {"description": "User not found"},
    })
def add_tag_to_user(user_id: int, tag_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.id != user_id and not permissions.has_permission(db, current_user, None, "user:update_tags"):
        raise HTTPException(status_code=403, detail="Not authorized")
    user = user_repo.get_user(db, user_id)
    tag = tag_repo.get_tag(db, tag_id)
    if not user or not tag:
        raise HTTPException(status_code=404, detail="User or tag not found")
    user_repo.add_tag_to_user(db, user, tag)
    return response.success_response(UserOut.model_validate(user), "Tag added to user")

@router.delete("/{user_id}/tags/{tag_id}", response_model=BaseResponse[UserOut],
    summary="Remove tag from user",
    description="Removes a specific tag from a user, deleting the associated categorization or attributes.",
    responses={
        200: {"description": "Tag removed"},
        401: {"description": "Not authenticated"},
        403: {"description": "Delete not authorized"},
        404: {"description": "User not found"},
    })
def remove_tag_from_user(user_id: int, tag_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.id != user_id and not permissions.has_permission(db, current_user, None, "user:update_tags"):
        raise HTTPException(status_code=403, detail="Not authorized")
    user = user_repo.get_user(db, user_id)
    tag = tag_repo.get_tag(db, tag_id)
    if not user or not tag:
        raise HTTPException(status_code=404, detail="User or tag not found")
    user_repo.remove_tag_from_user(db, user, tag)
    return response.success_response(UserOut.model_validate(user), "Tag removed from user")
