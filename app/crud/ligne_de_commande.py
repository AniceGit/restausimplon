from sqlmodel import Session, select
from typing import List
from app.models.ligne_de_commande import LigneCommande
from app.schemas.ligne_de_commande import LigneCommandeCreate
from fastapi import HTTPException


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
    session.add(db_ligne_commande)
    session.commit()
    session.refresh(db_ligne_commande)
    return db_ligne_commande


def update_ligne_commande(id: int, ligne_commande: LigneCommande, session: Session) -> LigneCommande:
    db_ligne_commande = session.get(LigneCommande, id)
    if not db_ligne_commande:
        raise HTTPException(status_code=404, detail="Ligne de commande non trouvée")
    
    update_data = ligne_commande.model_dump(exclude={"id"})
    for key, value in update_data.items():
        setattr(db_ligne_commande, key, value)

    session.add(db_ligne_commande)
    session.commit()
    session.refresh(db_ligne_commande)
    return db_ligne_commande

def delete_ligne_commande(id: int, session: Session):
    ligne_commande = session.get(LigneCommande, id)
    if not ligne_commande:
        raise HTTPException(status_code=404, detail="Ligne de commande non trouvée")
    session.delete(ligne_commande)
    session.commit()
    return {"ok": True}