import pytest
from sqlmodel import Session
from app.models.produit import Produit
from app.crud.produit import creer_produit
from app.schemas.produit import ProduitCreate
from app.schemas.categorie import CategorieCreate
from app.crud.categorie import create_categorie

import pytest
from sqlmodel import Session
from app.models.produit import Produit
from app.crud.produit import creer_produit
from app.schemas.produit import ProduitCreate
from app.schemas.categorie import CategorieCreate
from app.crud.categorie import create_categorie


@pytest.fixture
def categorie(session: Session):
    categorie_create = CategorieCreate(
        nom="CatTest",  # <= respecte max_length=10
        description="Catégorie test"
    )
    return create_categorie(categorie_create, session)


def test_creer_produit(session: Session, categorie):
    produit_create = ProduitCreate(
        nom="Produit Test",
        description="Description du produit test",
        prix=10.99,
        stock=100,
        categorie_id=categorie.id  # ✅ on utilise la vraie FK
    )

    produit = creer_produit(produit_create, session)

    assert produit.id is not None
    assert produit.nom == "Produit Test"
    assert produit.stock == 100
    assert produit.categorie_id == categorie.id
