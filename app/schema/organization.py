# app/schema/organization.py
from pydantic import BaseModel, Field
from typing import Optional

class OrganizationBase(BaseModel):
    name: str = Field(..., max_length=80)
    description: Optional[str] = Field(None, max_length=1024)

class OrganizationCreate(OrganizationBase):
    pass

class OrganizationUpdate(OrganizationBase):
    pass

class OrganizationOut(OrganizationBase):
    id: int

    model_config = {"from_attributes": True}
