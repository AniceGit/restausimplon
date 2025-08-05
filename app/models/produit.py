from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship


if TYPE_CHECKING:
    from .categorie import Categorie
    from .ligne_de_commande import LigneCommande

# Modèle de la table Product (articles du menu)
class Produit(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nom: str
    description: Optional[str] = None
    prix: float = Field(gt=0)
    stock: int = Field(default=0, ge=0)
    categorie_id: int = Field(foreign_key="categorie.id")

    categorie: Optional["Categorie"] = Relationship(back_populates="produits")
    lignes_commande: List["LigneCommande"] = Relationship(back_populates="produit")

