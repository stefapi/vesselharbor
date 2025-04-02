from sqlalchemy.orm import Session
from ..models.audit_log import AuditLog

def create_audit_log(db: Session, user_id: int, action: str, details: str = None) -> AuditLog:
    log = AuditLog(user_id=user_id, action=action, details=details)
    db.add(log)
    db.commit()
    db.refresh(log)
    return log
