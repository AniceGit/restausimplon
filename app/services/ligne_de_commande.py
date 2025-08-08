from sqlmodel import Session, select
from typing import List
from app.models.ligne_de_commande import LigneCommande
from fastapi import HTTPException


# Récupérer les lignes de commandes d'une commande
def get_lignes_commandes_by_commande(commande_id: int, session: Session) -> List[LigneCommande]:
    statement = select(LigneCommande).where(LigneCommande.commande_id == commande_id)
    lignes_commande = session.exec(statement).all()
    if not lignes_commande:
        raise HTTPException(status_code=404, detail="Aucune ligne de commande trouvée pour cette commande")
    return lignes_commande
