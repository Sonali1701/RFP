from pydantic_settings import BaseSettings
from typing import Optional, List
import os


class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql://user:password@localhost:5432/rfp_platform"
    database_test_url: str = "postgresql://user:password@localhost:5432/rfp_platform_test"
    
    # API Security
    secret_key: str = "your-secret-key-here"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # AI Services
    gemini_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    
    # Vector Database
    chroma_host: str = "localhost"
    chroma_port: int = 8000
    weaviate_url: str = "http://localhost:8080"
    
    # Redis
    redis_url: str = "redis://localhost:6379/0"
    
    # File Storage
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None
    aws_bucket_name: str = "rfp-documents"
    aws_region: str = "us-east-1"
    
    # Email
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_username: Optional[str] = None
    smtp_password: Optional[str] = None
    
    # Application
    debug: bool = True
    log_level: str = "INFO"
    max_file_size: str = "100MB"
    allowed_extensions: List[str] = ["pdf", "docx", "xlsx", "csv", "zip"]
    
    # Frontend
    frontend_url: str = "http://localhost:3000"
    
    # AI Model Settings
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    max_tokens: int = 4000
    temperature: float = 0.7
    
    # Processing Settings
    max_workers: int = 4
    chunk_size: int = 1000
    chunk_overlap: int = 200
    
    # Testing Mode
    testing_mode: bool = False
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
