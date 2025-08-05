from sqlmodel import Session, select
from typing import List
from app.models.commande import Commande
from app.schemas.commande import CommandeCreate
from fastapi import HTTPException


def get_all_commandes(session: Session) -> List[Commande]:
    statement = select(Commande)
    return session.exec(statement).all()


def get_commande_by_id(id: int, session: Session) -> Commande:
    commande = session.get(Commande, id)
    if not commande:
        raise HTTPException(status_code=404, detail="Commande non trouvée")
    return commande


def create_commande(commande: CommandeCreate, session: Session) -> Commande:
    db_commande = Commande(**commande.model_dump())
    session.add(db_commande)
    session.commit()
    session.refresh(db_commande)
    return db_commande


def update_commande(id: int, commande: Commande, session: Session) -> Commande:
    db_commande = session.get(Commande, id)
    if not db_commande:
        raise HTTPException(status_code=404, detail="Commande non trouvée")
    
    update_data = commande.model_dump(exclude={"id"})
    for key, value in update_data.items():
        setattr(db_commande, key, value)

    session.add(db_commande)
    session.commit()
    session.refresh(db_commande)
    return db_commande


def delete_commande(id: int, session: Session):
    commande = session.get(Commande, id)
    if not commande:
        raise HTTPException(status_code=404, detail="Commande non trouvée")
    session.delete(commande)
    session.commit()
    return {"ok": True}
