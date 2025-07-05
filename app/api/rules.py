from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database.session import SessionLocal
from ..repositories import rule_repo, policy_repo
from ..schema.rule import RuleCreate, RuleUpdate, RuleOut
from ..schema.auth import BaseResponse, EmptyData
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

@router.post("", response_model=BaseResponse[RuleOut], summary="Create a rule", description="Creates a new rule associated with a policy", responses={
    200: {"description": "Rule created successfully"},
    401: {"description": "Not authenticated"},
    403: {"description": "Insufficient permissions"},
    404: {"description": "Policy not found"}
})
def create_rule(rule_in: RuleCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    policy = policy_repo.get_policy(db, rule_in.policy_id)
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")
    if not permissions.has_permission(db, current_user, policy.organization_id, "rule:create"):
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    rule = rule_repo.create_rule(db, **rule_in.dict())
    audit.log_action(db, current_user.id, "Rule creation", f"Rule for policy {rule.policy_id} created")
    return response.success_response(rule, "Rule created")

@router.get("/{rule_id}", response_model=BaseResponse[RuleOut], summary="Rule details", description="Retrieves details of a specific rule", responses={
    200: {"description": "Rule retrieved successfully"},
    401: {"description": "Not authenticated"},
    403: {"description": "Insufficient permissions"},
    404: {"description": "Rule not found"}
})
def get_rule(rule_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    rule = rule_repo.get_rule(db, rule_id)
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")
    org_id = rule.policy.organization_id
    if not permissions.has_permission(db, current_user, org_id, "rule:read"):
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    return response.success_response(rule, "Rule retrieved")

@router.put("/{rule_id}", response_model=BaseResponse[RuleOut], summary="Update a rule", description="Updates an existing rule", responses={
    200: {"description": "Rule updated successfully"},
    401: {"description": "Not authenticated"},
    403: {"description": "Insufficient permissions"},
    404: {"description": "Rule not found"}
})
def update_rule(rule_id: int, rule_in: RuleUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    rule = rule_repo.get_rule(db, rule_id)
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")
    if not permissions.has_permission(db, current_user, rule.policy.organization_id, "rule:update"):
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    rule = rule_repo.update_rule(db, rule, **rule_in.dict(exclude_unset=True))
    audit.log_action(db, current_user.id, "Rule update", f"Rule {rule.id} updated")
    return response.success_response(rule, "Rule updated")

@router.delete("/{rule_id}", response_model=BaseResponse[EmptyData], summary="Delete a rule", description="Deletes an existing rule", responses={
    200: {"description": "Rule deleted successfully"},
    401: {"description": "Not authenticated"},
    403: {"description": "Insufficient permissions"},
    404: {"description": "Rule not found"}
})
def delete_rule(rule_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    rule = rule_repo.get_rule(db, rule_id)
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")
    if not permissions.has_permission(db, current_user, rule.policy.organization_id, "rule:delete"):
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    rule_repo.delete_rule(db, rule)
    audit.log_action(db, current_user.id, "Rule deletion", f"Rule {rule.id} deleted")
    return response.success_response(None, "Rule deleted")
