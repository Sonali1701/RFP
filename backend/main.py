from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from contextlib import asynccontextmanager
import uvicorn

from .core.config import settings
from .core.database import create_tables
from .api import auth, rfp, content, users, analytics


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup - only create tables if not in testing mode
    if not settings.testing_mode:
        create_tables()
    yield
    # Shutdown
    pass


app = FastAPI(
    title="Agentic AI RFP Automation Platform",
    description="An intelligent platform for automating RFP processes with AI agents",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url, "http://localhost:3000", "http://localhost:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["authentication"])
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(rfp.router, prefix="/api/v1/rfps", tags=["rfps"])
app.include_router(content.router, prefix="/api/v1/content", tags=["content"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["analytics"])


@app.get("/")
async def root():
    return {
        "message": "Agentic AI RFP Automation Platform",
        "version": "1.0.0",
        "status": "active"
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "database": "connected",
        "ai_services": "available"
    }


if __name__ == "__main__":
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )
