"""
Simple Proposal Processing Backend
Clean, minimal FastAPI application for proposal analysis and response generation
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
import uvicorn
import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from typing import List, Dict, Any, Optional

# Import only what we need
from services.simple_proposal import proposal_processor
from api.simple_proposal import router as simple_proposal_router
from api.auth import router as auth_router
from core.simple_database import get_db

# Simple FastAPI app
app = FastAPI(
    title="Simple Proposal Processing System",
    description="Clean, straightforward proposal analysis and response generation",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include only necessary routers
app.include_router(auth_router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(simple_proposal_router, prefix="/api/v1/simple", tags=["Simple Proposal"])

# JWT Configuration
SECRET_KEY = "your-super-secret-key-change-this-in-production-123456789"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Test user data - simple plain text for now
users_db = {
    "test@rfp.com": {
        "email": "test@rfp.com",
        "full_name": "Test User",
        "password": "test123456",  # Plain text for simplicity
        "role": "admin"
    }
}

# Pydantic models
class User(BaseModel):
    email: str
    full_name: str
    role: str

class UserInDB(User):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# Basic endpoints
@app.get("/")
async def root():
    return {
        "message": "Simple Proposal Processing System",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

@app.get("/info")
async def system_info():
    return {
        "system": "Simple Proposal Processing",
        "features": [
            "Proposal analysis",
            "Response generation",
            "Source tracking",
            "Document export",
            "Risk assessment"
        ],
        "endpoints": {
            "auth": "/api/v1/auth",
            "proposal": "/api/v1/simple"
        }
    }

if __name__ == "__main__":
    print("🚀 Starting Simple Proposal Processing System...")
    print("📍 API Documentation: http://localhost:8000/docs")
    print("🔍 Health Check: http://localhost:8000/health")
    print("📚 ReDoc: http://localhost:8000/redoc")
    print("=" * 60)
    
    uvicorn.run(
        "main_simple:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
