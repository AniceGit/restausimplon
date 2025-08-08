from sqlmodel import Session, select
from app.models.produit import Produit
from typing import List, Optional
from fastapi import HTTPException

def get_all_produits(session: Session) -> List[Produit]:
    """
    Récupère tous les produits de la base de données.

    Args:
        session (Session): Une session de base de données SQLModel pour exécuter la requête.

    Returns:
        List[Produit]: Une liste de tous les produits présents dans la base de données.
    """
    statement = select(Produit)
    return session.exec(statement).all()

def creer_produit(produit, session: Session):
    """
    Crée un nouveau produit dans la base de données.

    Args:
        produit: Un objet représentant les données du produit à créer.
        session (Session): Une session de base de données SQLModel pour ajouter le produit.

    Returns:
        Produit: Le produit nouvellement créé et ajouté à la base de données.
    """
    produit_data = produit.model_dump()
    db_produit = Produit(**produit_data)
    session.add(db_produit)
    session.commit()
    session.refresh(db_produit)
    return db_produit

def suppression_produit(produit_id: int, session: Session):
    """
    Supprime un produit de la base de données en fonction de son identifiant.

    Args:
        produit_id (int): L'identifiant du produit à supprimer.
        session (Session): Une session de base de données SQLModel pour supprimer le produit.

    Returns:
        Produit: Le produit qui a été supprimé de la base de données.

    Raises:
        HTTPException: Si le produit avec l'identifiant spécifié n'est pas trouvé.
    """
    produit = session.get(Produit, produit_id)
    if not produit:
        raise HTTPException(status_code=404, detail="Produit non trouvé")
    session.delete(produit)
    session.commit()
    return produit

def modification_produit(produit_id: int, produit_data: dict, session: Session):
    """
    Met à jour un produit existant dans la base de données.

    Args:
        produit_id (int): L'identifiant du produit à mettre à jour.
        produit_data (dict): Un dictionnaire contenant les données à mettre à jour pour le produit.
        session (Session): Une session de base de données SQLModel pour mettre à jour le produit.

    Returns:
        Produit: Le produit mis à jour.

    Raises:
        HTTPException: Si le produit avec l'identifiant spécifié n'est pas trouvé.
    """
    produit = session.get(Produit, produit_id)
    if not produit:
        raise HTTPException(status_code=404, detail="Produit non trouvé")
    for key, value in produit_data.items():
        setattr(produit, key, value)
    session.commit()
    session.refresh(produit)
    return produit

def rechercher_produits(
    session: Session,
    produit_id: Optional[int] = None,
    prix: Optional[float] = None,
    stock: Optional[int] = None
) -> List[Produit]:
    """
    Recherche des produits dans la base de données en fonction de critères optionnels.

    Args:
        session (Session): Une session de base de données SQLModel pour exécuter la requête.
        produit_id (Optional[int]): L'identifiant du produit à rechercher.
        prix (Optional[float]): Le prix des produits à rechercher.
        stock (Optional[int]): Le stock des produits à rechercher.

    Returns:
        List[Produit]: Une liste de produits correspondant aux critères de recherche.
    """
    query = select(Produit)
    if produit_id is not None:
        query = query.where(Produit.id == produit_id)
    if prix is not None:
        query = query.where(Produit.prix == prix)
    if stock is not None:
        query = query.where(Produit.stock == stock)
    return session.exec(query).all()
