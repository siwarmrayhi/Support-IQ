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
    llm_model: str = "gemini-2.5-flash"
    embedding_model: str = "BAAI/bge-m3"
    embedding_device: str = "cpu"

    raw_data_dir: Path = PROJECT_ROOT / "data" / "raw"
    index_dir: Path = PROJECT_ROOT / "data" / "index"


settings = Settings()