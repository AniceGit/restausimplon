import pytest
from fastapi import HTTPException
from app.models.produit import Produit
from sqlmodel import Session, select
from app.crud.produit import (
    get_all_produits,
    creer_produit,
    suppression_produit,
    modification_produit
)

@pytest.fixture
def produit_data():
    return {
        "nom": "Produit Test",
        "description": "Description du produit test",
        "prix": 10.99,
        "stock": 100,
        "categorie_id": 1
    }

@pytest.fixture
def produit_existant(session, produit_data):
    # Crée un vrai objet SQLModel pour éviter les erreurs de model_dump
    produit = Produit(**produit_data)
    session.add(produit)
    session.commit()
    session.refresh(produit)
    return produit

def test_creer_produit(session, produit_data):
    produit = Produit(**produit_data)
    session.add(produit)
    session.commit()
    session.refresh(produit)
    assert produit.id is not None
    assert produit.nom == produit_data["nom"]

def test_get_all_produits(session, produit_existant):
    produits = get_all_produits(session)
    assert len(produits) >= 1
    assert any(p.nom == produit_existant.nom for p in produits)

def test_modification_produit(session, produit_existant):
    updated = modification_produit(
        session, 
        produit_existant.id, 
        {"prix": 20.0}
    )
    assert updated.prix == 20.0

def test_modification_produit_inexistant(session: Session):
    with pytest.raises(HTTPException) as excinfo:
        modification_produit(session, 999, {"prix": 20.0})
    assert excinfo.value.status_code == 404

def test_suppression_produit(session, produit_existant):
    suppression_produit(session, produit_existant.id)
    produits = get_all_produits(session)
    assert all(p.id != produit_existant.id for p in produits)

def test_suppression_produit_inexistant(session):
    with pytest.raises(HTTPException) as excinfo:
        suppression_produit(session, 999)
    assert excinfo.value.status_code == 404