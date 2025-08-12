import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from sqlmodel import Session, select
from faker import Faker
import random
from datetime import datetime, timedelta

from app.models.utilisateur import Utilisateur, RoleEnum
from app.models.produit import Produit
from app.models.commande import Commande, CommandeStatusEnum
from app.models.categorie import Categorie
from app.models.ligne_de_commande import LigneCommande
from app.database import engine

fake = Faker("fr_FR")

def create_fake_data():
    with Session(engine) as session:
        # Créer catégories
        categories = [
            {"nom": "Entrées", "description": "Délicieuses entrées"},
            {"nom": "Plats principaux", "description": "Repas copieux"},
            {"nom": "Desserts", "description": "Finissez en beauté"},
            {"nom": "Boissons", "description": "Boissons fraîches et chaudes"},
            {"nom": "Pizzas", "description": "Pizzas artisanales"},
            {"nom": "Burgers", "description": "Burgers maison"}
        ]
        for cat in categories:
            existing = session.exec(select(Categorie).where(Categorie.nom == cat["nom"])).first()
            if not existing:
                session.add(Categorie(name=cat["nom"], description=cat["description"]))
        session.commit()

        # Créer produits
        produits_par_categorie = {
            "Entrées": ["Bruschetta", "Soupe à l'oignon", "Salade César"],
            "Plats principaux": ["Poulet curry", "Steak frites", "Lasagnes"],
            "Desserts": ["Tiramisu", "Crème brûlée", "Moelleux au chocolat"],
            "Boissons": ["Coca-Cola", "Bière blonde", "Eau gazeuse", "Jus d’orange"],
            "Pizzas": ["Margherita", "Reine", "4 Fromages", "Calzone"],
            "Burgers": ["Cheeseburger", "Double bacon burger", "Veggie burger"]
        }

        categories = {c.nom: c.id for c in session.exec(select(Categorie)).all()}

        for cat_name, produits in produits_par_categorie.items():
            for nom in produits:
                produit = Produit(
                    nom=nom,
                    description=fake.sentence(nb_words=6),
                    prix=round(fake.pyfloat(min_value=5, max_value=25), 2),
                    stock=fake.random_int(min=5, max=100),
                    categorie_id=categories[cat_name]
                )
                session.add(produit)
        session.commit()

        # Créer utilisateurs
        roles_to_create = (
            [RoleEnum.admin] * 1 +
            [RoleEnum.employe] * 2 +
            [RoleEnum.client] * 7
        )

        utilisateurs = []
        for role_choisi in roles_to_create:
            utilisateur = Utilisateur(
                nom=fake.last_name(),
                prenom=fake.first_name(),
                adresse=fake.address().replace('\n', ', '),
                telephone=fake.phone_number(),
                email=fake.unique.email(),
                motdepasse="hashed_mdp",
                role=role_choisi,
                is_active=True
            )
            session.add(utilisateur)
            utilisateurs.append(utilisateur)
        session.commit()

        # Créer commandes et lignes de commandes
        produits = session.exec(select(Produit)).all()

        # On garde que les clients pour créer des commandes
        clients = [u for u in utilisateurs if u.role == RoleEnum.client]

        for _ in range(30):
            with session.no_autoflush:
                commande = Commande(
                    utilisateur_id=random.choice(clients).id,
                    date_commande=fake.date_time_between(start_date="-30d", end_date="now"),
                    statut=random.choice(list(CommandeStatusEnum)),
                    prix_total=0.0  # Valeur temporaire
                )
                session.add(commande)
                session.flush()  # Pour générer commande.id

                total = 0
                num_lignes = random.randint(1, 4)
                produits_commande = random.sample(produits, num_lignes)

                for produit in produits_commande:
                    quantite = random.randint(1, 5)
                    prix_unitaire = produit.prix
                    prix_total_ligne = round(quantite * prix_unitaire, 2)

                    ligne = LigneCommande(
                        commande_id=commande.id,
                        produit_id=produit.id,
                        quantite=quantite,
                        prix_unitaire=prix_unitaire,
                        prix_total_ligne=prix_total_ligne
                    )
                    total += prix_total_ligne
                    session.add(ligne)

                commande.prix_total = round(total, 2)

        session.commit()


        print("Données tests générées avec succès.")

if __name__ == "__main__":
    create_fake_data()