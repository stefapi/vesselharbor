from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from ..database.session import SessionLocal
from ..schema.user import UserCreate, UserOut, UserUpdate, ChangePassword, ChangeSuperadmin
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

@router.post("", response_model=dict, summary="Créer un utilisateur")
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    if user_repo.get_user_by_email(db, user_in.email):
        raise HTTPException(status_code=400, detail="Email déjà enregistré")
    is_superadmin = db.query(User).first() is None
    user = user_repo.create_user(db, email=user_in.email, password=user_in.password, is_superadmin=is_superadmin)
    audit.log_action(db, user.id, "Création utilisateur", f"Création de l'utilisateur {user.email}")
    return response.success_response(UserOut.model_validate(user), "Utilisateur créé avec succès")

@router.get("", response_model=dict, summary="Lister les utilisateurs")
def list_users(current_user: User = Depends(get_current_user), db: Session = Depends(get_db), skip: int = 0, limit: int = 100, email: Optional[str] = None):
    if not permissions.has_permission(db, current_user, None, "user:list"):
        raise HTTPException(status_code=403, detail="Non autorisé")
    query = db.query(User)
    if email:
        query = query.filter(User.email.ilike(f"%{email}%"))
    users = query.offset(skip).limit(limit).all()
    return response.success_response([UserOut.model_validate(user) for user in users], "Liste des utilisateurs")

