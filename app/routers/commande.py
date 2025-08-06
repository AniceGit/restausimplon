from fastapi import APIRouter, Depends
from sqlmodel import Session
from typing import List
from datetime import datetime

from app.database import get_session

from app.schemas.commande import CommandeRead, CommandeCreate, CommandeUpdate
from app.schemas.ligne_de_commande import LigneCommandeCreateWithoutCommandId
from app.crud.commande import get_all_commandes, get_commande_by_id, create_commande, update_commande, delete_commande
from app.services.commande import create_commande_with_lignes_and_utilisateur, get_commandes_by_utilisateur_id, get_commandes_by_date

router = APIRouter(prefix="/commandes", tags=["Commandes"])

@router.get("/", response_model=List[CommandeRead])
def read_commandes(session: Session = Depends(get_session)):
    return get_all_commandes(session)

@router.get("/{commande_id}", response_model=CommandeRead)
def read_commande_by_id(commande_id: int, session: Session = Depends(get_session)):
    return get_commande_by_id(commande_id, session)

@router.get("/utilisateur/{utilisateur_id}", response_model=List[CommandeRead])
def read_commande_by_utilisateur_id(utilisateur_id: int, session: Session = Depends(get_session)):
    return get_commandes_by_utilisateur_id(utilisateur_id, session)

@router.get("/date/{date_commande}", response_model=List[CommandeRead])
def read_commande_by_date(date_commande: datetime, session = Depends(get_session)):
    return get_commandes_by_date(date_commande, session)

@router.post("/", response_model=CommandeRead)
def add_commande(commande: CommandeCreate, session: Session = Depends(get_session)):
    return create_commande(commande, session)

@router.post("/lignes/", response_model=CommandeRead)
def add_commande_with_lignes_and_utilisateur(commande: CommandeCreate, lignes_commande: List[LigneCommandeCreateWithoutCommandId], session: Session = Depends(get_session)):
    return create_commande_with_lignes_and_utilisateur(commande, lignes_commande, session)

@router.put("/{commande_id}", response_model=CommandeUpdate)
def modify_commande(commande_id: int, commande: CommandeCreate, session: Session = Depends(get_session)):
    return update_commande(commande_id, commande, session)

@router.delete("/{commande_id}")
def drop_commande(commande_id: int, session: Session = Depends(get_session)):
    return delete_commande(commande_id, session)