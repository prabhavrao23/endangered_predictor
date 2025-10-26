# utils/config.py
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # API Settings
    API_VERSION: str = "v1"
    API_TITLE: str = "Endangered Species ML API"
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "https://yourfrontend.com"]
    
    # Model Paths
    MODEL_DIR: str = "models/weights"
    
    # Database
    DATABASE_URL: str = "postgresql://user:pass@localhost/endangered_species"
    
    # Redis Cache
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    
    # Storage
    S3_BUCKET: str = "endangered-species-data"
    
    # Model Settings
    MAX_IMAGE_SIZE_MB: int = 10
    BATCH_SIZE: int = 32
    
    class Config:
        env_file = ".env"