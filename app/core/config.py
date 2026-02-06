from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # --- Database ---
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    # --- JWT ---
    JWT_ACCESS_SECRET_KEY: str
    JWT_REFRESH_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # --- Redis ---
    REDIS_URL: str

    BASE_DIR: Path = Path(__file__).parent.parent

    class Config:
        env_file = ".env"


settings = Settings()
