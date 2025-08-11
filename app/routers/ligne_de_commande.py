from fastapi import APIRouter, HTTPException, Depends, status
from sqlmodel import Session
from typing import List

from app.database import get_session

from app.schemas.ligne_de_commande import LigneCommandeRead, LigneCommandeCreate, LigneCommandeUpdate
from app.crud.ligne_de_commande import get_all_lignes_commande, get_ligne_commande_by_id, create_ligne_commande, update_ligne_commande, delete_ligne_commande
from app.services.ligne_de_commande import get_lignes_commandes_by_commande
from app.schemas.commande import CommandeWithLignes

#gestion des autorisations : 
from app.core.security import get_current_user
from app.models.utilisateur import Utilisateur


router = APIRouter(prefix="/lignes-de-commande", tags=["Lignes de commande"])

@router.get("/", response_model=List[LigneCommandeRead])
def read_lignes_commande(session: Session = Depends(get_session), current_user: Utilisateur = Depends(get_current_user)):
    # Seuls admin et employé peuvent voir les lignes de commabde
    if current_user.role not in ("admin", "employe"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Accès refusé")
    
    return get_all_lignes_commande(session)

@router.get("/{ligne_commande_id}", response_model=LigneCommandeRead)
def read_ligne_commande_by_id(ligne_commande_id: int, session: Session = Depends(get_session), current_user: Utilisateur = Depends(get_current_user)):
    # Seuls admin et employé peuvent voir les lignes de commabde
    if current_user.role not in ("admin", "employe"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Accès refusé")
    
    return get_ligne_commande_by_id(ligne_commande_id, session)

@router.get("/commande/{commande_id}", response_model=List[LigneCommandeRead])
def read_lignes_commandes_by_commande(commande_id: int, session: Session = Depends(get_session), current_user: Utilisateur = Depends(get_current_user)):
    # Seuls admin et employé peuvent voir les lignes de commabde
    if current_user.role not in ("admin", "employe"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Accès refusé")
    
    return get_lignes_commandes_by_commande(commande_id, session)

@router.post("/", response_model=CommandeWithLignes)
def add_ligne_commande(ligne_commande: LigneCommandeCreate, session: Session = Depends(get_session), current_user: Utilisateur = Depends(get_current_user)):
    # Seuls admin et employé peuvent créer une ligne de commabde
    if current_user.role not in ("admin", "employe"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Accès refusé")
    
    return create_ligne_commande(ligne_commande, session)

@router.put("/{ligne_commande_id}", response_model=CommandeWithLignes)
def modify_ligne_commande(ligne_commande_id: int, ligne_commande: LigneCommandeUpdate, session: Session = Depends(get_session), current_user: Utilisateur = Depends(get_current_user)):
    # Seuls admin et employé peuvent modifier une ligne de commabde
    if current_user.role not in ("admin", "employe"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Accès refusé")

    return update_ligne_commande(ligne_commande_id, ligne_commande, session)

@router.delete("/{ligne_commande_id}")
def drop_ligne_commande(ligne_commande_id: int, session: Session = Depends(get_session), current_user: Utilisateur = Depends(get_current_user)):
    # Seuls admin et employé peuvent supprimer une ligne de commabde
    if current_user.role not in ("admin", "employe"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Accès refusé")

    return delete_ligne_commande(ligne_commande_id, session)