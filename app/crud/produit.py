from sqlmodel import Session, select
from app.models.produit import Produit
from typing import List

def get_all_produits(session: Session) -> List[Produit]:
    statement = select(Produit)
    return session.exec(statement).all()
