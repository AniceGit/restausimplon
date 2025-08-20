import pytest
from sqlmodel import Session
from app.models.produit import Produit
from app.crud.produit import creer_produit, suppression_produit, modification_produit
from app.schemas.produit import ProduitCreate
from app.schemas.categorie import CategorieCreate
from app.crud.categorie import create_categorie
import uuid



@pytest.fixture
def categorie(session: Session):
    categorie_create = CategorieCreate(
        nom=f"Cat_{uuid.uuid4().hex[:6]}",
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

def test_modification_produit(session: Session, categorie):
    """✅ Test de modification d’un produit"""
    # On crée d'abord un produit
    produit_create = ProduitCreate(
        nom="Produit Modif",
        description="Ancienne description",
        prix=20.0,
        stock=50,
        categorie_id=categorie.id
    )
    produit = creer_produit(produit_create, session)

    # On modifie certains champs
    produit_modifie = modification_produit(
        produit.id,
        {"nom": "Produit Modifié", "stock": 75},
        session
    )

    assert produit_modifie.nom == "Produit Modifié"
    assert produit_modifie.stock == 75
    assert produit_modifie.description == "Ancienne description"  # non modifié
    assert produit_modifie.categorie_id == categorie.id


def test_suppression_produit(session: Session, categorie):
    """✅ Test de suppression d’un produit"""
    # Création d'un produit
    produit_create = ProduitCreate(
        nom="Produit Supp",
        description="Produit à supprimer",
        prix=15.0,
        stock=10,
        categorie_id=categorie.id
    )
    produit = creer_produit(produit_create, session)

    # Suppression
    produit_supprime = suppression_produit(produit.id, session)

    assert produit_supprime.id == produit.id

    # Vérifier qu'il n'existe plus en base
    produit_check = session.get(Produit, produit.id)
    assert produit_check is None