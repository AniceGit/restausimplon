from sqlmodel import Session, select
from typing import List
from app.models.ligne_de_commande import LigneCommande
from app.models.commande import Commande
from app.schemas.commande import CommandeWithLignes
from app.schemas.ligne_de_commande import LigneCommandeCreate, LigneCommandeUpdate
from fastapi import HTTPException
from sqlalchemy.orm import selectinload

def get_all_lignes_commande(session: Session) -> List[LigneCommande]:
    statement = select(LigneCommande)
    return session.exec(statement).all()


def get_ligne_commande_by_id(id: int, session: Session) -> LigneCommande:
    ligne_commande = session.get(LigneCommande, id)
    if not ligne_commande:
        raise HTTPException(status_code=404, detail="Ligne de commande non trouvée")
    return ligne_commande


def create_ligne_commande(ligne_commande: LigneCommandeCreate, session: Session) -> LigneCommande:
    db_ligne_commande = LigneCommande(**ligne_commande.model_dump())
    prix_total_ligne = db_ligne_commande.quantite * db_ligne_commande.prix_unitaire
    print(prix_total_ligne)
    db_ligne_commande.prix_total_ligne = prix_total_ligne

    commande = session.get(Commande, db_ligne_commande.commande_id)
    if not commande:
        raise HTTPException(status_code=404, detail="Commande non trouvée")
    if commande:
        commande.prix_total += prix_total_ligne
        session.add(commande)

    session.add(db_ligne_commande)
    session.commit()
    session.refresh(db_ligne_commande)

    statement = select(Commande).where(Commande.id == commande.id).options(selectinload(Commande.lignes_commande))
    full_commande = session.exec(statement).one()

    return full_commande


def update_ligne_commande(id: int, ligne_commande: LigneCommande, session: Session) -> CommandeWithLignes:
    db_ligne_commande = session.get(LigneCommande, id)
    if not db_ligne_commande:
        raise HTTPException(status_code=404, detail="Ligne de commande non trouvée")
    
    old_prix_total_ligne = db_ligne_commande.prix_total_ligne

    update_data = ligne_commande.model_dump(exclude={"id"})
    prix_total_ligne = update_data["quantite"] * update_data["prix_unitaire"]
    print(prix_total_ligne)
    update_data["prix_total_ligne"] = prix_total_ligne
    for key, value in update_data.items():
        setattr(db_ligne_commande, key, value)

    #différence de prix entre la nouvelle somme et l'ancienne
    price_difference = db_ligne_commande.prix_total_ligne - old_prix_total_ligne

    commande = session.get(Commande, db_ligne_commande.commande_id)
    if commande:
        commande.prix_total += price_difference
        session.add(commande)

    session.add(db_ligne_commande)
    session.commit()
    session.refresh(db_ligne_commande)

    statement = select(Commande).where(Commande.id == commande.id).options(selectinload(Commande.lignes_commande))
    full_commande = session.exec(statement).one()

    return full_commande

def delete_ligne_commande(id: int, session: Session):
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