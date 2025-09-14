"""
Configuration settings for the backend application.
"""

from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Application
    APP_NAME: str = "Instantly Backend"
    DEBUG: bool = False
    API_PREFIX: str = "/api"
    
    # Security
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"
    
    # Database
    MONGODB_URL: str
    REDIS_URL: str
    
    # LLM
    OPENAI_API_KEY: Optional[str] = None
    HF_API_KEY: Optional[str] = None
    
    # Sandbox
    DOCKER_REGISTRY: str = "localhost:5000"
    SANDBOX_IMAGE: str = "instantly-sandbox:latest"
    MAX_SANDBOX_MEMORY: str = "2g"
    SANDBOX_CPU_LIMIT: float = 1.0
    
    class Config:
        env_file = ".env"

settings = Settings()