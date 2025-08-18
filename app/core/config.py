from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int
    DATABASE_URL: str
    POSTGRES_USER : str
    POSTGRES_PASSWORD : str
    POSTGRES_DB : str
    POSTGRES_DATA_PATH : str
    POSTGRES_CONFIG_PATH : str
    POSTGRES_LOGS_PATH : str
    POSTGRES_BACKUPS_PATH : str
    BACKUP_SCHEDULE : str
    BACKUP_RETENTION_DAYS : int

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

settings = Settings()
print(settings)