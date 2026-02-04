from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Endee Configuration
    ENDEE_HOST: str = "localhost"
    ENDEE_PORT: int = 8080
    ENDEE_TOKEN: Optional[str] = None
    
    # OpenAI Configuration
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-3.5-turbo"
    
    # Application Configuration
    APP_NAME: str = "Legal AI Assistant"
    DEBUG: bool = False
    INDEX_NAME: str = "legal_documents"
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    
    # CORS Configuration
    CORS_ORIGINS: list = ["http://localhost:3000", "http://127.0.0.1:3000"]
    
    class Config:
        env_file = ".env"

settings = Settings()