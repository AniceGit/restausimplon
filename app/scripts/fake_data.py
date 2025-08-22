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

def get_description(produit_nom):
    descriptions = {
        "Bruschetta": "Tranches de pain grillé garnies de tomates fraîches, d'ail, de basilic et d'huile d'olive.",
        "Soupe à l'oignon": "Soupe traditionnelle à base d'oignons caramélisés, bouillon de bœuf, et fromage gratiné.",
        "Salade César": "Salade croquante avec poulet grillé, croûtons, parmesan et sauce César.",
        "Poulet curry": "Poulet tendre cuit dans une sauce onctueuse au curry, accompagné de riz basmati.",
        "Steak frites": "Steak grillé à point, accompagné de frites dorées et croustillantes.",
        "Lasagnes": "Couches de pâtes, viande hachée, béchamel et fromage fondu, cuites au four.",
        "Tiramisu": "Dessert italien à base de biscuits imbibés de café, mascarpone et cacao.",
        "Crème brûlée": "Crème vanille recouverte d'une fine couche de sucre caramélisé.",
        "Moelleux au chocolat": "Gâteau moelleux avec un cœur coulant au chocolat noir.",
        "Coca-Cola": "Soda rafraîchissant à base de cola, parfait pour accompagner vos repas.",
        "Bière blonde": "Bière légère et désaltérante, avec des notes fruitées et une touche d'amertume.",
        "Eau gazeuse": "Eau minérale naturellement gazeuse, idéale pour se désaltérer.",
        "Jus d'orange": "Jus d'orange pressé, riche en vitamine C et plein de fraîcheur.",
        "Margherita": "Pizza classique avec sauce tomate, mozzarella, basilic frais et huile d'olive.",
        "Reine": "Pizza garnie de jambon, champignons, olives et fromage, un délice royal.",
        "4 Fromages": "Pizza généreuse avec une sélection de quatre fromages fondants.",
        "Calzone": "Pizza pliée en deux, garnie de jambon, fromage, champignons et sauce tomate.",
        "Cheeseburger": "Burger juteux avec steak haché, fromage fondu, salade, tomate et sauce spéciale.",
        "Double bacon burger": "Double steak haché, bacon croustillant, fromage, salade et sauce barbecue.",
        "Veggie burger": "Galette végétarienne à base de légumes et céréales, accompagnée de salade et sauce."
    }
    return descriptions.get(produit_nom, fake.sentence(nb_words=6))

