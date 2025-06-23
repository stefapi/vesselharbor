from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database.session import SessionLocal
from ..helper.cosmicname import generate_codename
from ..models.organization import Organization
from ..models.user import User
from ..models.tag import Tag
from ..models.group import Group
from ..models.policy import Policy
from ..repositories import tag_repo
from ..api.users import get_current_user
from ..helper import response, permissions, audit
from ..schema.organization import OrganizationOut, OrganizationCreate, OrganizationUpdate
from ..schema.tag import TagOut
from ..schema.group import GroupOut
from ..schema.policy import PolicyOut
from ..schema.environment import EnvironmentOut
from ..models.environment import Environment

router = APIRouter(prefix="/organizations", tags=["organizations"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("", response_model=dict)
def list_organizations(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    orgs = db.query(Organization).all()
    # Convert Organization objects to OrganizationOut objects for proper serialization
    serializable_orgs = [
        OrganizationOut.model_validate(org) for org in orgs if permissions.has_permission(db, current_user, org.id, "organization:read")
    ]
    return response.success_response(serializable_orgs, "Organisations visibles récupérées")

@router.get("/{org_id}", response_model=dict)
def get_organization(org_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    org = db.query(Organization).get(org_id)
    if not org:
        raise HTTPException(status_code=404, detail="Organisation non trouvée")
    if not permissions.has_permission(db, current_user, org.id, "organization:read"):
        raise HTTPException(status_code=403, detail="Permission insuffisante")
    # Convert Organization object to OrganizationOut object for proper serialization
    serializable_org = OrganizationOut.model_validate(org)
    return response.success_response(serializable_org, "Organisation récupérée")

@router.post("", response_model=dict)
def create_organization(org_in: OrganizationCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not current_user.is_superadmin:
        raise HTTPException(status_code=403, detail="Seul un superadmin peut créer une organisation")

    if org_in.name == '':
        org_in.name = generate_codename()
    # Check if an organization with the same name already exists
    existing_org = db.query(Organization).filter(Organization.name == org_in.name).first()
    if existing_org:
        raise HTTPException(status_code=400, detail="Une organisation avec ce nom existe déjà")

    org = Organization(name=org_in.name, description=org_in.description)
    db.add(org)
    db.commit()
    db.refresh(org)
    audit.log_action(db, current_user.id, "Création organisation", f"Organisation '{org.name}'")
    # Convert Organization object to OrganizationOut object for proper serialization
    serializable_org = OrganizationOut.model_validate(org)
    return response.success_response(serializable_org, "Organisation créée")

@router.put("/{org_id}", response_model=dict)
def update_organization(org_id: int, org_in: OrganizationUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    org = db.query(Organization).get(org_id)
    if not org:
        raise HTTPException(status_code=404, detail="Organisation non trouvée")
    if not permissions.has_permission(db, current_user, org.id, "organization:update"):
        raise HTTPException(status_code=403, detail="Permission insuffisante")

    # Check if another organization with the same name already exists
    existing_org = db.query(Organization).filter(Organization.name == org_in.name, Organization.id != org_id).first()
    if existing_org:
        raise HTTPException(status_code=400, detail="Une organisation avec ce nom existe déjà")

    org.name = org_in.name
    org.description = org_in.description
    db.commit()
    audit.log_action(db, current_user.id, "Mise à jour organisation", f"Organisation '{org.name}'")
    # Convert Organization object to OrganizationOut object for proper serialization
    serializable_org = OrganizationOut.model_validate(org)
    return response.success_response(serializable_org, "Organisation mise à jour")

@router.delete("/{org_id}", response_model=dict)
def delete_organization(org_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    org = db.query(Organization).get(org_id)
    if not org:
        raise HTTPException(status_code=404, detail="Organisation non trouvée")
    if not permissions.has_permission(db, current_user, org.id, "organization:delete"):
        raise HTTPException(status_code=403, detail="Permission insuffisante")
    db.delete(org)
    db.commit()
    audit.log_action(db, current_user.id, "Suppression organisation", f"Organisation '{org.name}'")
    return response.success_response(None, "Organisation supprimée")

# --- Utilisateurs ---

@router.post("/{org_id}/users/{user_id}", response_model=dict)
def add_user_to_organization(org_id: int, user_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    org = db.query(Organization).get(org_id)
    user = db.query(User).get(user_id)
    if not org or not user:
        raise HTTPException(status_code=404, detail="Organisation ou utilisateur introuvable")
    if not permissions.has_permission(db, current_user, org.id, "organization:update"):
        raise HTTPException(status_code=403, detail="Permission insuffisante")
    if user not in org.users:
        org.users.append(user)
        db.commit()
        audit.log_action(db, current_user.id, "Ajout utilisateur", f"Utilisateur {user.email} ajouté à l'organisation {org.name}")
    # Convert User objects to UserOut objects for proper serialization
    serializable_users = [UserOut.model_validate(user) for user in org.users]
    return response.success_response(serializable_users, "Utilisateur ajouté")

@router.delete("/{org_id}/users/{user_id}", response_model=dict)
def remove_user_from_organization(org_id: int, user_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    org = db.query(Organization).get(org_id)
    user = db.query(User).get(user_id)
    if not org or not user:
        raise HTTPException(status_code=404, detail="Organisation ou utilisateur introuvable")
    if not permissions.has_permission(db, current_user, org.id, "organization:update"):
        raise HTTPException(status_code=403, detail="Permission insuffisante")
    if user in org.users:
        org.users.remove(user)
        db.commit()
        audit.log_action(db, current_user.id, "Retrait utilisateur", f"Utilisateur {user.email} retiré de l'organisation {org.name}")
    # Convert User objects to UserOut objects for proper serialization
    serializable_users = [UserOut.model_validate(user) for user in org.users]
    return response.success_response(serializable_users, "Utilisateur retiré")

# --- Tags ---

@router.get("/{org_id}/tags", response_model=dict)
def list_organization_tags(org_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not permissions.has_permission(db, current_user, org_id, "tag:read"):
        raise HTTPException(status_code=403, detail="Permission insuffisante")
    tags = [tag for tag in tag_repo.list_tags(db) if any(
        p.organization_id == org_id for p in tag.policies
    ) or any(
        g.organization_id == org_id for g in tag.groups
    )]
    # Convert Tag objects to TagOut objects for proper serialization
    serializable_tags = [TagOut.model_validate(tag) for tag in tags]
    return response.success_response(serializable_tags, "Tags de l'organisation récupérés")

@router.post("/{org_id}/tags", response_model=dict)
def add_tag_to_organization(org_id: int, value: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not permissions.has_permission(db, current_user, org_id, "tag:create"):
        raise HTTPException(status_code=403, detail="Permission insuffisante")
    tag = tag_repo.get_tag_by_value(db, value) or tag_repo.create_tag(db, value)
    audit.log_action(db, current_user.id, "Ajout tag", f"Tag '{value}' ajouté pour l'organisation {org_id}")
    # Convert Tag object to TagOut object for proper serialization
    serializable_tag = TagOut.model_validate(tag)
    return response.success_response(serializable_tag, "Tag ajouté")

@router.delete("/{org_id}/tags/{tag_id}", response_model=dict)
def remove_tag_from_organization(org_id: int, tag_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    tag = tag_repo.get_tag(db, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag non trouvé")
    if not permissions.has_permission(db, current_user, org_id, "tag:delete"):
        raise HTTPException(status_code=403, detail="Permission insuffisante")
    tag_repo.delete_tag(db, tag)
    audit.log_action(db, current_user.id, "Suppression tag", f"Tag '{tag.value}' supprimé de l'organisation {org_id}")
    return response.success_response(None, "Tag supprimé")

# --- Policies ---

@router.get("/{org_id}/policies", response_model=dict)
def list_organization_policies(org_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    org = db.query(Organization).get(org_id)
    if not org:
        raise HTTPException(status_code=404, detail="Organisation non trouvée")
    if not permissions.has_permission(db, current_user, org.id, "policy:read"):
        raise HTTPException(status_code=403, detail="Permission insuffisante")
    # Convert Policy objects to PolicyOut objects for proper serialization
    serializable_policies = [PolicyOut.model_validate(policy) for policy in org.policies]
    return response.success_response(serializable_policies, "Policies récupérées")

# --- Groupes ---

@router.get("/{org_id}/groups", response_model=dict)
def list_organization_groups(org_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    org = db.query(Organization).get(org_id)
    if not org:
        raise HTTPException(status_code=404, detail="Organisation non trouvée")
    if not permissions.has_permission(db, current_user, org.id, "group:read"):
        raise HTTPException(status_code=403, detail="Permission insuffisante")
    # Convert Group objects to GroupOut objects for proper serialization
    serializable_groups = [GroupOut.model_validate(group) for group in org.groups]
    return response.success_response(serializable_groups, "Groupes récupérés")

@router.get("/{org_id}/environments", response_model=dict)
def list_organization_environments(org_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    org = db.query(Organization).get(org_id)
    if not org:
        raise HTTPException(status_code=404, detail="Organisation non trouvée")

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
    return response.success_response(serializable_environments, "Environnements de l'organisation récupérés")
