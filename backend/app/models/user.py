from datetime import datetime
from sqlalchemy import (
    Column, 
    Integer, 
    String,
    DateTime
)

from app.core.database import Base

# User Table
class User(Base):
    __tablename__ = "users"

    # Primary key
    id = Column(
        Integer, 
        primary_key=True, 
        index=True
    )
        
    # Login information
    username = Column(
        String(50), 
        unique=True, 
        index=True,
        nullable=False
        )
    
    email = Column(
        String(255), 
        unique=True, 
        index=True,
        nullable=False
    )

    citizen_id = Column(
        String(13), 
        unique=True, 
        index=True,
        nullable=False
    )

    # Security
    hashed_password = Column(
        String(255), 
        nullable=False
    )

    # Authorization
    role = Column(
        String(50), 
        nullable=False,
        default="user"
    )

    # Audit fields
    created_at = Column(
        DateTime, 
        default=datetime.utcnow,
        nullable=False
    )

    updated_at = Column(
        DateTime, 
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )