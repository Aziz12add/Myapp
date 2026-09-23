from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Database
    DATABASE_URL: str = "postgresql://user:pass@db:5432/vpnpanel"

    # JWT
    SECRET_KEY: str = "CHANGE_ME_TO_A_LONG_RANDOM_STRING"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # IP Pool (در نسخهٔ واقعی بهتر است در دیتابیس باشد)
    IP_POOL: List[str] = [
        "203.0.113.1",
        "203.0.113.2",
        "203.0.113.3",
    ]

settings = Settings()
