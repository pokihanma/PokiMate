from pydantic_settings import BaseSettings
from typing import List
from functools import lru_cache


class Settings(BaseSettings):
    astra_env: str = "dev"
    astra_db_dir: str = "./data"
    astra_jwt_secret: str = "change-me-in-production"
    astra_jwt_access_minutes: int = 30
    astra_jwt_refresh_days: int = 30
    astra_cors_origins: str = "http://localhost:3000,http://localhost:1420"
    astra_ai_mode: str = "OFF"  # OFF | LIGHT | FULL
    astra_offline_mode: bool = False
    astra_drive_enabled: bool = False
    astra_google_client_id: str = ""
    astra_google_client_secret: str = ""
    astra_google_redirect_uri: str = "http://localhost:8000/sync/oauth/callback"
    astra_backup_passphrase_hint: str = ""
    astra_encryption_kdf: str = "argon2id"  # argon2id | scrypt
    astra_encryption_salt: str = ""
    astra_sync_folder_name: str = "Pokimate_Backups"
    astra_ai_service_url: str = "http://localhost:8001"

    class Config:
        env_file = ".env"
        env_prefix = "ASTRA_"
        case_sensitive = False

    @property
    def database_url(self) -> str:
        import os
        os.makedirs(self.astra_db_dir, exist_ok=True)
        return f"sqlite:///{os.path.join(self.astra_db_dir, 'pokimate.db')}"

    @property
    def cors_origins_list(self) -> List[str]:
        return [o.strip() for o in self.astra_cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
