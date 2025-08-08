from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

if TYPE_CHECKING:
    from .produit import Produit

# Modèle de la table Categorie (catégories de menu)
class Categorie(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nom: str = Field(unique=True) 
    description: Optional[str] = None

    produits: List["Produit"] = Relationship(back_populates="categorie")
