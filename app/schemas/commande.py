from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.models.commande import CommandeStatusEnum


class CommandeRead(BaseModel):
    id: int
    utilisateur_id: int
    date_commande: datetime
    statut: CommandeStatusEnum

    class Config:
        orm_mode = True

class CommandeCreate(BaseModel):
    utilisateur_id: int
    date_commande: datetime
    statut: CommandeStatusEnum


class CommandeUpdate(BaseModel):
    id: int
    utilisateur_id: Optional[int] = None
    date_commande: Optional[datetime] = None
    statut: Optional[CommandeStatusEnum] = None

    class Config:
        orm_mode = True