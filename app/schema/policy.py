from pydantic import BaseModel
from typing import Optional, List
from .tag import TagOut
from .user import UserOut
from .group import GroupOut


class PolicyCreate(BaseModel):
    name: str
    description: Optional[str] = None
    access_schedule: Optional[str] = None
    organization_id: int


class PolicyUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    access_schedule: Optional[str] = None


class PolicyOut(BaseModel):
    id: int
    name: str
    description: Optional[str]
    access_schedule: Optional[str]
    organization_id: int
    tags: List[TagOut] = []
    users: List[UserOut] = []
    groups: List[GroupOut] = []

    model_config = {"from_attributes": True}
