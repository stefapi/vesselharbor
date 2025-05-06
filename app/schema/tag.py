# app/schema/tag.py
from pydantic import BaseModel, Field
from typing import List, Optional

class TagCreate(BaseModel):
    value: str = Field(..., max_length=80)
    organization_id: int

class TagOut(BaseModel):
    id: int
    value: str

    model_config = {"from_attributes": True}

# Optionnel si tu veux un tag + ses relations
class TagWithRelationsOut(TagOut):
    users: Optional[List["UserOut"]] = []
    groups: Optional[List["GroupOut"]] = []
    policies: Optional[List["PolicyOut"]] = []

    model_config = {"from_attributes": True}

# Pour éviter l'erreur de référence circulaire :

from .group import GroupOut
