from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from ..schema.audit_log import AuditLogOut
from ..models.audit_log import AuditLog
from ..database.session import SessionLocal
from ..api.users import get_current_user
from ..models.user import User
from ..helper import response

router = APIRouter(prefix="/audit-logs", tags=["audit_logs"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get(
    "/",
    response_model=dict,
    summary="Lister les logs d'audit",
    description="Liste les logs d'audit avec pagination et filtrage par action et user_id (accessible uniquement par superadmin).",
    responses={
        200: {"description": "Logs d'audit récupérés avec succès"},
        401: {"description": "Non authentifié"},
        403: {"description": "Non autorisé"}
    }
)
def list_audit_logs(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    action: Optional[str] = None,
    user_id: Optional[int] = None
):
    if not current_user.is_superadmin:
        raise HTTPException(status_code=403, detail="Non autorisé")
    query = db.query(AuditLog)
    if action:
        query = query.filter(AuditLog.action.ilike(f"%{action}%"))
    if user_id:
        query = query.filter(AuditLog.user_id == user_id)
    logs = query.order_by(AuditLog.timestamp.desc()).offset(skip).limit(limit).all()
    return response.success_response(logs, "Logs d'audit récupérés")
