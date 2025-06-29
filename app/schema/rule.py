# app/schema/rule.py
from pydantic import BaseModel
from typing import Optional

class RuleCreate(BaseModel):
    policy_id: int
    function_id: int
    environment_id: Optional[int] = None
    element_id: Optional[int] = None
    access_schedule: Optional[dict] = None

class RuleUpdate(BaseModel):
    function_id: Optional[int] = None
    environment_id: Optional[int] = None
    element_id: Optional[int] = None
    access_schedule: Optional[dict] = None

class RuleOut(BaseModel):
    id: int
    function_id: int
    environment_id: Optional[int]
    element_id: Optional[int]
    access_schedule: Optional[dict]

    model_config = {"from_attributes": True}
