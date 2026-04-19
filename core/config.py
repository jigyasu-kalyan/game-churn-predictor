# core/config.py

import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    # API Keys
    GROQ_API_KEY: Optional[str] = None
    
    # Path Configuration
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    PLAYBOOK_PATH: str = os.path.join(BASE_DIR, "retention_playbook.md")
    CHROMA_PATH: str = os.path.join(BASE_DIR, "chroma_db")
    MODEL_PATH: str = os.path.join(BASE_DIR, "churn_model.pkl")
    
    # Model Configuration
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    LLM_MODEL: str = "llama-3.3-70b-versatile"
    LLM_TEMPERATURE: float = 0.2
    
    # RAG Configuration
    RETRIEVAL_K: int = 2

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
