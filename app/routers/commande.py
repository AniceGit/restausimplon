from fastapi import APIRouter, Depends
from sqlmodel import Session
from typing import List

from app.database import get_session

from app.schemas.commande import CommandeRead, CommandeCreate, CommandeUpdate
from app.crud.commande import get_all_commandes, get_commande_by_id, create_commande, update_commande, delete_commande

router = APIRouter(prefix="/commandes", tags=["Commandes"])

@router.get("/", response_model=List[CommandeRead])
def read_commandes(session: Session = Depends(get_session)):
    return get_all_commandes(session)

@router.get("/{commande_id}", response_model=CommandeRead)
def read_commande(commande_id: int, session: Session = Depends(get_session)):
    return get_commande_by_id(commande_id, session)

@router.post("/", response_model=CommandeRead)
def add_commande(commande: CommandeCreate, session: Session = Depends(get_session)):
    return create_commande(commande, session)

@router.put("/{commande_id}", response_model=CommandeUpdate)
def modify_commande(id: int, commande: CommandeCreate, session: Session = Depends(get_session)):
    return update_commande(id, commande, session)

@router.delete("/{commande_id}")
def drop_commande(commande_id: int, session: Session = Depends(get_session)):
    return delete_commande(commande_id, session)