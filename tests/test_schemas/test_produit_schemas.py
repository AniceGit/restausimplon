import pytest

from app.schemas.produit import ProduitCreate


def test_name_too_short_input_string(valid_product_create):
    # Arrange
    valid_product_create["nom"] = "" # empty input

    # Act & Assert
    with pytest.raises(ValueError): # Le test passe si ValueError est levée
       ProduitCreate(**valid_product_create)
    
    

def test_name_valid_input_string(valid_product_create):
    produit = ProduitCreate(**valid_product_create)
    
    # Assert
    assert produit.nom == valid_product_create["nom"]



def test_stock_thousands_separator_input_integer(valid_product_create):
    # Arrange
    valid_product_create["stock"] = 1,450 # input with thousands separator

    # Act & Assert
    with pytest.raises(ValueError): # Le test passe si ValueError est levée
        ProduitCreate(**valid_product_create)    
    


def test_stock_valid_input_integer(valid_product_create):
    produit = ProduitCreate(**valid_product_create)
    
    # Assert
    assert produit.stock == valid_product_create["stock"]



def test_price_negative_input_float(valid_product_create):
    # Arrange
    valid_product_create["prix"] = -20.50 # input with negative float

    # Act & Assert
    with pytest.raises(ValueError): # Le test passe si ValueError est levée
        ProduitCreate(**valid_product_create)    
    


def test_price_valid_input_float(valid_product_create):
    produit = ProduitCreate(**valid_product_create)
    
    # Assert
    assert produit.prix == valid_product_create["prix"]

