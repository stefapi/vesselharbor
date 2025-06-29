# app/schema/user.py
from pydantic import BaseModel, EmailStr
from typing import List
from .tag import TagOut

class UserCreate(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    is_superadmin: bool
    tags: List[TagOut] = []

    model_config = {
        "from_attributes": True
    }

class ChangePassword(BaseModel):
    old_password: str
    new_password: str

class ChangeSuperadmin(BaseModel):
    is_superadmin: bool

class UserUpdate(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: EmailStr
