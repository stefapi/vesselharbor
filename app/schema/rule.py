# app/schema/rule.py
from pydantic import BaseModel
from typing import Optional

class RuleCreate(BaseModel):
    policy_id: int
    function_id: int
    environment_id: Optional[int] = None
    element_id: Optional[int] = None

class RuleUpdate(BaseModel):
    function_id: Optional[int] = None
    environment_id: Optional[int] = None
    element_id: Optional[int] = None

class RuleOut(BaseModel):
    id: int
    function_id: int
    environment_id: Optional[int]
    element_id: Optional[int]

    model_config = {"from_attributes": True}
