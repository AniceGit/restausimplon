from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

if TYPE_CHECKING:
    from .commande import Commande
    from .utilisateur import Utilisateur

# Modèle de la table Client
class Client(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nom: str
    prenom: str
    adresse: str
    telephone: str
    email: str = Field(unique=True)
    user_id: Optional[int] = Field(default=None, foreign_key="utilisateur.id")

    user: Optional["Utilisateur"] = Relationship(back_populates="client")
    commandes: List["Commande"] = Relationship(back_populates="client")
