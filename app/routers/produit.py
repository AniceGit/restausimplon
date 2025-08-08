from sqlmodel import SQLModel, create_engine, Session
from fastapi import APIRouter, Depends, Query
from typing import List
from app.crud.produit import creer_produit, get_all_produits, suppression_produit, modification_produit, rechercher_produits
from app.database import get_session
from app.schemas.produit import ProduitRead, ProduitCreate, ProduitUpdate
from typing import List, Optional

router = APIRouter(prefix="/produits", tags=["Produits"])

@router.get("/", response_model=List[ProduitRead])
def read_produits(session: Session = Depends(get_session)):
    """
    Récupère tous les produits de la base de données.

    Args:
        session (Session): Une session de base de données SQLModel injectée automatiquement.

    Returns:
        List[ProduitRead]: Une liste de tous les produits présents dans la base de données.
    """
    return get_all_produits(session)

@router.post("/", response_model=ProduitRead)
def create_produit(produit: ProduitCreate, session: Session = Depends(get_session)):
    """
    Crée un nouveau produit dans la base de données.

    Args:
        produit (ProduitCreate): Les données du produit à créer.
        session (Session): Une session de base de données SQLModel injectée automatiquement.

    Returns:
        ProduitRead: Le produit nouvellement créé et ajouté à la base de données.
    """
    return creer_produit(produit, session)

@router.delete("/{produit_id}", response_model=ProduitRead)
def delete_produit(produit_id: int, session: Session = Depends(get_session)):
    """
    Supprime un produit de la base de données en fonction de son identifiant.

    Args:
        produit_id (int): L'identifiant du produit à supprimer.
        session (Session): Une session de base de données SQLModel injectée automatiquement.

    Returns:
        ProduitRead: Le produit qui a été supprimé de la base de données.
    """
    produit = suppression_produit(produit_id, session)
    return produit

@router.put("/{produit_id}", response_model=ProduitRead)
def update_produit(produit_id: int, produit: ProduitUpdate, session: Session = Depends(get_session)):
    """
    Met à jour un produit existant dans la base de données.

    Args:
        produit_id (int): L'identifiant du produit à mettre à jour.
        produit (ProduitUpdate): Les données à mettre à jour pour le produit.
        session (Session): Une session de base de données SQLModel injectée automatiquement.

    Returns:
        ProduitRead: Le produit mis à jour.
    """
    produit_data = produit.model_dump(exclude_unset=True)
    updated_produit = modification_produit(produit_id, produit_data, session)
    return updated_produit

@router.get("/search", response_model=List[ProduitRead])
def recherche_produit(
    produit_id: Optional[int] = Query(None),
    prix: Optional[float] = Query(None),
    stock: Optional[int] = Query(None),
    session: Session = Depends(get_session)
):
    """
    Recherche des produits dans la base de données en fonction de critères optionnels.

    Args:
        produit_id (Optional[int]): L'identifiant du produit à rechercher.
        prix (Optional[float]): Le prix des produits à rechercher.
        stock (Optional[int]): Le stock des produits à rechercher.
        session (Session): Une session de base de données SQLModel injectée automatiquement.

    Returns:
        List[ProduitRead]: Une liste de produits correspondant aux critères de recherche.
    """
    produits = rechercher_produits(session, produit_id, prix, stock)
    return produits
