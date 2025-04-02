from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AuditLogOut(BaseModel):
    id: int
    user_id: Optional[int]
    action: str
    details: Optional[str]
    timestamp: datetime

    model_config = {
        "from_attributes": True
    }
