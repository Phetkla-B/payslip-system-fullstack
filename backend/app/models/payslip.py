from sqlalchemy import Column, Integer, String, DateTime, Numeric, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base

# Payslip table
class Payslip(Base):
    __tablename__ = "payslips"

    # Prevent duplicate payslip for same user in same month/year
    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "salary_month",
            "salary_year",
            name="uq_user_salary_month_year"
        ),
    )

    # Primary key
    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # Link to users table
    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    # Link to upload_history table
    upload_history_id = Column(
        Integer,
        ForeignKey("upload_history.id"),
        nullable=True,
        index=True
    )

    # Employee reference data from excel
    employee_code = Column(
        String(20),
        nullable=False,
        index=True
    )

    citizen_id = Column(
        String(13),
        nullable=False,
        index=True
    )

    department = Column(
        String(100),
        nullable=True
    )

    position = Column(
        String(100),
         nullable=True
    )

    # Salary period
    salary_month = Column(
        Integer,
        nullable=False
    )

    salary_year = Column(
        Integer,
        nullable=False
    )

    # Income items
    base_salary = Column(
        Numeric(12, 2),
        nullable=False,
        default=0
    )

    paid_salary = Column(
        Numeric(12, 2),
        nullable=False,
        default=0
    )

    allowance = Column(
        Numeric(12, 2),
        nullable=False,
        default=0
    )

    overtime_pay = Column(
        Numeric(12, 2),
        nullable=False,
        default=0
    )

    bonus = Column(
        Numeric(12, 2),
        nullable=False,
        default=0
    )

    other_income = Column(
        Numeric(12, 2),
        nullable=False,
        default=0
    )

    adjust_amount = Column(
        Numeric(12, 2),
        nullable=False,
        default=0
    )

    special_amount = Column(
        Numeric(12, 2),
        nullable=False,
        default=0
    )

    # Deduction items
    expense_deduction = Column(
        Numeric(12, 2),
        nullable=False,
        default=0
    )

    social_security = Column(
        Numeric(12, 2),
        nullable=False,
        default=0
    )

    provident_fund = Column(
        Numeric(12, 2),
        nullable=False,
        default=0
    )

    tax = Column(
        Numeric(12, 2),
        nullable=False,
        default=0
    )

    other_deduction = Column(
        Numeric(12, 2),
        nullable=False,
        default=0
    )

    # Summary
    total_income = Column(
        Numeric(12, 2),
        nullable=False,
        default=0
    )

    total_deduction = Column(
        Numeric(12, 2),
        nullable=False,
        default=0
    )

    net_salary = Column(
        Numeric(12, 2),
        nullable=False,
        default=0
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
    user = relationship(
        "User",
        back_populates="payslips"
    )

    upload_history = relationship(
        "UploadHistory",
        back_populates="payslips"
    )