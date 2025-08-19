from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Classe de configuration centralisée de l'application.

    Cette classe hérite de `BaseSettings` de Pydantic, ce qui permet de charger
    automatiquement les variables d'environnement depuis un fichier `.env` ou 
    directement depuis l'environnement système.

    Attributs :
        SECRET_KEY (str) :
            Clé secrète utilisée pour signer et vérifier les tokens JWT.
        
        ALGORITHM (str) :
            Algorithme utilisé pour le chiffrement JWT (ex: "HS256").
        
        ACCESS_TOKEN_EXPIRE_MINUTES (int) :
            Durée de vie d’un access token (en minutes).
        
        REFRESH_TOKEN_EXPIRE_DAYS (int) :
            Durée de vie d’un refresh token (en jours).
        
        DATABASE_URL (str) :
            URL de connexion à la base de données (ex: "postgresql://user:pass@localhost/dbname").
        
        POSTGRES_USER (str) :
            Nom d’utilisateur PostgreSQL.
        
        POSTGRES_PASSWORD (str) :
            Mot de passe PostgreSQL.
        
        POSTGRES_DB (str) :
            Nom de la base de données PostgreSQL.
        
        POSTGRES_DATA_PATH (str) :
            Répertoire de stockage des données PostgreSQL.
        
        POSTGRES_CONFIG_PATH (str) :
            Répertoire de stockage des fichiers de configuration PostgreSQL.
        
        POSTGRES_LOGS_PATH (str) :
            Répertoire de stockage des logs PostgreSQL.
        
        POSTGRES_BACKUPS_PATH (str) :
            Répertoire de stockage des sauvegardes PostgreSQL.
        
        BACKUP_SCHEDULE (str) :
            Fréquence de planification des sauvegardes (ex: "0 2 * * *" pour une sauvegarde quotidienne à 2h).
        
        BACKUP_RETENTION_DAYS (int) :
            Nombre de jours de conservation des sauvegardes.
    """

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int
    DATABASE_URL: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_DATA_PATH: str
    POSTGRES_CONFIG_PATH: str
    POSTGRES_LOGS_PATH: str
    POSTGRES_BACKUPS_PATH: str
    BACKUP_SCHEDULE: str
    BACKUP_RETENTION_DAYS: int

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

# Instance globale des paramètres
settings = Settings()
print(settings)
