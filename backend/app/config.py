from pathlib import Path

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

_env_path = Path(__file__).resolve().parent.parent / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(_env_path), env_file_encoding="utf-8", extra="ignore"
    )

    # Supabase
    supabase_url: str
    supabase_anon_key: str
    supabase_service_role_key: str

    # Postgres (direct connection for Alembic / SQLAlchemy)
    database_url: str

    # OpenAI / Groq (OpenAI-compatible API)
    openai_api_key: str
    openai_base_url: str = "https://api.groq.com/openai/v1"
    openai_embedding_model: str = "text-embedding-3-small"
    openai_embedding_dimensions: int = 1536

    # Server
    allowed_origins: str = "http://localhost:5173"

    @computed_field
    @property
    def cors_origins(self) -> list[str]:
        return [
            origin.strip()
            for origin in self.allowed_origins.split(",")
            if origin.strip()
        ]


settings = Settings()
