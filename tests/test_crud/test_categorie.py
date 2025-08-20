import pytest
from sqlmodel import Session
from app.crud.categorie import create_categorie
from app.schemas.categorie import CategorieCreate


@pytest.fixture
def categorie_data():
    return {
        "nom": "Categorie",
        "description": "Description de categorie test",
    }


def test_creer_categorie(session: Session, categorie_data):
    categorie_create = CategorieCreate(**categorie_data)
    categorie = create_categorie(categorie_create, session)

    assert categorie.id is not None
    assert categorie.nom == categorie_data["nom"]
    assert categorie.description == categorie_data["description"]