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
    """
    Modèle représentant une commande passée par un utilisateur.

    Attributes:
        id: Identifiant unique de la commande (clé primaire).
        utilisateur_id: Identifiant de l'utilisateur ayant passé la commande.
        date_commande: Date et heure de la commande.
        statut: Statut actuel de la commande, basé sur CommandeStatusEnum 
                (préparation, prête, servie).
        prix_total: Montant total de la commande.
        utilisateur: Relation vers l'utilisateur ayant passé la commande.
        lignes_commande: Liste des lignes de commande associées, avec suppression en cascade.
    """
    id: Optional[int] = Field(gt=0, default=None, primary_key=True)
    utilisateur_id: int = Field(gt=0, foreign_key="utilisateur.id")
    date_commande: datetime
    statut: CommandeStatusEnum
    prix_total: float = Field(gt=0)

    utilisateur: Optional["Utilisateur"] = Relationship(back_populates="commandes")
    lignes_commande: List["LigneCommande"] = Relationship(back_populates="commande", cascade_delete=True)
