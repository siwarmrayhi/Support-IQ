from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    google_api_key: str
    jwt_secret: str
    access_token_minutes: int = 60
    llm_model: str = "gemini-3.5-flash-lite"
    embedding_model: str = "BAAI/bge-m3"
    embedding_device: str = "cpu"

    raw_data_dir: Path = PROJECT_ROOT / "data" / "raw"
    index_dir: Path = PROJECT_ROOT / "data" / "index"
    database_path: Path = PROJECT_ROOT / "data" / "supportiq.db"


settings = Settings()