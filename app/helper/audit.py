from ..repositories import audit_log_repo

def log_action(db, user_id: int, action: str, details: str = None):
    audit_log_repo.create_audit_log(db, user_id, action, details)
