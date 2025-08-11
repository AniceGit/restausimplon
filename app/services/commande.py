from sqlmodel import Session, select
from typing import List
from app.models.commande import Commande
from app.models.ligne_de_commande import LigneCommande
from datetime import datetime
from app.schemas.commande import CommandeCreate
from app.crud.ligne_de_commande import get_ligne_commande_by_id, create_ligne_commande
from app.schemas.ligne_de_commande import LigneCommandeCreateWithoutCommandId, LigneCommandeCreate
from fastapi import HTTPException
from sqlalchemy.orm import selectinload

# méthode créer commande (utilisateur + liste d’articles + quantités)
# bloquer la méthode si problème avec ligne de commande, ou supprimer la commande
# ajouter le fait que comme le client ne peut faire une commande d'uavec son id
def create_commande_with_lignes_and_utilisateur(commande: CommandeCreate, lignes_commande: List[LigneCommandeCreateWithoutCommandId], session: Session) -> Commande:
    db_commande = Commande(**commande.model_dump())
    prix_total = 0.0
    db_commande.prix_total = prix_total

    session.add(db_commande)
    session.flush()

    for ligne_commande in lignes_commande:
        prix_total_ligne = round(ligne_commande.quantite * ligne_commande.prix_unitaire, 2)
        prix_total += prix_total_ligne
        
        data_ligne_commande = ligne_commande.model_dump()
        data_ligne_commande["commande_id"] = db_commande.id
        data_ligne_commande["prix_total_ligne"] = prix_total_ligne

        new_ligne_commande = LigneCommande(**data_ligne_commande)
        session.add(new_ligne_commande)

    
    db_commande.prix_total = prix_total
    session.add(db_commande)
    session.commit()

    statement = select(Commande).where(Commande.id == db_commande.id).options(selectinload(Commande.lignes_commande))
    full_commande = session.exec(statement).one()

    return full_commande


# consulter les commandes par utilisateur
def get_commandes_by_utilisateur_id(utilisateur_id: int, session: Session) -> List[Commande]:
    statement = select(Commande).where(Commande.utilisateur_id == utilisateur_id).options(selectinload(Commande.lignes_commande))
    commande = session.exec(statement).all()
    if not commande:
        raise HTTPException(status_code=404, detail="Aucune commande trouvée pour cet utilisateur")
    return commande


# consulter les commandes par date - à améliorer
def get_commandes_by_date(date_commande: datetime, session: Session) -> List[Commande]:
    statement = select(Commande).where(Commande.date_commande == date_commande).options(selectinload(Commande.lignes_commande))
    commande = session.exec(statement).all()
    if not commande:
        raise HTTPException(status_code=404, detail="Aucune commande trouvée pour cette date")
    return commande
