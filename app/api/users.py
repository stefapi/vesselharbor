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



@router.post("", response_model=dict,
    summary="Créer un utilisateur en mode libre",
    description="Crée un nouvel utilisateur en mode libre dans le système. Le premier utilisateur créé devient automatiquement superadmin.",
    responses={
         200: {"description": "Utilisateur créé avec succès"},
         400: {"description": "Email déjà enregistré"},
     }
)
def register_user(user_in: UserCreate, db: Session = Depends(get_db)):
    # TODO avoir un flag autorisant ou interdisant la création libre
    # TODO gérer la création libre avec confirmation d'Email (envoi de mail plus endpoint de validation)

    if user_repo.get_user_by_email(db, user_in.email):
        raise HTTPException(status_code=400, detail="Email déjà enregistré")
    is_superadmin = db.query(User).first() is None
    user = user_repo.create_user(db, email=user_in.email, username=user_in.username, first_name=user_in.first_name, last_name=user_in.last_name,password=user_in.password, is_superadmin=is_superadmin)
    audit.log_action(db, user.id, "Création utilisateur", f"Création de l'utilisateur {user.email}")
    return response.success_response(UserOut.model_validate(user), "Utilisateur créé avec succès")

@router.post("/{organization_id}", response_model=dict, summary="Créer un utilisateur",
             description="Crée un nouvel utilisateur dans le système. Il est rattaché à une Organization",
             responses={
    200: {"description": "Utilisateur créé avec succès"},
    400: {"description": "Email déjà enregistré"},
    401: {"description": "Non authentifié"},
    403: {"description": "Permission insuffisante"}
})
def create_user(organization_id: int, user_in: UserCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not permissions.has_permission(db, current_user, organization_id, "user:create"):
        raise HTTPException(status_code=403, detail="Permission insuffisante")
    if user_repo.get_user_by_email(db, user_in.email):
        raise HTTPException(status_code=400, detail="Email déjà enregistré")
    is_superadmin =  False
    user = user_repo.create_user(db, email=user_in.email, username=user_in.username, first_name=user_in.first_name,
                                 last_name=user_in.last_name, password=user_in.password, is_superadmin=is_superadmin)
    audit.log_action(db, user.id, "Création utilisateur", f"Création de l'utilisateur {user.email}")
    return response.success_response(UserOut.model_validate(user), "Utilisateur créé avec succès")

@router.get("", response_model=dict,
    summary="Lister les utilisateurs",
    description="Récupère la liste des utilisateurs avec pagination et filtrage optionnel par email.",
    responses={
    200: {"description": "Utilisateur créé avec succès"},
    401: {"description": "Non authentifié"},
    403: {"description": "Permission insuffisante"}
})
def list_users(current_user: User = Depends(get_current_user), db: Session = Depends(get_db), skip: int = 0, limit: int = 100, email: Optional[str] = None):
    if not permissions.has_permission(db, current_user, None, "user:list"):
        raise HTTPException(status_code=403, detail="Permission insuffisante")
    query = db.query(User)
    if email:
        query = query.filter(User.email.ilike(f"%{email}%"))
    users = query.offset(skip).limit(limit).all()
    return response.success_response([UserOut.model_validate(user) for user in users], "Liste des utilisateurs")

@router.get("/{user_id}", response_model=dict,
    summary="Obtenir un utilisateur",
    description="Récupère les informations détaillées d'un utilisateur spécifique par son ID.",
    responses={
        200: {"description": "Utilisateur créé avec succès"},
        401: {"description": "Non authentifié"},
        403: {"description": "Permission insuffisante"},
        404: {"description": "Utilisateur non trouvé"}
})
def get_user(user_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    user = user_repo.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    if current_user.id != user_id and  not permissions.has_permission(db, current_user, None, "user:read"):
        raise HTTPException(status_code=403, detail="Permission insuffisante")
    return response.success_response(UserOut.model_validate(user), "Utilisateur récupéré avec succès")

@router.put(
    "/{user_id}",
    response_model=dict,
    summary="Mettre à jour les informations d’un utilisateur",
    description="Modifie les informations personnelles d'un utilisateur existant (nom, prénom, email, username).",
    responses={
        200: {"description": "Utilisateur mis à jour avec succès"},
        400: {"description": "Mise à jour échouée"},
        401: {"description": "Non authentifié"},
        403: {"description": "Modification non autorisée"},
        404: {"description": "Utilisateur non trouvé"},
    }
)
def update_user(user_id: int, user_in: UserUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    user = user_repo.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    if current_user.id != user_id:
        if not permissions.has_permission(db, current_user, None, "user:update"):
            raise HTTPException(status_code=403, detail="Modification non autorisée")
    try:
        user.first_name = user_in.first_name
        user.last_name = user_in.last_name
        user.username = user_in.username
        user.email = user_in.email
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail="Mise à jour échouée")
    audit.log_action(db, current_user.id, "Mise à jour utilisateur", f"Mise à jour de l'utilisateur {user.email} (ID {user.id})")
    return response.success_response(UserOut.model_validate(user), "Utilisateur mis à jour")

@router.delete("/{user_id}", response_model=dict,
    summary="Supprimer un utilisateur",
    description="Supprime définitivement un utilisateur du système. Un utilisateur ne peut pas se supprimer lui-même, et le dernier superadmin ne peut pas être supprimé.",
    responses={
        200: {"description": "Utilisateur supprimé avec succès"},
        400: {"description": "Vous ne pouvez pas vous supprimer vous-même ou autre interdiction de suppression"},
        401: {"description": "Non authentifié"},
        403: {"description": "Modification non autorisée"},
        404: {"description": "Utilisateur non trouvé"},
    })
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

@router.put("/{user_id}/password", response_model=dict,
    summary="Changer le mot de passe",
    description="Permet à un utilisateur de changer son propre mot de passe ou à un administrateur de réinitialiser le mot de passe d'un autre utilisateur.",
    responses={
        200: {"description": "Mot de passe mis à jour avec succès"},
        400: {"description": "Mots de passe incorrects"},
        401: {"description": "Non authentifié"},
        403: {"description": "Modification non autorisée"},
        404: {"description": "Utilisateur non trouvé"},
    })
def change_password(user_id: int, cp: ChangePassword, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    user = user_repo.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    if permissions.has_permission(db, current_user, None, "user:update_password") and current_user.id != user_id:
        if cp.new_password and user.is_superadmin:
            user.hashed_password = security.get_password_hash(cp.new_password)
            db.commit()
            return response.success_response(None, "Mot de passe réinitialisé par admin")
        elif cp.send_email:
            token = security.create_password_reset_token(user.id)
            email.send_reset_email(user.email, token)
            return response.success_response(None, "Email de réinitialisation envoyé")
        elif user.is_superadmin:
            new_pass = secrets.token_urlsafe(20)
            user.hashed_password = security.get_password_hash(new_pass)
            db.commit()
            return response.success_response({"new_password": new_pass}, "Mot de passe généré")
        else:
            raise HTTPException(status_code=403, detail="Non autorisé")
    else:
        if current_user.id != user_id:
            raise HTTPException(status_code=403, detail="Non autorisé")
        if cp.old_password is None or cp.new_password is None:
            raise HTTPException(status_code=400, detail="Les mots de passe ne doivent pas être vide")
        if not security.verify_password(cp.old_password, user.hashed_password):
            raise HTTPException(status_code=400, detail="Mot de passe actuel incorrect")
        user.hashed_password = security.get_password_hash(cp.new_password)
        db.commit()
        return response.success_response(None, "Mot de passe mis à jour")

@router.put("/{user_id}/superadmin", response_model=dict,
    summary="Modifier statut superadmin",
    description="Permet à un superadmin de modifier le statut superadmin d'un autre utilisateur. Un superadmin ne peut pas modifier son propre statut, et le dernier superadmin ne peut pas être déclassé.",
    responses={
        200: {"description": "Utilisateur mis à jour avec succès"},
        400: {"description": "Impossible de retirer le dernier superadmin"},
        401: {"description": "Non authentifié"},
        403: {"description": "Modification non autorisée"},
        404: {"description": "Utilisateur non trouvé"},
    })
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
        # Check not really useful the third party superadmin is removed by the loggued superadmin
        other_super = db.query(User).filter(User.is_superadmin == True, User.id != user_id).first()
        if not other_super:
            raise HTTPException(status_code=400, detail="Impossible de retirer le dernier superadmin")
    user.is_superadmin = change.is_superadmin
    db.commit()
    audit.log_action(db, current_user.id, "Modification superadmin", f"Statut modifié pour {user.email}")
    return response.success_response(None, "Statut superadmin mis à jour")

@router.get("/{user_id}/groups", response_model=dict,
    summary="Groupes du user",
    description="Récupère la liste des groupes auxquels l'utilisateur appartient.",
    responses={
        200: {"description": "Groupes récupérés"},
        401: {"description": "Non authentifié"},
        403: {"description": "Lecture non autorisée"},
        404: {"description": "Utilisateur non trouvé"},
    })
def list_user_groups(user_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.id != user_id and not permissions.has_permission(db, current_user, None, "user:read_groups"):
        raise HTTPException(status_code=403, detail="Non autorisé")
    user = user_repo.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return response.success_response(user.groups, "Groupes récupérés")

@router.get("/{user_id}/policies", response_model=dict,
    summary="Policies du user",
    description="Récupère la liste des policies directement associées à l'utilisateur.",
    responses={
        200: {"description": "Policies récupérés"},
        401: {"description": "Non authentifié"},
        403: {"description": "Lecture non autorisée"},
        404: {"description": "Utilisateur non trouvé"},
    })
def list_user_policies(user_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.id != user_id and not permissions.has_permission(db, current_user, None, "user:read_policies"):
        raise HTTPException(status_code=403, detail="Non autorisé")
    user = user_repo.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return response.success_response(user.policies, "Policies récupérées")

@router.get("/{user_id}/organizations", response_model=dict,
    summary="Organisations du user",
    description="Récupère la liste des organisations auxquelles l'utilisateur est associé.",
    responses={
        200: {"description": "Organisations récupérés"},
        401: {"description": "Non authentifié"},
        403: {"description": "Lecture non autorisée"},
        404: {"description": "Utilisateur non trouvé"},
    })
def list_user_organizations(user_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.id != user_id and not permissions.has_permission(db, current_user, None, "user:read_organizations"):
        raise HTTPException(status_code=403, detail="Non autorisé")
    user = user_repo.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return response.success_response(user.organizations, "Organisations récupérées")

@router.get("/{user_id}/tags", response_model=dict,
    summary="Lister les tags d'un utilisateur",
    description="Récupère la liste des tags associés à un utilisateur spécifique.",
    responses={
        200: {"description": "Tags récupérés"},
        401: {"description": "Non authentifié"},
        403: {"description": "Lecture non autorisée"},
        404: {"description": "Utilisateur non trouvé"},
    })
def list_user_tags(user_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.id != user_id and not permissions.has_permission(db, current_user, None, "user:read_tags"):
        raise HTTPException(status_code=403, detail="Non autorisé")
    user = user_repo.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return response.success_response(user.tags, "Tags récupérés")

@router.post("/{user_id}/tags/{tag_id}", response_model=dict,
    summary="Associer un tag à un utilisateur",
    description="Ajoute un tag spécifique à un utilisateur pour le catégoriser ou lui attribuer des caractéristiques particulières.",
    responses={
        200: {"description": "Tag ajouté"},
        401: {"description": "Non authentifié"},
        403: {"description": "Ajout non autorisée"},
        404: {"description": "Utilisateur non trouvé"},
    })
def add_tag_to_user(user_id: int, tag_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.id != user_id and not permissions.has_permission(db, current_user, None, "user:update_tags"):
        raise HTTPException(status_code=403, detail="Non autorisé")
    user = user_repo.get_user(db, user_id)
    tag = tag_repo.get_tag(db, tag_id)
    if not user or not tag:
        raise HTTPException(status_code=404, detail="Utilisateur ou tag non trouvé")
    user_repo.add_tag_to_user(db, user, tag)
    return response.success_response(user, "Tag ajouté à l'utilisateur")

@router.delete("/{user_id}/tags/{tag_id}", response_model=dict,
    summary="Dissocier un tag d'un utilisateur",
    description="Retire un tag spécifique d'un utilisateur, supprimant ainsi la catégorisation ou les caractéristiques associées.",
    responses={
        200: {"description": "Tag retiré"},
        401: {"description": "Non authentifié"},
        403: {"description": "Suppression non autorisée"},
        404: {"description": "Utilisateur non trouvé"},
    })
def remove_tag_from_user(user_id: int, tag_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.id != user_id and not permissions.has_permission(db, current_user, None, "user:update_tags"):
        raise HTTPException(status_code=403, detail="Non autorisé")
    user = user_repo.get_user(db, user_id)
    tag = tag_repo.get_tag(db, tag_id)
    if not user or not tag:
        raise HTTPException(status_code=404, detail="Utilisateur ou tag non trouvé")
    user_repo.remove_tag_from_user(db, user, tag)
    return response.success_response(user, "Tag retiré de l'utilisateur")
