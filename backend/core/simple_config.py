"""
Simple Configuration for Clean Proposal System
"""

import os
from typing import Optional

class SimpleSettings:
    """Simple settings class"""
    
    # Database
    database_url: str = "sqlite:///./simple_proposal.db"
    
    # API Security
    secret_key: str = "your-super-secret-key-change-this-in-production-123456789"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Testing mode
    testing_mode: bool = True
    
    # Debug
    debug: bool = True
    
    @classmethod
    def get_env_var(cls, key: str, default: str = None) -> str:
        """Get environment variable"""
        return os.getenv(key, default)

# Global settings instance
settings = SimpleSettings()
