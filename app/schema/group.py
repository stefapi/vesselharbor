from pydantic import BaseModel
from typing import List, Optional
from ..schema.function import FunctionOut
from ..schema.user import UserOut

class GroupCreate(BaseModel):
    name: str
    description: Optional[str] = None

class GroupUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]

class GroupOut(BaseModel):
    id: int
    name: str
    description: Optional[str]
    # Facultatif : inclure fonctions et utilisateurs associés
    functions: List[FunctionOut] = []
    users: List[UserOut] = []

    model_config = {
        "from_attributes": True
    }
