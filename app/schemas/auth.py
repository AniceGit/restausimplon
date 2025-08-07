from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum

class RoleEnum(str, Enum):
    admin = "admin"
    employe = "employe"
    client = "client"

class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: Optional[str]

class TokenData(BaseModel):
    email: Optional[EmailStr] = None

class UserInDB(BaseModel):
    email: EmailStr | None = None
    motdepasse: str
    role: RoleEnum
    is_active: bool

    class Config:
        from_attributes = True




