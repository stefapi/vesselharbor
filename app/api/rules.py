from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database.session import SessionLocal
from ..repositories import rule_repo, policy_repo
from ..schema.rule import RuleCreate, RuleUpdate, RuleOut
from ..api.users import get_current_user
from ..models.user import User
from ..helper import permissions, audit, response

router = APIRouter(prefix="/rules", tags=["rules"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/policy/{policy_id}", response_model=dict, summary="Lister les règles d'une politique", description="Récupère toutes les règles associées à une politique spécifique", responses={
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

@router.get("/{rule_id}", response_model=dict, summary="Détail d'une règle", description="Récupère les détails d'une règle spécifique", responses={
    200: {"description": "Règle récupérée avec succès"},
    401: {"description": "Non authentifié"},
    403: {"description": "Permission insuffisante"},
    404: {"description": "Règle non trouvée"}
})
def get_rule(rule_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    rule = rule_repo.get_rule(db, rule_id)
    if not rule:
        raise HTTPException(status_code=404, detail="Règle non trouvée")
    org_id = rule.policy.organization_id
    if not permissions.has_permission(db, current_user, org_id, "rule:read"):
        raise HTTPException(status_code=403, detail="Permission insuffisante")
    return response.success_response(rule, "Règle récupérée")

@router.post("", response_model=dict, summary="Créer une règle", description="Crée une nouvelle règle associée à une politique", responses={
    200: {"description": "Règle créée avec succès"},
    401: {"description": "Non authentifié"},
    403: {"description": "Permission insuffisante"},
    404: {"description": "Policy non trouvée"}
})
def create_rule(rule_in: RuleCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    policy = policy_repo.get_policy(db, rule_in.policy_id)
    if not policy:
        raise HTTPException(status_code=404, detail="Policy non trouvée")
    if not permissions.has_permission(db, current_user, policy.organization_id, "rule:create"):
        raise HTTPException(status_code=403, detail="Permission insuffisante")
    rule = rule_repo.create_rule(db, **rule_in.dict())
    audit.log_action(db, current_user.id, "Création règle", f"Règle pour policy {rule.policy_id} créée")
    return response.success_response(rule, "Règle créée")

@router.put("/{rule_id}", response_model=dict, summary="Mettre à jour une règle", description="Met à jour une règle existante", responses={
    200: {"description": "Règle mise à jour avec succès"},
    401: {"description": "Non authentifié"},
    403: {"description": "Permission insuffisante"},
    404: {"description": "Règle non trouvée"}
})
def update_rule(rule_id: int, rule_in: RuleUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    rule = rule_repo.get_rule(db, rule_id)
    if not rule:
        raise HTTPException(status_code=404, detail="Règle non trouvée")
    if not permissions.has_permission(db, current_user, rule.policy.organization_id, "rule:update"):
        raise HTTPException(status_code=403, detail="Permission insuffisante")
    rule = rule_repo.update_rule(db, rule, **rule_in.dict(exclude_unset=True))
    audit.log_action(db, current_user.id, "Mise à jour règle", f"Règle {rule.id} mise à jour")
    return response.success_response(rule, "Règle mise à jour")

@router.delete("/{rule_id}", response_model=dict, summary="Supprimer une règle", description="Supprime une règle existante", responses={
    200: {"description": "Règle supprimée avec succès"},
    401: {"description": "Non authentifié"},
    403: {"description": "Permission insuffisante"},
    404: {"description": "Règle non trouvée"}
})
def delete_rule(rule_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    rule = rule_repo.get_rule(db, rule_id)
    if not rule:
        raise HTTPException(status_code=404, detail="Règle non trouvée")
    if not permissions.has_permission(db, current_user, rule.policy.organization_id, "rule:delete"):
        raise HTTPException(status_code=403, detail="Permission insuffisante")
    rule_repo.delete_rule(db, rule)
    audit.log_action(db, current_user.id, "Suppression règle", f"Règle {rule.id} supprimée")
    return response.success_response(None, "Règle supprimée")
