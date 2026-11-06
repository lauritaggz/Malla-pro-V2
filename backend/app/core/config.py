from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    environment: str = "development"
    database_url: str = "postgresql+asyncpg://mallapro:change-me@localhost:5432/mallapro"
    test_database_url: str = "postgresql+asyncpg://mallapro:change-me@localhost:5432/mallapro_test"
    # Comma-separated list. Kept as str: pydantic-settings would try to parse list[str] as JSON.
    cors_origins_raw: str = Field(default="http://localhost:5173", validation_alias="CORS_ORIGINS")
    # Local: path to the service-account file. Production: same JSON, base64-encoded (has priority).
    firebase_credentials_path: str = Field(
        default="firebase-sa.json", validation_alias="FIREBASE_CREDENTIALS_PATH"
    )
    firebase_credentials_json: str | None = Field(
        default=None, validation_alias="FIREBASE_CREDENTIALS_JSON"
    )

    # Prototype AI extraction (spike/ia-mallas). Only in backend/.env, never committed.
    anthropic_api_key: str | None = Field(default=None, validation_alias="ANTHROPIC_API_KEY")
    ai_model: str = Field(default="claude-sonnet-5-5", validation_alias="AI_MODEL")
    # Prototype history: one JSON per draft, one folder per user (gitignored).
    ai_drafts_dir: str = Field(default="ia-pruebas/historial", validation_alias="AI_DRAFTS_DIR")

    @property
    def cors_origins(self) -> list[str]:
        return [o.strip() for o in self.cors_origins_raw.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
