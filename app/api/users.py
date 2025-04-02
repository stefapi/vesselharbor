from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import List, Optional

from ..schema.user import UserCreate, UserOut, ChangePassword, ChangeSuperadmin
from ..schema.auth import Token
from ..schema.password_reset import PasswordResetRequest, PasswordReset
from ..schema.group import GroupOut
from ..models.user import User
from ..models.user_assignment import UserAssignment  # Nouvelle table d'affectation
from ..database.session import SessionLocal
from ..helper import security, audit, email, response
from ..repositories import user_repo
from ..core import auth

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    try:
        payload = auth.decode_access_token(token)
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalide")
        user = user_repo.get_user(db, int(user_id))
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Utilisateur non trouvé")
        return user
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Identifiants invalides")

@router.post(
    "/users",
    response_model=dict,
    summary="Créer un utilisateur",
    description="Crée un nouvel utilisateur. Le premier utilisateur créé devient superadmin.",
    responses={
        400: {"description": "Email déjà enregistré"},
        500: {"description": "Erreur interne du serveur"}
    }
)
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    if user_repo.get_user_by_email(db, user_in.email):
        raise HTTPException(status_code=400, detail="Email déjà enregistré")
    is_superadmin = db.query(User).first() is None
    user = user_repo.create_user(db, email=user_in.email, password=user_in.password, is_superadmin=is_superadmin)
    audit.log_action(db, user.id, "Création utilisateur", f"Création de l'utilisateur {user.email}")
    return response.success_response(UserOut.model_validate(user), "Utilisateur créé avec succès")

@router.post(
    "/login",
    response_model=dict,
    summary="Authentifier un utilisateur",
    description="Authentifie un utilisateur et retourne un token d'accès.",
    responses={
        400: {"description": "Email ou mot de passe incorrect"},
        401: {"description": "Non autorisé"}
    }
)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = user_repo.get_user_by_email(db, form_data.username)
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Email ou mot de passe incorrect")
    access_token = auth.create_access_token(data={"sub": str(user.id)})
    audit.log_action(db, user.id, "Login", "Connexion réussie")
    return {"access_token": access_token, "token_type": "bearer"}

