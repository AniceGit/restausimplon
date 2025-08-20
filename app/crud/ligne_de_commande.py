from sqlmodel import Session, select
from typing import List
from app.models.ligne_de_commande import LigneCommande
from app.models.commande import Commande
from app.schemas.commande import CommandeWithLignes
from app.schemas.ligne_de_commande import LigneCommandeCreate, LigneCommandeUpdate
from fastapi import HTTPException
from sqlalchemy.orm import selectinload


def get_all_lignes_commande(session: Session) -> List[LigneCommande]:
    """
    Récupère toutes les lignes de commande de la base.

    Args:
        session (Session): La session SQLModel permettant l’accès à la base.

    Returns:
        List[LigneCommande]: La liste des lignes de commande existantes.
    """
    statement = select(LigneCommande)
    return session.exec(statement).all()


def get_ligne_commande_by_id(id: int, session: Session) -> LigneCommande:
    """
    Récupère une ligne de commande par son identifiant.

    Args:
        id (int): L’identifiant unique de la ligne de commande.
        session (Session): La session SQLModel pour interagir avec la base.

    Returns:
        LigneCommande: L’objet ligne de commande correspondant.

    Raises:
        HTTPException (404): Si aucune ligne de commande ne correspond à cet ID.
    """
    ligne_commande = session.get(LigneCommande, id)
    if not ligne_commande:
        raise HTTPException(status_code=404, detail="Ligne de commande non trouvée")
    return ligne_commande


def create_ligne_commande(ligne_commande: LigneCommandeCreate, session: Session) -> LigneCommande:
    """
    Crée une nouvelle ligne de commande et met à jour le prix total de la commande associée.

    Args:
        ligne_commande (LigneCommandeCreate): Les données de la nouvelle ligne (produit, quantité, prix unitaire).
        session (Session): La session SQLModel pour interagir avec la base.

    Returns:
        Commande: La commande complète mise à jour avec ses lignes.

    Raises:
        HTTPException (404): Si la commande associée n’existe pas.
    """
    db_ligne_commande = LigneCommande(**ligne_commande.model_dump())
    prix_total_ligne = round(db_ligne_commande.quantite * db_ligne_commande.prix_unitaire, 2)
    db_ligne_commande.prix_total_ligne = prix_total_ligne

    commande = session.get(Commande, db_ligne_commande.commande_id)
    if not commande:
        raise HTTPException(status_code=404, detail="Commande non trouvée")

    # Mise à jour du prix total de la commande
    commande.prix_total += prix_total_ligne
    session.add(commande)

    session.add(db_ligne_commande)
    session.commit()
    session.refresh(db_ligne_commande)

    # Retourne la commande complète avec ses lignes
    statement = select(Commande).where(Commande.id == commande.id).options(selectinload(Commande.lignes_commande))
    full_commande = session.exec(statement).one()

    return full_commande


def update_ligne_commande(id: int, ligne_commande: LigneCommande, session: Session) -> CommandeWithLignes:
    """
    Met à jour une ligne de commande existante et ajuste le prix total de la commande associée.

    Args:
        id (int): L’identifiant de la ligne de commande à modifier.
        ligne_commande (LigneCommande): Les nouvelles données de la ligne.
        session (Session): La session SQLModel pour interagir avec la base.

    Returns:
        CommandeWithLignes: La commande mise à jour avec ses lignes.

    Raises:
        HTTPException (404): Si la ligne de commande n’existe pas.
    """
    db_ligne_commande = session.get(LigneCommande, id)
    if not db_ligne_commande:
        raise HTTPException(status_code=404, detail="Ligne de commande non trouvée")
    
    old_prix_total_ligne = db_ligne_commande.prix_total_ligne

    update_data = ligne_commande.model_dump(exclude={"id"})
    prix_total_ligne = round(update_data["quantite"] * update_data["prix_unitaire"], 2)
    update_data["prix_total_ligne"] = prix_total_ligne

    for key, value in update_data.items():
        setattr(db_ligne_commande, key, value)

    # Ajuste la commande en fonction de la différence de prix
    price_difference = db_ligne_commande.prix_total_ligne - old_prix_total_ligne
    commande = session.get(Commande, db_ligne_commande.commande_id)
    if commande:
        commande.prix_total += price_difference
        session.add(commande)

    session.add(db_ligne_commande)
    session.commit()
    session.refresh(db_ligne_commande)

    # Retourne la commande mise à jour
    statement = select(Commande).where(Commande.id == commande.id).options(selectinload(Commande.lignes_commande))
    full_commande = session.exec(statement).one()

    return full_commande


def delete_ligne_commande(id: int, session: Session):
    """
    Supprime une ligne de commande et ajuste le prix total de la commande associée.

    Args:
        id (int): L’identifiant unique de la ligne de commande.
        session (Session): La session SQLModel pour interagir avec la base.

    Returns:
        str: Un message confirmant la suppression.

    Raises:
        HTTPException (404): Si la ligne de commande n’existe pas.
    """
    ligne_commande = session.get(LigneCommande, id)
    if not ligne_commande:
        raise HTTPException(status_code=404, detail="Ligne de commande non trouvée")
    
    prix_total_ligne = ligne_commande.prix_total_ligne
    commande = session.get(Commande, ligne_commande.commande_id)
    if commande:
        commande.prix_total -= prix_total_ligne
        session.add(commande)
    
    session.delete(ligne_commande)
    session.commit()
    return f"Ligne commande {ligne_commande.id} supprimée de la commande {commande.id}"
