from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi import HTTPException, status
from .config import settings

# Only create database engine if not in testing mode
if not settings.testing_mode:
    # Create database engine
    engine = create_engine(
        settings.database_url,
        poolclass=StaticPool,
        connect_args={"check_same_thread": False} if "mysql" in settings.database_url else {},
        echo=settings.debug,
        # MySQL specific settings
        pool_pre_ping=True,
        pool_recycle=3600,
        pool_size=10,
        max_overflow=20
    )

    # Create session factory
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Create base class for models
    Base = declarative_base()


    def get_db():
        """Dependency to get database session"""
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()


    def create_tables():
        """Create all database tables"""
        Base.metadata.create_all(bind=engine)


    def drop_tables():
        """Drop all database tables"""
        Base.metadata.drop_all(bind=engine)
else:
    # Testing mode - don't create database engine
    engine = None
    SessionLocal = None
    Base = declarative_base()


    def get_db():
        """Testing mode - no database session"""
        raise HTTPException(status_code=503, detail="Database not available in testing mode")


    def create_tables():
        """Testing mode - don't create tables"""
        pass


    def drop_tables():
        """Testing mode - don't drop tables"""
        pass