@router.get("/{user_id}", response_model=UserOut, summary="Obtenir un utilisateur")
def get_user(user_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    user = user_repo.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    if current_user.id != user_id and  not permissions.has_permission(db, current_user, None, "user:read"):
        raise HTTPException(status_code=403, detail="Non autorisé")
    return user

@router.put(
    "/{user_id}",
    response_model=dict,
    summary="Mettre à jour les informations d’un utilisateur",
    responses={
        403: {"description": "Modification non autorisée"},
        404: {"description": "Utilisateur non trouvé"},
    }
)
def update_user(user_id: int, user_in: UserUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    user = user_repo.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    if current_user.id != user_id and not permissions.has_permission(db, current_user, None, "user:update"):
        raise HTTPException(status_code=403, detail="Modification non autorisée")
    user.first_name = user_in.first_name
    user.last_name = user_in.last_name
    user.username = user_in.username
    user.email = user_in.email
    db.commit()
    audit.log_action(db, current_user.id, "Mise à jour utilisateur", f"Mise à jour de l'utilisateur {user.email} (ID {user.id})")
    return response.success_response(user, "Utilisateur mis à jour")

@router.delete("/{user_id}", response_model=dict, summary="Supprimer un utilisateur")
def delete_user(user_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.id == user_id:
        raise HTTPException(status_code=400, detail="Vous ne pouvez pas vous supprimer vous-même")
    user = user_repo.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    if not permissions.has_permission(db, current_user, None, "user:delete"):
        raise HTTPException(status_code=403, detail="Non autorisé")
    if user.is_superadmin:
        other_super = db.query(User).filter(User.is_superadmin == True, User.id != user.id).first()
        if not other_super:
            raise HTTPException(status_code=400, detail="Impossible de supprimer le dernier superadmin")
    user_repo.delete_user(db, user)
    audit.log_action(db, current_user.id, "Suppression utilisateur", f"Suppression de l'utilisateur {user.email}")
    return response.success_response(None, "Utilisateur supprimé")

@router.put("/{user_id}/password", response_model=dict, summary="Changer le mot de passe")
def change_password(user_id: int, cp: ChangePassword, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    user = user_repo.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    if permissions.has_permission(db, current_user, None, "user:update_password") and current_user.id != user_id:
        if cp.new_password:
            user.hashed_password = security.get_password_hash(cp.new_password)
            db.commit()
            return response.success_response(None, "Mot de passe réinitialisé par admin")
        elif cp.send_email:
            token = security.create_password_reset_token(user.id)
            email.send_reset_email(user.email, token)
            return response.success_response(None, "Email de réinitialisation envoyé")
        else:
            new_pass = secrets.token_urlsafe(20)
            user.hashed_password = security.get_password_hash(new_pass)
            db.commit()
            return response.success_response({"new_password": new_pass}, "Mot de passe généré")
    else:
        if current_user.id != user_id:
            raise HTTPException(status_code=403, detail="Non autorisé")
        if not security.verify_password(cp.old_password, user.hashed_password):
            raise HTTPException(status_code=400, detail="Mot de passe actuel incorrect")
        user.hashed_password = security.get_password_hash(cp.new_password)
        db.commit()
        return response.success_response(None, "Mot de passe mis à jour")

@router.put("/{user_id}/superadmin", response_model=dict, summary="Modifier statut superadmin")
def change_superadmin(user_id: int, change: ChangeSuperadmin, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Only superadmins can change superadmin status
    if not current_user.is_superadmin:
        raise HTTPException(status_code=403, detail="Non autorisé")
    # Users can't change their own superadmin status
    if current_user.id == user_id:
        raise HTTPException(status_code=403, detail="Non autorisé")
    user = user_repo.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    if user.is_superadmin and not change.is_superadmin:
        other_super = db.query(User).filter(User.is_superadmin == True, User.id != user_id).first()
        if not other_super:
            raise HTTPException(status_code=400, detail="Impossible de retirer le dernier superadmin")
    user.is_superadmin = change.is_superadmin
    db.commit()
    audit.log_action(db, current_user.id, "Modification superadmin", f"Statut modifié pour {user.email}")
    return response.success_response(None, "Statut superadmin mis à jour")

@router.get("/{user_id}/assignments", response_model=dict, summary="Lister affectations")
def list_user_assignments(user_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.id != user_id and not permissions.has_permission(db, current_user, None, "user:read_assignments"):
        raise HTTPException(status_code=403, detail="Non autorisé")
    assignments = user_repo.list_assignments(db, user_id)
    return response.success_response(assignments, "Affectations récupérées")

@router.get("/{user_id}/groups", response_model=dict, summary="Groupes du user")
def list_user_groups(user_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.id != user_id and not permissions.has_permission(db, current_user, None, "user:read_groups"):
        raise HTTPException(status_code=403, detail="Non autorisé")
    user = user_repo.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return response.success_response(user.groups, "Groupes récupérés")

@router.get("/{user_id}/policies", response_model=dict, summary="Policies du user")
def list_user_policies(user_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.id != user_id and not permissions.has_permission(db, current_user, None, "user:read_policies"):
        raise HTTPException(status_code=403, detail="Non autorisé")
    user = user_repo.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return response.success_response(user.policies, "Policies récupérées")

@router.get("/{user_id}/organizations", response_model=dict, summary="Organisations du user")
def list_user_organizations(user_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.id != user_id and not permissions.has_permission(db, current_user, None, "user:read_organizations"):
        raise HTTPException(status_code=403, detail="Non autorisé")
    user = user_repo.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return response.success_response(user.organizations, "Organisations récupérées")

@router.get("/{user_id}/tags", response_model=dict, summary="Lister les tags d'un utilisateur")
def list_user_tags(user_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.id != user_id and not permissions.has_permission(db, current_user, None, "user:read_tags"):
        raise HTTPException(status_code=403, detail="Non autorisé")
    user = user_repo.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return response.success_response(user.tags, "Tags récupérés")

@router.post("/{user_id}/tags/{tag_id}", response_model=dict, summary="Associer un tag à un utilisateur")
def add_tag_to_user(user_id: int, tag_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.id != user_id and not permissions.has_permission(db, current_user, None, "user:update_tags"):
        raise HTTPException(status_code=403, detail="Non autorisé")
    user = user_repo.get_user(db, user_id)
    tag = tag_repo.get_tag(db, tag_id)
    if not user or not tag:
        raise HTTPException(status_code=404, detail="Utilisateur ou tag non trouvé")
    user_repo.add_tag_to_user(db, user, tag)
    return response.success_response(user, "Tag ajouté à l'utilisateur")

@router.delete("/{user_id}/tags/{tag_id}", response_model=dict, summary="Dissocier un tag d'un utilisateur")
def remove_tag_from_user(user_id: int, tag_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.id != user_id and not permissions.has_permission(db, current_user, None, "user:update_tags"):
        raise HTTPException(status_code=403, detail="Non autorisé")
    user = user_repo.get_user(db, user_id)
    tag = tag_repo.get_tag(db, tag_id)
    if not user or not tag:
        raise HTTPException(status_code=404, detail="Utilisateur ou tag non trouvé")
    user_repo.remove_tag_from_user(db, user, tag)
    return response.success_response(user, "Tag retiré de l'utilisateur")
