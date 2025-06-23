from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database.session import SessionLocal
from ..models.user import User
from ..repositories import user_repo, group_repo
from ..api.auth import get_current_user
from ..helper import audit, response

router = APIRouter(prefix="/users", tags=["user_groups"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/{user_id}/groups", response_model=dict, summary="Ajouter un utilisateur à un groupe")
def add_user_to_group(user_id: int, data: dict, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not current_user.is_superadmin:
        raise HTTPException(status_code=403, detail="Non autorisé")

    user = user_repo.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

    group_id = data.get("group_id")
    if not group_id:
        raise HTTPException(status_code=400, detail="ID de groupe requis")

    group = group_repo.get_group(db, group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Groupe non trouvé")

    # Vérifier si l'utilisateur est déjà dans le groupe
    if user in group.users:
        return response.success_response(None, "L'utilisateur est déjà dans ce groupe")

    # Ajouter l'utilisateur au groupe
    group.users.append(user)
    db.commit()

    audit.log_action(db, current_user.id, "Ajout à un groupe", f"Utilisateur {user.email} ajouté au groupe {group.name}")
    return response.success_response(None, "Utilisateur ajouté au groupe")

@router.delete("/{user_id}/groups/{group_id}", response_model=dict, summary="Retirer un utilisateur d'un groupe")
def remove_user_from_group(user_id: int, group_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not current_user.is_superadmin:
        raise HTTPException(status_code=403, detail="Non autorisé")

    user = user_repo.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

    group = group_repo.get_group(db, group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Groupe non trouvé")

    # Vérifier si l'utilisateur est dans le groupe
    if user not in group.users:
        return response.success_response(None, "L'utilisateur n'est pas dans ce groupe")

    # Retirer l'utilisateur du groupe
    group.users.remove(user)
    db.commit()

    audit.log_action(db, current_user.id, "Retrait d'un groupe", f"Utilisateur {user.email} retiré du groupe {group.name}")
    return response.success_response(None, "Utilisateur retiré du groupe")
