from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    is_superadmin: bool

    model_config = {
        "from_attributes": True
    }

class ChangePassword(BaseModel):
    old_password: str
    new_password: str

class ChangeSuperadmin(BaseModel):
    is_superadmin: bool
