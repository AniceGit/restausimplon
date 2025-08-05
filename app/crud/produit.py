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
