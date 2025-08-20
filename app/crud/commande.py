from sqlmodel import Session, select
from typing import List
from app.models.commande import Commande
from app.models.ligne_de_commande import LigneCommande
from app.schemas.commande import CommandeCreate
from fastapi import HTTPException
from sqlalchemy.orm import selectinload


def get_all_commandes(session: Session) -> List[Commande]:
    """
    Récupère toutes les commandes avec leurs lignes associées.

    Args:
        session (Session): La session SQLModel permettant l’interaction avec la base.

    Returns:
        List[Commande]: La liste des commandes avec leurs lignes de commande chargées.
    """
    statement = select(Commande).options(selectinload(Commande.lignes_commande))
    return session.exec(statement).all()


def get_commande_by_id(id: int, session: Session) -> Commande:
    """
    Récupère une commande spécifique par son identifiant, incluant ses lignes de commande.

    Args:
        id (int): L’identifiant unique de la commande.
        session (Session): La session SQLModel permettant l’interaction avec la base.

    Returns:
        Commande: La commande correspondante avec ses lignes.

    Raises:
        HTTPException (404): Si aucune commande n’existe avec cet identifiant.
    """
    statement = select(Commande).where(Commande.id == id).options(selectinload(Commande.lignes_commande))
    result = session.exec(statement).first()
    if not result:
        raise HTTPException(status_code=404, detail="Commande non trouvée pour cet id")
    return result


def update_commande(id: int, commande: Commande, session: Session) -> Commande:
    """
    Met à jour une commande existante et recalcule son prix total à partir des lignes de commande.

    Args:
        id (int): L’identifiant de la commande à mettre à jour.
        commande (Commande): Les nouvelles données de la commande (hors `id` et `prix_total`).
        session (Session): La session SQLModel permettant l’interaction avec la base.

    Returns:
        Commande: La commande mise à jour, avec les lignes et le prix total recalculé.

    Raises:
        HTTPException (404): Si la commande n’existe pas.
    """
    db_commande = session.get(Commande, id)
    if not db_commande:
        raise HTTPException(status_code=404, detail="Commande non trouvée")
    
    update_data = commande.model_dump(exclude={"id", "prix_total"})
    for key, value in update_data.items():
        setattr(db_commande, key, value)

    # Recalcule le prix total à partir des lignes de commande associées
    statement_lignes = select(LigneCommande).where(LigneCommande.commande_id == id)
    lignes = session.exec(statement_lignes).all()
    prix_total = round(sum(ligne.prix_total_ligne for ligne in lignes), 2)
    db_commande.prix_total = prix_total

    session.add(db_commande)
    session.commit()
    session.refresh(db_commande)
    
    # Recharge la commande complète avec ses lignes
    statement = select(Commande).where(Commande.id == id).options(selectinload(Commande.lignes_commande))
    full_commande = session.exec(statement).one()

    return full_commande


def delete_commande(id: int, session: Session):
    """
    Supprime une commande existante par son identifiant.

    Args:
        id (int): L’identifiant unique de la commande à supprimer.
        session (Session): La session SQLModel permettant l’interaction avec la base.

    Returns:
        str: Un message confirmant la suppression de la commande.

    Raises:
        HTTPException (404): Si la commande n’existe pas.
    """
    commande = session.get(Commande, id)
    if not commande:
        raise HTTPException(status_code=404, detail="Commande non trouvée")
    session.delete(commande)
    session.commit()
    return f"La commande {id} a été supprimée"
