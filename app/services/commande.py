from sqlmodel import Session, select
from typing import List
from app.models.commande import Commande
from app.models.ligne_de_commande import LigneCommande
from datetime import datetime
from app.crud.commande import get_commande_by_id, create_commande
from app.schemas.commande import CommandeCreate
from app.crud.ligne_de_commande import get_ligne_commande_by_id, create_ligne_commande
from app.schemas.ligne_de_commande import LigneCommandeCreateWithoutCommandId, LigneCommandeCreate
from fastapi import HTTPException


# méthode créer commande (utilisateur + liste d’articles + quantités)
# bloquer la méthode si problème avec ligne de commande, ou supprimer la commande
# ajouter le fait que comme le client ne peut faire une commande d'uavec son id
def create_commande_with_lignes_and_utilisateur(commande: CommandeCreate, lignes_commande: List[LigneCommandeCreateWithoutCommandId], session: Session) -> Commande:
    db_commande = create_commande(commande, session)
    print("commande id is", db_commande.id)
    for ligne_commande in lignes_commande:
        data_ligne_commande = ligne_commande.model_dump()
        data_ligne_commande["commande_id"] = db_commande.id
        new_ligne_commande = LigneCommandeCreate(**data_ligne_commande)
        create_ligne_commande(new_ligne_commande, session)
    return db_commande


# consulter les commandes par utilisateur
def get_commandes_by_utilisateur_id(utilisateur_id: int, session: Session) -> List[Commande]:
    statement = select(Commande).where(Commande.utilisateur_id == utilisateur_id)
    commande = session.exec(statement).all()
    if not commande:
        raise HTTPException(status_code=404, detail="Aucune commande trouvée pour ce utilisateur")
    return commande


# consulter les commandes par date - à améliorer
def get_commandes_by_date(date_commande: datetime, session: Session) -> List[Commande]:
    statement = select(Commande).where(Commande.date_commande == date_commande)
    commande = session.exec(statement).all()
    if not commande:
        raise HTTPException(status_code=404, detail="Aucune commande trouvée pour cette date")
    return commande
