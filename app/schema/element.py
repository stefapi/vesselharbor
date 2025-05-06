# app/schema/element.py

from pydantic import BaseModel
from typing import Optional, List, TYPE_CHECKING
from .rule import RuleOut  # si on veut les inclure
from .user import UserOut
from .group import GroupOut
if TYPE_CHECKING:
    from .environment import EnvironmentBase

class ElementCreate(BaseModel):
    name: str
    description: Optional[str] = None
    environment_id: int

class ElementUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]

class ElementBase(BaseModel):
    id: int
    name: str
    description: Optional[str]
    environment_id: int

class ElementOut(ElementBase):

    # Ajouts utiles
    environment: Optional['EnvironmentBase'] = None
    rules: Optional[List[RuleOut]] = []
    users: Optional[List[UserOut]] = []
    groups: Optional[List[GroupOut]] = []

    model_config = {
        "from_attributes": True
    }
