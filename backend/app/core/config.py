import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "School Knowledge RAG Assistant"
    API_V1_STR: str = "/api/v1"
    
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "llama3")
    
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "fallback_secret")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
    
    VECTOR_STORE_PATH: str = os.getenv("VECTOR_STORE_PATH", "../data/vector_store")
    EMBEDDING_MODEL_NAME: str = os.getenv("EMBEDDING_MODEL_NAME", "all-MiniLM-L6-v2")

    class Config:
        env_file = ".env"

settings = Settings()
