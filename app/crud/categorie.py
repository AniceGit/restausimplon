from http.client import HTTPException
from app.schemas.categorie import CategorieCreate
from sqlmodel import Session, select
from app.models.categorie import Categorie
from typing import List

def create_categorie(categorie: CategorieCreate, session: Session) -> Categorie:
    db_categorie = Categorie(**categorie.model_dump())
    session.add(db_categorie)
    session.commit()
    session.refresh(db_categorie)
    return db_categorie


def get_all_categories(session: Session) -> List[Categorie]:
    statement = select(Categorie)
    return session.exec(statement).all()


def get_categorie_by_id(id: int, session: Session) -> Categorie:
    db_categorie = session.get(Categorie, id)
    if not db_categorie:
        raise HTTPException(status_code=404, detail="Catégorie non trouvée")    
    return db_categorie
    

def update_categorie_by_id(id: int, categorie: Categorie, session: Session) -> Categorie:
    db_categorie = session.get(Categorie, id)
    if not db_categorie:
        raise HTTPException(status_code=404, detail="Catégorie non trouvée")
    update_data = categorie.model_dump(exclude={"id"})
    for key, value in update_data.items():
        setattr(db_categorie, key, value)
    
    session.add(db_categorie)
    session.commit()
    session.refresh(db_categorie)
    return db_categorie


def delete_categorie_by_id(id: int, session: Session) -> Categorie:
    db_categorie = session.get(Categorie, id)
    if not db_categorie:
        raise HTTPException(status_code=404, detail="Catégorie non trouvée")    
    session.delete(db_categorie)
    session.commit()
    session.refresh(db_categorie)
    return {'ok': True}