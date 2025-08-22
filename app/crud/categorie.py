from http.client import HTTPException
from app.schemas.categorie import CategorieCreate
from sqlmodel import Session, select
from app.models.categorie import Categorie
from typing import List


def create_categorie(categorie: CategorieCreate, session: Session) -> Categorie:
    """
    Crée une nouvelle catégorie dans la base de données.

    Args:
        categorie (CategorieCreate): Les données de la catégorie à créer (nom, description, etc.).
        session (Session): La session SQLModel permettant l’interaction avec la base.

    Returns:
        Categorie: L’objet `Categorie` nouvellement créé avec son identifiant.
    """
    db_categorie = Categorie(**categorie.model_dump())
    session.add(db_categorie)
    session.commit()
    session.refresh(db_categorie)
    return db_categorie


def get_all_categories(session: Session) -> List[Categorie]:
    """
    Récupère toutes les catégories disponibles dans la base de données.

    Args:
        session (Session): La session SQLModel permettant l’interaction avec la base.

    Returns:
        List[Categorie]: La liste de toutes les catégories enregistrées.
    """
    statement = select(Categorie)
    return session.exec(statement).all()


def get_categorie_by_id(id: int, session: Session) -> Categorie:
    """
    Récupère une catégorie spécifique par son identifiant.

    Args:
        id (int): L’identifiant unique de la catégorie.
        session (Session): La session SQLModel permettant l’interaction avec la base.

    Returns:
        Categorie: L’objet `Categorie` correspondant à l’identifiant fourni.

    Raises:
        HTTPException (404): Si aucune catégorie n’existe avec cet identifiant.
    """
    db_categorie = session.get(Categorie, id)
    if not db_categorie:
        raise HTTPException(status_code=404, detail="Catégorie non trouvée")    
    return db_categorie
    

def update_categorie_by_id(id: int, categorie: Categorie, session: Session) -> Categorie:
    """
    Met à jour une catégorie existante par son identifiant.

    Args:
        id (int): L’identifiant de la catégorie à mettre à jour.
        categorie (Categorie): Les nouvelles données de la catégorie.
        session (Session): La session SQLModel permettant l’interaction avec la base.

    Returns:
        Categorie: L’objet `Categorie` mis à jour.

    Raises:
        HTTPException (404): Si aucune catégorie n’existe avec cet identifiant.
    """
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
    """
    Supprime une catégorie existante par son identifiant.

    Args:
        id (int): L’identifiant unique de la catégorie à supprimer.
        session (Session): La session SQLModel permettant l’interaction avec la base.

    Returns:
        Categorie: L’objet `Categorie` supprimé.

    Raises:
        HTTPException (404): Si aucune catégorie n’existe avec cet identifiant.
    """
    db_categorie = session.get(Categorie, id)
    if not db_categorie:
        raise HTTPException(status_code=404, detail="Catégorie non trouvée")    
    session.delete(db_categorie)
    session.commit()    
    return db_categorie
