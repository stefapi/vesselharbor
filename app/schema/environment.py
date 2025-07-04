# app/schema/environment.py

from __future__ import annotations

from pydantic import BaseModel, Field
from typing import Optional, List, TYPE_CHECKING

from .element import ElementOut
from .rule import RuleOut
from .user import UserOut
from .group import GroupOut
from .tag import TagOut
from .physical_host import PhysicalHostOut

if TYPE_CHECKING:
    from .organization import OrganizationBase, OrganizationOut

class EnvironmentCreate(BaseModel):
    name: str
    description: Optional[str] = None
    organization_id: int

class EnvironmentBase(BaseModel):
    id: int
    name: str
    description: Optional[str]
    organization_id: int

class EnvironmentOut(EnvironmentBase):

    # Ajouts relationnels
    organization: Optional['OrganizationOut'] = None
    elements: List[ElementOut] = Field(default_factory=list)
    rules: List[RuleOut] = Field(default_factory=list)
    users: List[UserOut] = Field(default_factory=list)
    groups_with_access: List[GroupOut] = Field(default_factory=list)
    tags: List[TagOut] = Field(default_factory=list)
    physical_hosts: List[PhysicalHostOut] = Field(default_factory=list)

    model_config = {
        "from_attributes": True
    }
