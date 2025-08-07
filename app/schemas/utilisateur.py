from pydantic import BaseModel, EmailStr
from enum import Enum
from typing import Optional

class RoleEnum(str, Enum):
    admin = "admin"
    employe = "employe"
    client = "client"

# class UtilisateurBase(BaseModel):
#     email: EmailStr
#     role: RoleEnum
#     is_active: bool = True

class UtilisateurCreate(BaseModel):
    email: Optional[EmailStr] = None
    motdepasse: str
    role: RoleEnum
    is_active: bool = True

    class Config:
        orm_mode = True
class UtilisateurRead(BaseModel):
    id: int
    email: Optional[EmailStr] = None
    role: RoleEnum
    is_active: bool

    class Config:
        orm_mode = True

class UtilisateurUpdate(BaseModel):
    email: Optional[EmailStr] = None
    motdepasse: Optional[str] = None
    role: Optional[RoleEnum] = None

    class Config:
        orm_mode = True