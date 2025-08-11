# API RestauSimplon

Système de gestion de commandes pour un restaurant



## Description du projet :


Nous sommes développeur·euse backend au sein d’une start‑up tech spécialisée dans les solutions métier.
Notre nouveau client, RestauSimplon, souhaite digitaliser la gestion de ses commandes, de ses clients et des articles du menu.
Aujourd’hui, tout se fait sur papier : erreurs fréquentes et temps de traitement élevés.



## Technologies du projet :


- API REST complète sous FastAPI

- Bibliothèque SQLModel de type ORM (Object Relational Mapping) pour une conversion bidirectionnelle entre les objets issus de Python et la base de données relationnelle sous SQL

- Authentification & Autorisation par jetons (JWT)

- Conteneurisation via Docker & Docker Compose

- CI/CD & tests automatisés (GitHub Actions ou GitLab CI, pytest)



## Lancement du projet :


La première étape consiste à cloner le dépôt Git depuis l'URL en ligne vers votre machine locale. Cela crée une copie complète du projet, y compris tout l'historique des commits.
Ouvrez votre terminal de VS Code ou votre invite de commandes et utilisez la commande "git clone https://github.com/AniceGit/restausimplon.git". Cette commande va créer un dossier avec le nom du dépôt "restausimplon" et télécharger tous les fichiers du projet à l'intérieur.

Après avoir cloné le dépôt, vous devez vous déplacer dans le dossier qui vient d'être créé pour pouvoir travailler sur le projet en utilisant la commande "cd restausimplon" dans votre terminal de VS Code.

Le projet nécessite l'installation des dépendences pour pouvoir fonctionner. Ces dernières sont listées dans un fichier "requirements.txt" présent dans le dossier à la racine du projet. Pour ce faire, dans le terminal de VS Code de votre environnement virtuel, vous utilisez la commande suivante : "pip install -r requirements.txt".

Une fois les dépendances installées, vous pouvez lancer le serveur Uvicorn avec la commande "uvicorn app.main:app --reload" dans votre terminal de VS Code. Un fichier "restausimplon.sql" sera créé dans le dossier à la racine du projet. Ensuite, sur votre navigateur web, vous tapez l'adresse URL suivante : http://127.0.0.1:8000/docs/ qui vous dirigera vers l'interface Swagger/OpenAPI de l'API RestauSimplon.



## Fonctionnalités du projet :


1. Authentification & Autorisation


    - Création de comptes (admin, employé, client).


    - Flux OAuth2 Password avec access & refresh tokens JWT.


    - Rôles / scopes appliqués via FastAPI. 


    - Sécurité : hashage Bcrypt, rotation / expirations paramétrables.


2. Gestion des articles du menu


    - CRUD complet.


    - Champs : nom, prix, catégorie, description , stock.


    - Gestion des clients


    - CRUD complet.


    - Champs : nom, prénom, adresse, téléphone, email.


    - Un client peut s’inscrire/demander une commande via API ou interface graphique. Le client ne peut commander que pour lui-même.


3. Gestion des commandes


    - Endpoints :

        + créer commande (client + liste d’articles + quantités). Le staff peut commander pour n'importe quel client.
        + consulter les commandes par client
        + consulter les commandes par date


    - Calcul automatique du montant total (prix * quantité).


    - Statut de commande (En préparation, Prête, Servie)


4. Validation & Intégrité des données


    - Pydantic v2 models, validators custom.


    - Règles : prix > 0, quantité ≥ 1, email valide, commande ≥ 1 article, etc.




