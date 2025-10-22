"""
Configuration settings for English Assistant backend
"""
import os
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # API Configuration
    api_host: str = "localhost"
    api_port: int = 8000
    api_debug: bool = True
    
    # Database Configuration
    database_url: str = "postgresql://english_assistant_user:password@localhost:5432/english_assistant"
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "english_assistant"
    db_user: str = "english_assistant_user"
    db_password: str = "password"
    
    # Security
    secret_key: str = "your-secret-key-change-in-production"
    cors_origins: List[str] = ["http://localhost:3000", "http://localhost:8080"]
    
    # Model Configuration
    models_cache_dir: str = "./models_cache"
    hf_home: str = "./models_cache"
    
    # Logging
    log_level: str = "INFO"
    log_file: str = "logs/english_assistant.log"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()