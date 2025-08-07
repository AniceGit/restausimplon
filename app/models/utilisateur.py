# app/models/user.py
from typing import Optional, List, TYPE_CHECKING
from enum import Enum
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .commande import Commande

class RoleEnum(str, Enum):
    admin = "admin"
    employe = "employe"
    client = "client"
#Modèle table utilisateur
class Utilisateur(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nom: str
    prenom: str
    adresse: str
    telephone: str
    email: str = Field(unique=True)
    motdepasse: str  # Stocke le mot de passe haché
    role: RoleEnum
    is_active: bool = True
    #access_token: Optional[str] = Field(default=None)
    refresh_token: Optional[str] = Field(default=None)
    commandes: List["Commande"] = Relationship(back_populates="utilisateur")

