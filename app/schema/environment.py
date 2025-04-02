from pydantic import BaseModel

class EnvironmentCreate(BaseModel):
    name: str

class EnvironmentOut(BaseModel):
    id: int
    name: str

    model_config = {
        "from_attributes": True
    }

class AssignUserEnv(BaseModel):
    user_id: int
    role: str  # "user" ou "admin"

class ChangeUserEnvRole(BaseModel):
    role: str  # "user" ou "admin"
