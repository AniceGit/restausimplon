from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

if TYPE_CHECKING:
    from .produit import Produit

class Categorie(SQLModel, table=True):
    """
    Modèle représentant une catégorie de produits ou de menu.

    Attributes:
        id: Identifiant unique de la catégorie (clé primaire).
        nom: Nom unique de la catégorie.
        description: Description optionnelle de la catégorie.
        produits: Liste des produits associés à cette catégorie.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    nom: str = Field(unique=True)
    description: Optional[str] = None

    produits: List["Produit"] = Relationship(back_populates="categorie")
