from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # JWT configuration
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Database configuration
    DATABASE_URL: str

    # Load environment variables from .env file
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

settings = Settings()