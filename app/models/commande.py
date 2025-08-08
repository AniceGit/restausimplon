from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from enum import Enum
from datetime import datetime

if TYPE_CHECKING:
    from .utilisateur import Utilisateur
    from .ligne_de_commande import LigneCommande

class CommandeStatusEnum(str, Enum):
    preparation = "En préparation"
    prete = "Prête"
    servie = "Servie"
#Modèle table commande
class Commande(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    utilisateur_id: int = Field(foreign_key="utilisateur.id")
    date_commande: datetime
    statut: CommandeStatusEnum
    prix_total: float = Field(gt=0)

    utilisateur: Optional["Utilisateur"] = Relationship(back_populates="commandes")
    lignes_commande: List["LigneCommande"] = Relationship(back_populates="commande", cascade_delete=True)
