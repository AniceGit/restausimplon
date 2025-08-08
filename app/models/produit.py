from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship


if TYPE_CHECKING:
    from .categorie import Categorie
    from .ligne_de_commande import LigneCommande

# Modèle de la table Product (articles du menu)
class Produit(SQLModel, table=True):
    """
    Modèle de la table Produit représentant les articles d'un menu.

    Ce modèle définit la structure d'un produit avec ses attributs et ses relations
    avec d'autres tables de la base de données, notamment les catégories et les lignes de commande.

    Attributes:
        id (Optional[int]): Identifiant unique du produit. Clé primaire auto-incrémentée.
        nom (str): Nom du produit. Ce champ est obligatoire.
        description (Optional[str]): Description du produit. Ce champ est optionnel.
        prix (float): Prix du produit. Doit être supérieur à zéro.
        stock (int): Quantité en stock du produit. Ne peut pas être négatif, valeur par défaut est zéro.
        categorie_id (int): Identifiant de la catégorie à laquelle le produit appartient.
            Clé étrangère référençant la table Categorie.
        categorie (Optional["Categorie"]): Relation avec le modèle Categorie.
            Un produit appartient à une catégorie.
        lignes_commande (List["LigneCommande"]): Relation avec le modèle LigneCommande.
            Un produit peut être inclus dans plusieurs lignes de commande.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    nom: str
    description: Optional[str] = None
    prix: float = Field(gt=0)
    stock: int = Field(default=0, ge=0)
    categorie_id: int = Field(foreign_key="categorie.id")

    categorie: Optional["Categorie"] = Relationship(back_populates="produits")
    lignes_commande: List["LigneCommande"] = Relationship(back_populates="produit")

