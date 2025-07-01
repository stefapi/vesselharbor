from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

from ..database.session import SessionLocal
from ..models.user import User
from ..repositories import policy_repo, user_repo, group_repo, tag_repo, rule_repo
from ..schema.policy import PolicyCreate, PolicyUpdate
from ..api.users import get_current_user
from ..helper import permissions, audit, response

router = APIRouter(prefix="/policies", tags=["policies"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("", response_model=dict,
    summary="Lister les policies",
    description="Récupère la liste des policies pour une organisation donnée avec pagination.",
    responses={
    200: {"description": "Policies récupérées avec succès"},
    401: {"description": "Non authentifié"},
    403: {"description": "Permission insuffisante"}
})
def list_policies(
    organization_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not permissions.has_permission(db, current_user, organization_id, "policy:read"):
        raise HTTPException(status_code=403, detail="Permission insuffisante")
    policies = policy_repo.list_policies(db, organization_id, skip, limit)
    return response.success_response(policies, "Policies récupérées")

@router.get("/{policy_id}", response_model=dict,
    summary="Obtenir une policy",
    description="Récupère les détails d'une policy spécifique par son ID.",
    responses={
    200: {"description": "Policy récupérée avec succès"},
    401: {"description": "Non authentifié"},
    403: {"description": "Permission insuffisante"},
    404: {"description": "Policy non trouvée"}
})
def get_policy(policy_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    policy = policy_repo.get_policy(db, policy_id)
    if not policy:
        raise HTTPException(status_code=404, detail="Policy non trouvée")
    if not permissions.has_permission(db, current_user, policy.organization_id, "policy:read"):
        raise HTTPException(status_code=403, detail="Permission insuffisante")
    return response.success_response(policy, "Policy récupérée")

@router.post("", response_model=dict,
    summary="Créer une policy",
    description="Crée une nouvelle policy dans l'organisation spécifiée.",
    responses={
    200: {"description": "Policy créée avec succès"},
    401: {"description": "Non authentifié"},
    403: {"description": "Permission insuffisante"}
})
def create_policy(policy_in: PolicyCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not permissions.has_permission(db, current_user, policy_in.organization_id, "policy:create"):
        raise HTTPException(status_code=403, detail="Permission insuffisante")
    policy = policy_repo.create_policy(db, policy_in)
    audit.log_action(db, current_user.id, "Création policy", f"Policy '{policy.name}' créée")
    return response.success_response(policy, "Policy créée")

@router.put("/{policy_id}", response_model=dict,
    summary="Mettre à jour une policy",
    description="Modifie les informations d'une policy existante.",
    responses={
    200: {"description": "Policy mise à jour avec succès"},
    401: {"description": "Non authentifié"},
    403: {"description": "Permission insuffisante"},
    404: {"description": "Policy non trouvée"}
})
def update_policy(policy_id: int, policy_in: PolicyUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    policy = policy_repo.get_policy(db, policy_id)
    if not policy:
        raise HTTPException(status_code=404, detail="Policy non trouvée")
    if not permissions.has_permission(db, current_user, policy.organization_id, "policy:update"):
        raise HTTPException(status_code=403, detail="Permission insuffisante")
    policy = policy_repo.update_policy(db, policy, policy_in)
    audit.log_action(db, current_user.id, "Mise à jour policy", f"Policy '{policy.name}' mise à jour")
    return response.success_response(policy, "Policy mise à jour")

@router.delete("/{policy_id}", response_model=dict,
    summary="Supprimer une policy",
    description="Supprime définitivement une policy existante.",
    responses={
    200: {"description": "Policy supprimée avec succès"},
    401: {"description": "Non authentifié"},
    403: {"description": "Permission insuffisante"},
    404: {"description": "Policy non trouvée"}
})
def delete_policy(policy_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    policy = policy_repo.get_policy(db, policy_id)
    if not policy:
        raise HTTPException(status_code=404, detail="Policy non trouvée")
    if not permissions.has_permission(db, current_user, policy.organization_id, "policy:delete"):
        raise HTTPException(status_code=403, detail="Permission insuffisante")
    policy_repo.delete_policy(db, policy)
    audit.log_action(db, current_user.id, "Suppression policy", f"Policy '{policy.name}' supprimée")
    return response.success_response(None, "Policy supprimée")

# Gestion des relations : users, groups, tags

@router.get("/{policy_id}/users", response_model=dict,
    summary="Lister les utilisateurs d'une policy",
    description="Récupère la liste de tous les utilisateurs associés à une policy spécifique.",
    responses={
    200: {"description": "Liste des utilisateurs de la policy récupérée avec succès"},
    401: {"description": "Non authentifié"},
    403: {"description": "Permission insuffisante"},
    404: {"description": "Policy non trouvée"}
})
def list_policy_users(policy_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    policy = policy_repo.get_policy(db, policy_id)
    if not policy:
        raise HTTPException(status_code=404, detail="Policy non trouvée")
    if not permissions.has_permission(db, current_user, policy.organization_id, "policy:read"):
        raise HTTPException(status_code=403, detail="Permission insuffisante")
    return response.success_response(policy.users, "Utilisateurs de la policy récupérés")

@router.post("/{policy_id}/users/{user_id}", response_model=dict,
    summary="Ajouter un utilisateur à une policy",
    description="Associe un utilisateur spécifique à une policy pour lui accorder les permissions définies.",
    responses={
    200: {"description": "Utilisateur ajouté à la policy avec succès"},
    401: {"description": "Non authentifié"},
    403: {"description": "Permission insuffisante"},
    404: {"description": "Policy ou user non trouvé"}
})
def add_user(policy_id: int, user_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    policy = policy_repo.get_policy(db, policy_id)
    user = user_repo.get_user(db, user_id)
    if not policy or not user:
        raise HTTPException(status_code=404, detail="Policy ou user non trouvé")
    if not permissions.has_permission(db, current_user, policy.organization_id, "policy:update"):
        raise HTTPException(status_code=403, detail="Permission insuffisante")
    policy_repo.add_user(db, policy, user)
    return response.success_response(None, "Utilisateur ajouté à la policy")

@router.delete("/{policy_id}/users/{user_id}", response_model=dict,
    summary="Retirer un utilisateur d'une policy",
    description="Dissocie un utilisateur d'une policy, lui retirant ainsi les permissions associées.",
    responses={
    200: {"description": "Utilisateur retiré de la policy avec succès"},
    401: {"description": "Non authentifié"},
    403: {"description": "Permission insuffisante"},
    404: {"description": "Policy ou user non trouvé"}
})
def remove_user(policy_id: int, user_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    policy = policy_repo.get_policy(db, policy_id)
    user = user_repo.get_user(db, user_id)
    if not policy or not user:
        raise HTTPException(status_code=404, detail="Policy ou user non trouvé")
    if not permissions.has_permission(db, current_user, policy.organization_id, "policy:update"):
        raise HTTPException(status_code=403, detail="Permission insuffisante")
    policy_repo.remove_user(db, policy, user)
    return response.success_response(None, "Utilisateur retiré de la policy")

@router.get("/{policy_id}/groups", response_model=dict,
    summary="Lister les groupes d'une policy",
    description="Récupère la liste de tous les groupes associés à une policy spécifique.",
    responses={
    200: {"description": "Liste des groupes de la policy récupérée avec succès"},
    401: {"description": "Non authentifié"},
    403: {"description": "Permission insuffisante"},
    404: {"description": "Policy non trouvée"}
})
def list_policy_groups(policy_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    policy = policy_repo.get_policy(db, policy_id)
    if not policy:
        raise HTTPException(status_code=404, detail="Policy non trouvée")
    if not permissions.has_permission(db, current_user, policy.organization_id, "policy:read"):
        raise HTTPException(status_code=403, detail="Permission insuffisante")
    return response.success_response(policy.groups, "Groupes de la policy récupérés")

@router.post("/{policy_id}/groups/{group_id}", response_model=dict,
    summary="Ajouter un groupe à une policy",
    description="Associe un groupe à une policy, accordant ainsi les permissions définies à tous les membres du groupe.",
    responses={
    200: {"description": "Groupe ajouté à la policy avec succès"},
    401: {"description": "Non authentifié"},
    403: {"description": "Permission insuffisante"},
    404: {"description": "Policy ou groupe non trouvé"}
})
def add_group(policy_id: int, group_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    policy = policy_repo.get_policy(db, policy_id)
    group = group_repo.get_group(db, group_id)
    if not policy or not group:
        raise HTTPException(status_code=404, detail="Policy ou groupe non trouvé")
    if not permissions.has_permission(db, current_user, policy.organization_id, "policy:update"):
        raise HTTPException(status_code=403, detail="Permission insuffisante")
    policy_repo.add_group(db, policy, group)
    return response.success_response(None, "Groupe ajouté à la policy")

@router.get("/{policy_id}/rules", response_model=dict, summary="Lister les règles d'une politique", description="Récupère toutes les règles associées à une politique spécifique", responses={
    200: {"description": "Règles récupérées avec succès"},
    401: {"description": "Non authentifié"},
    403: {"description": "Permission insuffisante"},
    404: {"description": "Policy non trouvée"}
})
def list_rules(policy_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    policy = policy_repo.get_policy(db, policy_id)
    if not policy:
        raise HTTPException(status_code=404, detail="Policy non trouvée")
    if not permissions.has_permission(db, current_user, policy.organization_id, "rule:read"):
        raise HTTPException(status_code=403, detail="Permission insuffisante")
    rules = rule_repo.list_rules_for_policy(db, policy_id)
    return response.success_response(rules, "Règles récupérées")


@router.delete("/{policy_id}/groups/{group_id}", response_model=dict,
    summary="Retirer un groupe d'une policy",
    description="Dissocie un groupe d'une policy, retirant ainsi les permissions associées à tous les membres du groupe.",
    responses={
    200: {"description": "Groupe retiré de la policy avec succès"},
    401: {"description": "Non authentifié"},
    403: {"description": "Permission insuffisante"},
    404: {"description": "Policy ou groupe non trouvé"}
})
def remove_group(policy_id: int, group_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    policy = policy_repo.get_policy(db, policy_id)
    group = group_repo.get_group(db, group_id)
    if not policy or not group:
        raise HTTPException(status_code=404, detail="Policy ou groupe non trouvé")
    if not permissions.has_permission(db, current_user, policy.organization_id, "policy:update"):
        raise HTTPException(status_code=403, detail="Permission insuffisante")
    policy_repo.remove_group(db, policy, group)
    return response.success_response(None, "Groupe retiré de la policy")

@router.post("/{policy_id}/tags/{tag_id}", response_model=dict,
    summary="Ajouter un tag à une policy",
    description="Associe un tag à une policy, permettant d'appliquer la policy à tous les éléments portant ce tag.",
    responses={
    200: {"description": "Tag ajouté à la policy avec succès"},
    401: {"description": "Non authentifié"},
    403: {"description": "Permission insuffisante"},
    404: {"description": "Policy ou tag non trouvé"}
})
def add_tag(policy_id: int, tag_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    policy = policy_repo.get_policy(db, policy_id)
    tag = tag_repo.get_tag(db, tag_id)
    if not policy or not tag:
        raise HTTPException(status_code=404, detail="Policy ou tag non trouvé")
    if not permissions.has_permission(db, current_user, policy.organization_id, "policy:update"):
        raise HTTPException(status_code=403, detail="Permission insuffisante")
    policy_repo.add_tag(db, policy, tag)
    return response.success_response(None, "Tag ajouté à la policy")

@router.delete("/{policy_id}/tags/{tag_id}", response_model=dict,
    summary="Retirer un tag d'une policy",
    description="Dissocie un tag d'une policy, retirant ainsi l'application de la policy aux éléments portant ce tag.",
    responses={
    200: {"description": "Tag retiré de la policy avec succès"},
    401: {"description": "Non authentifié"},
    403: {"description": "Permission insuffisante"},
    404: {"description": "Policy ou tag non trouvé"}
})
def remove_tag(policy_id: int, tag_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    policy = policy_repo.get_policy(db, policy_id)
    tag = tag_repo.get_tag(db, tag_id)
    if not policy or not tag:
        raise HTTPException(status_code=404, detail="Policy ou tag non trouvé")
    if not permissions.has_permission(db, current_user, policy.organization_id, "policy:update"):
        raise HTTPException(status_code=403, detail="Permission insuffisante")
    policy_repo.remove_tag(db, policy, tag)
    return response.success_response(None, "Tag retiré de la policy")

