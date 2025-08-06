from fastapi import APIRouter, Depends
from sqlmodel import Session
from typing import List

from app.database import get_session

from app.schemas.ligne_de_commande import LigneCommandeRead, LigneCommandeCreate, LigneCommandeUpdate, MontantCommande
from app.crud.ligne_de_commande import get_all_lignes_commande, get_ligne_commande_by_id, create_ligne_commande, update_ligne_commande, delete_ligne_commande
from app.services.ligne_de_commande import get_lignes_commandes_by_commande, calculate_montant_total_commande

router = APIRouter(prefix="/lignes-de-commande", tags=["Lignes de commande"])

@router.get("/", response_model=List[LigneCommandeRead])
def read_lignes_commande(session: Session = Depends(get_session)):
    return get_all_lignes_commande(session)

@router.get("/{ligne_commande_id}", response_model=LigneCommandeRead)
def read_ligne_commande_by_id(ligne_commande_id: int, session: Session = Depends(get_session)):
    return get_ligne_commande_by_id(ligne_commande_id, session)

@router.get("/commande/{commande_id}", response_model=List[LigneCommandeRead])
def read_lignes_commandes_by_commande(commande_id: int, session: Session = Depends(get_session)):
    return get_lignes_commandes_by_commande(commande_id, session)

@router.get("/total/{commande_id}", response_model=MontantCommande)
def sum_montant_total_commande(commande_id: int, session: Session = Depends(get_session)):
    return calculate_montant_total_commande(commande_id, session)

@router.post("/", response_model=LigneCommandeRead)
def add_ligne_commande(ligne_commande: LigneCommandeCreate, session: Session = Depends(get_session)):
    return create_ligne_commande(ligne_commande, session)

@router.put("/{commande_id}", response_model=LigneCommandeUpdate)
def modify_ligne_commande(commande_id: int, ligne_commande: LigneCommandeCreate, session: Session = Depends(get_session)):
    return update_ligne_commande(commande_id, ligne_commande, session)

@router.delete("/{commande_id}")
def drop_ligne_commande(commande_id: int, session: Session = Depends(get_session)):
    return delete_ligne_commande(commande_id, session)