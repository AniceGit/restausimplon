from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from sqlmodel import Field
from app.models.commande import CommandeStatusEnum


class CommandeRead(BaseModel):
    id: int = Field(..., gt=0, description="Identifiant unique de la commande")
    utilisateur_id: int = Field(..., gt=0, description="ID de l'utilisateur")
    date_commande: datetime = Field(..., description="Date et heure de la commande")
    statut: CommandeStatusEnum = Field(..., description="Statut actuel de la commande")
    prix_total: float

    class Config:
        orm_mode = True

class CommandeCreate(BaseModel):
    utilisateur_id: int = Field(..., gt=0, description="ID de l'utilisateur qui passe la commande")
    date_commande: Optional[datetime] = Field(default_factory=datetime.now, description="Date de la commande")
    statut: CommandeStatusEnum
    prix_total: float = Field(gt=0)

class CommandeUpdate(BaseModel):
    id: int = Field(..., gt=0, description="ID de la commande à modifier")
    utilisateur_id: Optional[int] = Field(None, gt=0, description="Nouvel ID utilisateur")
    date_commande: Optional[datetime] = Field(None, description="Nouvelle date de commande")
    statut: Optional[CommandeStatusEnum] = None
    prix_total: Optional[float] = None

    class Config:
        orm_mode = True