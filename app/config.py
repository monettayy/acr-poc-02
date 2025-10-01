import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/fastapi_db")
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: int = int(os.getenv("DB_PORT", "5432"))
    DB_NAME: str = os.getenv("DB_NAME", "fastapi_db")
    DB_USER: str = os.getenv("DB_USER", "postgres")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "password")
    
    # Application settings
    APP_NAME: str = os.getenv("APP_NAME", "FastAPI Backend")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"


settings = Settings()
