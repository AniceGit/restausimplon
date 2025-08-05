from sqlmodel import Session, select
#from app.schemas.produit import ProduitCreer, ProduitLu
from app.models.produit import Produit
from typing import List  


def get_all_produits(session: Session) -> List[Produit]:
    statement = select(Produit)
    return session.exec(statement).all()


def creer_produit(produit, session: Session):
    produit_data = produit.model_dump()
    db_produit = Produit(**produit_data)
    session.add(db_produit)
    session.commit()
    session.refresh(db_produit)

    return db_produit

def suppression_produit(produit_id, session: Session):
    produit = session.get(Produit, produit_id)
    if produit:
        session.delete(produit)
        session.commit()
    return produit

def modification_produit(produit_id: int, produit_data: dict, session: Session):

    produit = session.get(Produit, produit_id)
    if produit:
        for key, value in produit_data.items():
            setattr(produit, key, value)
        session.commit()
        session.refresh(produit)
    return produit
