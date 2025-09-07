# app/core/config.py
from pydantic_settings import BaseSettings
from pydantic import Field
from pathlib import Path

class Settings(BaseSettings):
    APP_NAME: str = "BlogApp"
    DEBUG: bool = True
    SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_EXPIRATION_HOURS: int

    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    UPLOAD_FOLDER: Path = Path(__file__).parent.parent / "media"
    ALLOWED_EXTENSIONS: list[str] = ["jpg", "jpeg", "png", "gif"]

    ADMIN_EMAIL: str
    ADMIN_PASSWORD: str

    class Config:
        env_file = ".env"


settings = Settings()