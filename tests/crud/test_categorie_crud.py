from app.crud.categorie import Categorie
from app.crud.categorie import get_all_categories, create_categorie
import pytest    

def test_create_categorie(categorie_fixture_create, session):
    response = create_categorie(categorie_fixture_create, session)
    assert response == Categorie(nom='test', id=1, description='ceci est un test')

def test_get_all_categorie(session):
    response = get_all_categories(session)
    assert response == [Categorie(nom='test', id=1, description='ceci est un test')]