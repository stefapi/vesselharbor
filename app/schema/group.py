# app/schema/group.py
from pydantic import BaseModel
from typing import List, Optional
from .tag import TagOut

class GroupCreate(BaseModel):
    name: str
    description: Optional[str] = None
    organization_id: int

class GroupUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class GroupOut(BaseModel):
    id: int
    name: str
    description: Optional[str]
    tags: List[TagOut] = []

    model_config = {
        "from_attributes": True
    }
