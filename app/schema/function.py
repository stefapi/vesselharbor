from pydantic import BaseModel
from typing import Optional

class FunctionCreate(BaseModel):
    name: str
    description: Optional[str] = None

class FunctionUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]

class FunctionOut(BaseModel):
    id: int
    name: str
    description: Optional[str]

    model_config = {
        "from_attributes": True
    }
