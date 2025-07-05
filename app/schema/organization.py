# app/schema/organization.py

from __future__ import annotations

from pydantic import BaseModel, Field
from typing import Optional, List, TYPE_CHECKING

from .user import UserOut
from .group import GroupOut
from .policy import PolicyOut

if TYPE_CHECKING:
    from .environment import EnvironmentOut

class OrganizationBase(BaseModel):
    name: str = Field(..., max_length=80)
    description: Optional[str] = Field(None, max_length=1024)

class OrganizationCreate(OrganizationBase):
    pass

class OrganizationUpdate(OrganizationBase):
    pass

class OrganizationOut(OrganizationBase):
    id: int
    users: List[UserOut] = []
    environments: List['EnvironmentOut'] = []
    groups: List[GroupOut] = []
    policies: List[PolicyOut] = []

    model_config = {"from_attributes": True}
