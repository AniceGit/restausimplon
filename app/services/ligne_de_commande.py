from sqlmodel import Session, select
from typing import List
from app.models.ligne_de_commande import LigneCommande
from datetime import datetime
from app.crud.commande import get_commande_by_id, create_commande
from app.schemas.commande import CommandeCreate
from app.crud.ligne_de_commande import get_ligne_commande_by_id, create_ligne_commande
from app.schemas.ligne_de_commande import LigneCommandeCreateWithoutCommandId, MontantCommande
from fastapi import HTTPException


# Récupérer les lignes de commandes d'une commande
def get_lignes_commandes_by_commande(commande_id: int, session: Session) -> List[LigneCommande]:
    statement = select(LigneCommande).where(LigneCommande.commande_id == commande_id)
    lignes_commande = session.exec(statement).all()
    if not lignes_commande:
        raise HTTPException(status_code=404, detail="Aucune ligne de commande trouvée pour cette commande")
    return lignes_commande


# Calcul automatique du montant total (prix * quantité).
def calculate_montant_total_commande(commande_id: int, session: Session) -> MontantCommande:
    lignes_commande = get_lignes_commandes_by_commande(commande_id, session)
    total = 0
    for ligne_commande in lignes_commande:
        montant_ligne = ligne_commande.quantite * ligne_commande.prix_unitaire
        total+= montant_ligne
    return MontantCommande(total=total)