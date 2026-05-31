from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base

# Upload history table
class UploadHistory(Base):
    __tablename__ = "upload_history"

    # Primary key
    id = Column(
        Integer,
        primary_key=True,
        index=True
    )
    
    # Upload file information
    file_name = Column(
        String(255),
        nullable=False
    )

    # Admin/HR user who uploaded the file
    uploaded_by_user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    # Salary period of uploaded payslip file
    salary_month = Column(
        Integer,
        nullable=False
    )

    salary_year = Column(
        Integer,
        nullable=False
    )

    # Upload result summary
    total_records = Column(
        Integer,
        nullable=False,
        default=0
    )

    success_records = Column(
        Integer,
        nullable=False,
        default=0
    )

    failed_records = Column(
        Integer,
        nullable=False,
        default=0
    )

    # Upload status: success, partial_failed, failed
    status = Column(
        String(20),
        nullable=False,
        default="success"
    )

    # Error details if upload failed
    error_details = Column(
        Text,
        nullable=True
    )

    # Audit field
    created_at = Column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )

    # Relationships
    payslips = relationship(
        "Payslip",
        back_populates="upload_history"
    )

    # Admin/HR user who uploaded the file
    uploaded_by_user = relationship(
        "User",
        back_populates="upload_histories"
    )