def create_fake_data():
    with Session(engine) as session:
        try:
            # Créer catégories avec gestion d'erreur et logging
            categories_data = [
                {"nom": "Entrées", "description": "Délicieuses entrées"},
                {"nom": "Plats principaux", "description": "Repas copieux"},
                {"nom": "Desserts", "description": "Finissez en beauté"},
                {"nom": "Boissons", "description": "Boissons fraîches et chaudes"},
                {"nom": "Pizzas", "description": "Pizzas artisanales"},
                {"nom": "Burgers", "description": "Burgers maison"}
            ]
            
            print("Création des catégories...")
            categories_creees = []
            for cat_data in categories_data:
                # Vérifier l'attribut correct selon votre modèle
                # Utilisez soit 'nom' soit 'name' selon votre modèle Categorie
                existing = session.exec(select(Categorie).where(Categorie.nom == cat_data["nom"])).first()
                if not existing:
                    # Créer avec l'attribut correct (nom au lieu de name)
                    nouvelle_categorie = Categorie(nom=cat_data["nom"], description=cat_data["description"])
                    session.add(nouvelle_categorie)
                    categories_creees.append(nouvelle_categorie)
                    print(f"Catégorie créée: {cat_data['nom']}")
                else:
                    print(f"Catégorie existante: {cat_data['nom']}")
            
            session.commit()
            print(f"✅ {len(categories_creees)} nouvelles catégories créées")

            # Récupérer toutes les catégories après commit
            categories_db = session.exec(select(Categorie)).all()
            print(f"Total catégories en base: {len(categories_db)}")
            
            if not categories_db:
                raise Exception("Aucune catégorie trouvée en base de données")
            
            categories_map = {c.nom: c.id for c in categories_db}
            print(f"Mapping catégories: {categories_map}")

            # Créer produits avec gestion d'erreur
            produits_par_categorie = {
                "Entrées": ["Bruschetta", "Soupe à l'oignon", "Salade César"],
                "Plats principaux": ["Poulet curry", "Steak frites", "Lasagnes"],
                "Desserts": ["Tiramisu", "Crème brûlée", "Moelleux au chocolat"],
                "Boissons": ["Coca-Cola", "Bière blonde", "Eau gazeuse", "Jus d'orange"],
                "Pizzas": ["Margherita", "Reine", "4 Fromages", "Calzone"],
                "Burgers": ["Cheeseburger", "Double bacon burger", "Veggie burger"]
            }
            
            print("Création des produits...")
            produits_crees = 0
            for cat_name, produits_noms in produits_par_categorie.items():
                if cat_name not in categories_map:
                    print(f"⚠️  Catégorie '{cat_name}' non trouvée dans le mapping")
                    continue
                    
                categorie_id = categories_map[cat_name]
                for nom in produits_noms:
                    # Vérifier si le produit existe déjà
                    existing_produit = session.exec(select(Produit).where(Produit.nom == nom)).first()
                    if not existing_produit:
                        produit = Produit(
                            nom=nom,
                            description=get_description(nom),
                            prix=round(fake.pyfloat(min_value=5, max_value=25), 2),
                            stock=fake.random_int(min=5, max=100),
                            categorie_id=categorie_id
                        )
                        session.add(produit)
                        produits_crees += 1
                        print(f"Produit créé: {nom} (catégorie: {cat_name})")
                    else:
                        print(f"Produit existant: {nom}")
            
            session.commit()
            print(f"✅ {produits_crees} nouveaux produits créés")

            # Créer utilisateurs
            print("Création des utilisateurs...")
            roles_to_create = (
                [RoleEnum.admin] * 1 +
                [RoleEnum.employe] * 2 +
                [RoleEnum.client] * 7
            )
            utilisateurs = []
            utilisateurs_crees = 0
            for role_choisi in roles_to_create:
                email = fake.unique.email()
                existing_user = session.exec(select(Utilisateur).where(Utilisateur.email == email)).first()
                if not existing_user:
                    utilisateur = Utilisateur(
                        nom=fake.last_name(),
                        prenom=fake.first_name(),
                        adresse=fake.address().replace('\n', ', '),
                        telephone=fake.phone_number(),
                        email=email,
                        motdepasse="hashed_mdp",
                        role=role_choisi,
                        is_active=True
                    )
                    session.add(utilisateur)
                    utilisateurs.append(utilisateur)
                    utilisateurs_crees += 1
            
            session.commit()
            print(f"✅ {utilisateurs_crees} nouveaux utilisateurs créés")

            # Créer commandes et lignes de commandes
            print("Création des commandes...")
            produits = session.exec(select(Produit)).all()
            if not produits:
                print("⚠️  Aucun produit trouvé, impossible de créer des commandes")
                return
            
            # Récupérer tous les clients (pas seulement ceux créés dans cette session)
            clients = session.exec(select(Utilisateur).where(Utilisateur.role == RoleEnum.client)).all()
            if not clients:
                print("⚠️  Aucun client trouvé, impossible de créer des commandes")
                return
            
            commandes_creees = 0
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
                    produits_commande = random.sample(produits, min(num_lignes, len(produits)))
                    
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
                    commandes_creees += 1
            
            session.commit()
            print(f"✅ {commandes_creees} nouvelles commandes créées")
            print("🎉 Données tests générées avec succès!")
            
        except Exception as e:
            print(f"❌ Erreur lors de la génération des données: {str(e)}")
            session.rollback()
            raise

if __name__ == "__main__":
    create_fake_data()