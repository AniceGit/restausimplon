from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional

if TYPE_CHECKING:
    from .commande import Commande
    from .produit import Produit

# Modèle table Ligne de commande (produit + quantité)
class LigneCommande(SQLModel, table=True):
    """
    Modèle représentant une ligne de commande, associant un produit spécifique à une commande,
    avec sa quantité et le calcul du prix total de cette ligne.

    Attributes:
        id (int, optional): Identifiant unique de la ligne de commande (clé primaire).
        commande_id (int): Identifiant de la commande associée (clé étrangère).
        produit_id (int): Identifiant du produit commandé (clé étrangère).
        quantite (int): Quantité de produit commandée (doit être >= 1).
        prix_unitaire (float): Prix unitaire du produit au moment de la commande.
        prix_total_ligne (float): Prix total de la ligne (quantite * prix_unitaire).
        commande (Commande, optional): Relation vers la commande associée.
        produit (Produit, optional): Relation vers le produit associé.
    """
    id: Optional[int] = Field(gt=0, default=None, primary_key=True)
    commande_id: int = Field(gt=0, foreign_key="commande.id", ondelete="CASCADE")
    produit_id: int = Field(gt= 0, foreign_key="produit.id")
    quantite: int = Field(ge=1)
    prix_unitaire: float = Field(gt=0)
    prix_total_ligne: float = Field(gt=0)

    commande: Optional["Commande"] = Relationship(back_populates="lignes_commande")
    produit: Optional["Produit"] = Relationship(back_populates="lignes_commande")