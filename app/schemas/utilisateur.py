from pydantic import BaseModel,Field, EmailStr
from enum import Enum
from typing import Optional

class RoleEnum(str, Enum):
    admin = "admin"
    employe = "employe"
    client = "client"

class UtilisateurCreate(BaseModel):
    email: EmailStr
    nom: str = Field(..., min_length=2)
    prenom: str = Field(..., min_length=2)
    adresse: str
    telephone: str
    motdepasse: str = Field(..., min_length=8)
    role: RoleEnum
    is_active: bool = True

    class Config:
        orm_mode = True

class UtilisateurRead(BaseModel):
    id: int
    email: str
    nom: str
    prenom: str
    adresse: str
    telephone: str
    role: RoleEnum
    is_active: bool

    class Config:
        orm_mode = True

class UtilisateurUpdate(BaseModel):
    email: Optional[str] = None
    nom: Optional[str] = None
    prenom: Optional[str] = None
    adresse: Optional[str] = None
    telephone: Optional[str] = None
    motdepasse: Optional[str] = None
    role: Optional[RoleEnum] = None

    class Config:
        orm_mode = True
    
