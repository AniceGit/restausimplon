from app.models.categorie import Categorie
from fastapi import APIRouter, Depends
from sqlmodel import Session
from typing import List


from app.database import get_session
from app.schemas.categorie import CategorieCreate
from app.schemas.categorie import CategorieRead
from app.schemas.categorie import CategorieUpdate
from app.schemas.categorie import CategorieDelete
from app.crud.categorie import create_categorie
from app.crud.categorie import get_all_categories
from app.crud.categorie import get_categorie_by_id
from app.crud.categorie import update_categorie_by_id
from app.crud.categorie import delete_categorie_by_id


router = APIRouter(prefix="/categories", tags=["Categories"])


@router.post("/", response_model=CategorieCreate)
def add_categorie(categorie: CategorieCreate, session: Session = Depends(get_session)):
    return create_categorie(categorie, session)


@router.get("/", response_model=List[CategorieRead])
def read_categories(session: Session = Depends(get_session)):
    return get_all_categories(session)


@router.get("/{id}", response_model=CategorieRead)
def read_one_categorie(id: int, session: Session = Depends(get_session)):
    return get_categorie_by_id(id, session)



@router.patch("/", response_model=CategorieUpdate)
def update_one_categorie(id: int, categorie: Categorie, session: Session = Depends(get_session)):
    return update_categorie_by_id(id, categorie, session)



@router.delete("/", response_model=CategorieDelete)
def delete_one_categorie(id: int, session: Session = Depends(get_session)):
    return delete_categorie_by_id(id, session)

