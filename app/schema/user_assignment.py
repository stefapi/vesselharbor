from pydantic import BaseModel
from typing import Optional

class UserAssignmentOut(BaseModel):
    id: int
    user_id: int
    group_id: int
    element_id: Optional[int]

    model_config = {
        "from_attributes": True
    }
