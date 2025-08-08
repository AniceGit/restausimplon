from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional

if TYPE_CHECKING:
    from .commande import Commande
    from .produit import Produit

# Modèle table Ligne de commande (produit + quantité)
class LigneCommande(SQLModel, table=True):
    id: Optional[int] = Field(gt=0, default=None, primary_key=True)
    commande_id: int = Field(gt=0, foreign_key="commande.id", ondelete="CASCADE")
    produit_id: int = Field(gt= 0, foreign_key="produit.id")
    quantite: int = Field(ge=1)
    prix_unitaire: float = Field(gt=0)
    prix_total_ligne: float = Field(gt=0)

    commande: Optional["Commande"] = Relationship(back_populates="lignes_commande")
    produit: Optional["Produit"] = Relationship(back_populates="lignes_commande")