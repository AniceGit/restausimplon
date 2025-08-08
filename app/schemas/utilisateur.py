from pydantic import BaseModel,Field, EmailStr
from enum import Enum
from typing import Optional

class RoleEnum(str, Enum):
    admin = "admin"
    employe = "employe"
    client = "client"

class UtilisateurCreate(BaseModel):
    email: EmailStr
    nom: str = Field(..., min_length=2, max_length=50, description="Nom de l'utilisateur")
    prenom: str = Field(..., min_length=2, max_length=20, description="Prénom de l'utilisateur")
    adresse: str = Field(..., min_length=5, max_length=100, description="Adresse de l'utilisateur")
    telephone: str = Field(..., min_length=10, max_length=15, description="Numéro de téléphone de l'utilisateur")
    motdepasse: str = Field(..., min_length=8, max_length=15, description="Mot de passe de l'utilisateur")
    role: RoleEnum
    is_active: bool = True
    
    class Config:
        orm_mode = True

class UtilisateurRead(BaseModel):
    id: int = Field(..., gt=0)
    email: EmailStr = Field(..., description="Email de l'utilisateur")
    nom: str = Field(..., description="Nom de l'utilisateur")
    prenom: str = Field(..., description="Prénom de l'utilisateur")
    adresse: str = Field(..., description="Adresse de l'utilisateur")
    telephone: str = Field(..., description="Téléphone de l'utilisateur")
    role: RoleEnum
    is_active: bool

    class Config:
        orm_mode = True

class UtilisateurUpdate(BaseModel):
    email: Optional[EmailStr] = Field(None, description="Nouvelle adresse email")
    nom: Optional[str] = Field(None, min_length=2, max_length=50, description="Nouveau nom")
    prenom: Optional[str] = Field(None, min_length=2, max_length=50, description="Nouveau prénom")
    adresse: Optional[str] = Field(None, min_length=5, max_length=200, description="Nouvelle adresse")
    telephone: Optional[str] = Field(None, min_length=10, max_length=15, description="Nouveau téléphone")
    role: Optional[RoleEnum] = None

    class Config:
        orm_mode = True