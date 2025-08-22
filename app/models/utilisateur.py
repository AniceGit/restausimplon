# app/models/user.py
from typing import Optional, List, TYPE_CHECKING
from enum import Enum
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .commande import Commande

class RoleEnum(str, Enum):
    admin = "admin"
    employe = "employe"
    client = "client"
#Modèle table utilisateur
class Utilisateur(SQLModel, table=True):
    """
    Modèle représentant un utilisateur de l'application, pouvant être un client, un employé ou un administrateur.

    Attributes:
        id (int, optional): Identifiant unique de l'utilisateur (clé primaire).
        nom (str): Nom de l'utilisateur.
        prenom (str): Prénom de l'utilisateur.
        adresse (str): Adresse postale de l'utilisateur.
        telephone (str): Numéro de téléphone de l'utilisateur.
        email (str): Adresse e-mail unique de l'utilisateur.
        motdepasse (str): Mot de passe haché de l'utilisateur.
        role (RoleEnum): Rôle de l'utilisateur dans l'application (admin, employe, client).
        is_active (bool): Indique si l'utilisateur est actif (par défaut True).
        commandes (List[Commande]): Liste des commandes associées à l'utilisateur.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    nom: str
    prenom: str
    adresse: str
    telephone: str
    email: str = Field(unique=True)
    motdepasse: str  # Stocke le mot de passe haché
    role: RoleEnum
    is_active: bool = True


    commandes: List["Commande"] = Relationship(back_populates="utilisateur")

