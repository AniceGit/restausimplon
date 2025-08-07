# app/models/user.py
from typing import Optional, List, TYPE_CHECKING
from enum import Enum
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .client import Client

class RoleEnum(str, Enum):
    admin = "admin"
    employe = "employe"
    client = "client"
#Modèle table utilisateur
class Utilisateur(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True)
    motdepasse: str  # Stocke le mot de passe haché
    role: RoleEnum
    is_active: bool = True
    refresh_token: Optional[str] = Field(default=None)
    
    client: Optional["Client"] = Relationship(back_populates="user", sa_relationship_kwargs={"uselist": False})
