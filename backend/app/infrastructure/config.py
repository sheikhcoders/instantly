import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "Intelligent Conversation Agent System"
    VERSION: str = "1.0.0"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "mongodb://localhost:27017")
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    SANDBOX_URL: str = os.getenv("SANDBOX_URL", "http://localhost:8001")

settings = Settings()
