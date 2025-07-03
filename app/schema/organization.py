# app/schema/organization.py
from pydantic import BaseModel, Field
from typing import Optional, List

from .user import UserOut
from .environment import EnvironmentOut
from .group import GroupOut
from .policy import PolicyOut

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
    environments: List[EnvironmentOut] = []
    groups: List[GroupOut] = []
    policies: List[PolicyOut] = []

    model_config = {"from_attributes": True}
