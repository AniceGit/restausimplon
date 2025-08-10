from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from sqlmodel import Field
from app.models.commande import CommandeStatusEnum
from app.schemas.ligne_de_commande import LigneCommandeRead


class CommandeRead(BaseModel):
    id: int = Field(..., gt=0, description="Identifiant unique de la commande")
    utilisateur_id: int = Field(..., gt=0, description="ID de l'utilisateur")
    date_commande: datetime = Field(..., description="Date et heure de la commande")
    statut: CommandeStatusEnum = Field(..., description="Statut actuel de la commande")
    prix_total: float = Field(..., gt=0, description="Prix total de la commande")

    class Config:
        orm_mode = True

class CommandeCreate(BaseModel):
    utilisateur_id: int = Field(..., gt=0, description="ID de l'utilisateur qui passe la commande")
    date_commande: Optional[datetime] = Field(default_factory=datetime.now, description="Date de la commande")
    statut: CommandeStatusEnum = Field(..., description="Statut actuel de la commande")

class CommandeUpdate(BaseModel):
    utilisateur_id: Optional[int] = Field(None, gt=0, description="Nouvel ID utilisateur")
    statut: Optional[CommandeStatusEnum] = Field(None, description="Nouveau statut actuel de la commande")

    class Config:
        orm_mode = True

class CommandeWithLignes(BaseModel):
    id: int = Field(..., gt=0, description="Identifiant unique de la commande")
    utilisateur_id: int = Field(..., gt=0, description="ID de l'utilisateur")
    date_commande: datetime = Field(..., description="Date et heure de la commande")
    statut: CommandeStatusEnum = Field(..., description="Statut actuel de la commande")
    prix_total: float = Field(..., gt=0, description="Prix total de la commande")
    lignes_commande: list[LigneCommandeRead] = Field(description="Lignes de commande associées à la commande")

    class Config:
        orm_mode = True