 os
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    # Database
    DATABASE_URL: str = ""

    # JWT
    SECRET_KEY: str = "CHANGE_ME_TO_A_LONG_RANDOM_STRING"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    # IP Pool
    IP_POOL: List[str] = [
        "203.0.113.1",
        "203.0.113.2",
        "203.0.113.3",
    ]


settings = Settings()


# Build DATABASE_URL from Wasmer DB_* variables if DATABASE_URL is not provided
if not settings.DATABASE_URL:
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")
    db_username = os.getenv("DB_USERNAME")
    db_password = os.getenv("DB_PASSWORD")

    if all([db_host, db_port, db_name, db_username, db_password]):
        settings.DATABASE_URL = (
            f"postgresql://{db_username}:{db_password}"
            f"@{db_host}:{db_port}/{db_name}"
        )
    else:
        raise RuntimeError(
            "Database configuration is missing. "
            "Set DATABASE_URL or all DB_* variables."
