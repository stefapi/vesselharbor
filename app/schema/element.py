from pydantic import BaseModel
from typing import Optional

class ElementCreate(BaseModel):
    name: str
    description: Optional[str] = None

class ElementUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]

class ElementOut(BaseModel):
    id: int
    name: str
    description: Optional[str]

    model_config = {
        "from_attributes": True
    }
