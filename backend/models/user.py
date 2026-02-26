from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
import enum

# Create Base directly instead of importing from database
Base = declarative_base()


class UserRole(enum.Enum):
    ADMIN = "admin"
    PROPOSAL_MANAGER = "proposal_manager"
    SALES = "sales"
    SME = "sme"
    COMPLIANCE = "compliance"
    EXECUTIVE = "executive"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.SALES)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    
    # Profile information
    phone = Column(String(20))
    department = Column(String(100))
    title = Column(String(100))
    bio = Column(Text)
    
    # Expertise areas for SMEs
    expertise_areas = Column(Text)  # JSON string of expertise areas
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True))
    
    # Relationships
    rfps_assigned = relationship("RFP", back_populates="assigned_user")
    responses_created = relationship("Response", back_populates="created_by_user")
    comments = relationship("Comment", back_populates="author")
    approvals = relationship("Approval", back_populates="approver")
