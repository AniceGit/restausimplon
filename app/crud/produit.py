from sqlmodel import Session, select, or_
#from app.schemas.produit import ProduitCreer, ProduitLu
from app.models.produit import Produit
from typing import List, Optional

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

def rechercher_produits(
    session: Session,
    produit_id: Optional[int] = None,
    prix: Optional[float] = None,
    stock: Optional[int] = None
) -> List[Produit]:
    # Commencez par une requête de base
    query = select(Produit)

    # Ajoutez des filtres en fonction des paramètres fournis
    if produit_id is not None:
        query = query.where(Produit.id == produit_id)
    if prix is not None:
        query = query.where(Produit.prix == prix)
    if stock is not None:
        query = query.where(Produit.stock == stock)

    # Exécutez la requête et retournez les résultats
    return session.exec(query).all()