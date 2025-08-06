from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from enum import Enum
from datetime import datetime

if TYPE_CHECKING:
    from .client import Client
    from .ligne_de_commande import LigneCommande

class CommandeStatusEnum(str, Enum):
    preparation = "En préparation"
    prete = "Prête"
    servie = "Servie"
#Modèle table commande
class Commande(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    client_id: int = Field(foreign_key="client.id")
    date_commande: datetime
    statut: CommandeStatusEnum

    client: Optional["Client"] = Relationship(back_populates="commandes")
    lignes_commande: List["LigneCommande"] = Relationship(back_populates="commande", cascade_delete=True)