@router.delete(
    "/users/{user_id}",
    response_model=dict,
    summary="Supprimer un utilisateur",
    description="Supprime un utilisateur (l'utilisateur ne peut se supprimer lui-même).",
    responses={
        400: {"description": "Suppression interdite (par ex. dernier superadmin ou seul admin d'un groupe)"},
        404: {"description": "Utilisateur non trouvé"}
    }
)
def delete_user(user_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.id == user_id:
        raise HTTPException(status_code=400, detail="Vous ne pouvez pas vous supprimer vous-même")
    user = user_repo.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    if user.is_superadmin:
        other_super = db.query(User).filter(User.is_superadmin == True, User.id != user.id).first()
        if not other_super:
            raise HTTPException(status_code=400, detail="Impossible de supprimer le dernier superadmin")
    # Vérifier que l'utilisateur n'est pas le seul admin dans l'un de ses groupes
    for assignment in user.user_assignments:
        group = assignment.group
        if group:
            is_admin = any(func.name == "admin" for func in group.functions)
            if is_admin:
                other_admin = db.query(UserAssignment).filter(
                    UserAssignment.group_id == group.id,
                    UserAssignment.user_id != user.id
                ).first()
                if not other_admin:
                    raise HTTPException(status_code=400, detail=f"Impossible de supprimer l'utilisateur ; il est le seul admin dans le groupe {group.name}")
    user_repo.delete_user(db, user)
    audit.log_action(db, current_user.id, "Suppression utilisateur", f"Suppression de l'utilisateur {user.email}")
    return response.success_response(None, "Utilisateur supprimé")

@router.put(
    "/users/{user_id}/password",
    response_model=dict,
    summary="Changer le mot de passe",
    description="Permet à un utilisateur de changer son propre mot de passe.",
    responses={
        400: {"description": "Informations d'identification invalides"},
        403: {"description": "Modification interdite"}
    }
)
def change_password(user_id: int, cp: ChangePassword, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Vous ne pouvez changer que votre propre mot de passe")
    user = user_repo.get_user(db, user_id)
    if not user or not security.verify_password(cp.old_password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Informations d'identification invalides")
    user.hashed_password = security.get_password_hash(cp.new_password)
    db.commit()
    audit.log_action(db, user.id, "Changement de mot de passe", "Modification par l'utilisateur")
    return response.success_response(None, "Mot de passe mis à jour")

@router.put(
    "/users/{user_id}/superadmin",
    response_model=dict,
    summary="Modifier le statut superadmin",
    description="Permet à un superadmin de modifier le statut superadmin d'un autre utilisateur.",
    responses={
        400: {"description": "Modification interdite"},
        403: {"description": "Non autorisé"},
        404: {"description": "Utilisateur non trouvé"}
    }
)
def change_superadmin(user_id: int, change: ChangeSuperadmin, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not current_user.is_superadmin:
        raise HTTPException(status_code=403, detail="Non autorisé")
    if current_user.id == user_id:
        raise HTTPException(status_code=400, detail="Vous ne pouvez pas modifier votre propre statut superadmin")
    user = user_repo.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    if user.is_superadmin and not change.is_superadmin:
        other_super = db.query(User).filter(User.is_superadmin == True, User.id != user_id).first()
        if not other_super:
            raise HTTPException(status_code=400, detail="Impossible de retirer le statut superadmin ; l'utilisateur est le seul superadmin")
    user.is_superadmin = change.is_superadmin
    db.commit()
    audit.log_action(db, current_user.id, "Modification superadmin", f"Modification du statut de {user.email} à {change.is_superadmin}")
    return response.success_response(None, "Statut superadmin mis à jour")

@router.get(
    "/users",
    response_model=dict,
    summary="Lister les utilisateurs",
    description="Liste tous les utilisateurs (accessible uniquement par superadmin) avec pagination et filtrage par email.",
    responses={
        403: {"description": "Non autorisé"}
    }
)
def list_users(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    email: Optional[str] = None
):
    if not current_user.is_superadmin:
        raise HTTPException(status_code=403, detail="Non autorisé")
    query = db.query(User)
    if email:
        query = query.filter(User.email.ilike(f"%{email}%"))
    users = query.offset(skip).limit(limit).all()
    return response.success_response([UserOut.model_validate(user) for user in users], "Liste des utilisateurs")

@router.get(
    "/users/{user_id}/assignments",
    response_model=dict,
    summary="Lister les affectations d'un utilisateur",
    description="Liste les affectations (UserAssignment) d'un utilisateur.",
    responses={
        403: {"description": "Non autorisé"}
    }
)
def list_user_assignments(user_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.id != user_id and not current_user.is_superadmin:
        raise HTTPException(status_code=403, detail="Non autorisé")
    assignments = db.query(UserAssignment).filter(UserAssignment.user_id == user_id).all()
    return response.success_response(assignments, "Affectations récupérées")

@router.get(
    "/users/{user_id}/groups",
    response_model=dict,
    summary="Lister les groupes d'un utilisateur",
    description="Renvoie la liste des groupes auxquels un utilisateur est affecté via ses affectations.",
    responses={
        403: {"description": "Non autorisé"},
        404: {"description": "Utilisateur non trouvé"}
    }
)
def list_user_groups(user_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.id != user_id and not current_user.is_superadmin:
        raise HTTPException(status_code=403, detail="Non autorisé")
    user = user_repo.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return response.success_response(user.groups, "Liste des groupes récupérée")

@router.post(
    "/users/reset_password_request",
    response_model=dict,
    summary="Demander une réinitialisation de mot de passe",
    description="Envoie un lien de réinitialisation par email si l'email est enregistré.",
    responses={
        200: {"description": "Lien de réinitialisation envoyé (même si l'email n'existe pas pour sécurité)"}
    }
)
def reset_password_request(reset_req: PasswordResetRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    user = user_repo.get_user_by_email(db, reset_req.email)
    if not user:
        return response.success_response(None, "Si cet email est enregistré, vous recevrez un lien de réinitialisation.")
    token = auth.create_access_token(data={"sub": str(user.id), "token_type": "password_reset"})
    reset_link = f"https://votre-app.com/reset_password?token={token}"
    background_tasks.add_task(email.send_reset_email, user.email, reset_link)
    audit.log_action(db, user.id, "Réinitialisation mot de passe", "Lien de réinitialisation envoyé par email")
    return response.success_response(None, "Si cet email est enregistré, vous recevrez un lien de réinitialisation.")

@router.post(
    "/users/reset_password",
    response_model=dict,
    summary="Réinitialiser le mot de passe",
    description="Réinitialise le mot de passe via le token reçu par email.",
    responses={
        400: {"description": "Token invalide ou expiré"},
        404: {"description": "Utilisateur non trouvé"}
    }
)
def reset_password(reset: PasswordReset, db: Session = Depends(get_db)):
    try:
        payload = auth.decode_access_token(reset.token)
    except Exception:
        raise HTTPException(status_code=400, detail="Token invalide ou expiré")
    if payload.get("token_type") != "password_reset":
        raise HTTPException(status_code=400, detail="Token incorrect")
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=400, detail="Token invalide")
    user = user_repo.get_user(db, int(user_id))
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    user.hashed_password = security.get_password_hash(reset.new_password)
    db.commit()
    audit.log_action(db, user.id, "Réinitialisation mot de passe", "Mot de passe réinitialisé via lien email")
    return response.success_response(None, "Mot de passe réinitialisé avec succès")
