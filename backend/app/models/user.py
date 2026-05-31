from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

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

    # Employee information
    employee_code = Column(
        String(20),
        unique=True,
        nullable=False,
        index=True
    )

    citizen_id = Column(
        String(13),
        unique=True,
        nullable=False,
        index=True
    )

    first_name = Column(
        String(100), 
        nullable=False
    )

    last_name = Column(
        String(100), 
        nullable=False
    )

    email = Column(
        String(255), 
        unique=True, 
        nullable=False
    )

    # Login information
    hashed_password = Column(
        String(255), 
        nullable=False
    )

    # admin / employee
    role = Column(
        String(20), 
        nullable=False,
        default="employee"
    )

    # Audit fields
    created_at = Column(
        DateTime, 
        server_default=func.now(),
        nullable=False
    )

    updated_at = Column(
        DateTime, 
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    # Relationships
    payslips = relationship(
        "Payslip",
        back_populates="user"
    )

    # Relationship to upload history
    upload_histories = relationship(
        "UploadHistory",
        back_populates="uploaded_by_user"
    )