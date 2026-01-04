from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    APP_NAME: str = "IRSS COMMAND API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: str
    DATABASE_URL_ASYNC: str | None = None
    
    # Security
    SECRET_KEY: str
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:8080", "http://localhost:3000"]
    
    # API
    API_V1_PREFIX: str = "/api/v1"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

