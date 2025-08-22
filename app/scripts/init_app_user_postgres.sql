--Création d'un utilisateur applicatif avec mot de passe
CREATE USER app_user WITH PASSWORD 'motdepasseappuser';

--Donner accès à la base
GRANT CONNECT ON DATABASE restausimplon TO app_user;

--Donner accès au schéma public
GRANT USAGE ON SCHEMA public TO app_user;

--Autoriser lecture/écriture sur toutes les tables existantes
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO app_user;

--Autoriser l'accès aux séquences (pour les champs SERIAL / ID auto-incrémentés)
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO app_user;

--Pour que les futures tables/séquences aient automatiquement ces droits
ALTER DEFAULT PRIVILEGES IN SCHEMA public
    GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO app_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public
    GRANT USAGE, SELECT ON SEQUENCES TO app_user;