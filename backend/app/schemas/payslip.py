from decimal import Decimal
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class PayslipResponse(BaseModel):
    # Allow Pydantic ti read data from SQLAlchemy model
    model_config = ConfigDict(from_attributes=True)

    # Basic information
    id: int
    employee_code: str
    citizen_id: str
    department: str | None
    position: str | None
    salary_month: int
    salary_year: int

    # Salary details
    base_salary: Decimal
    paid_salary: Decimal
    allowance: Decimal
    overtime_pay: Decimal
    bonus: Decimal
    other_income: Decimal
    adjust_amount: Decimal
    special_amount: Decimal

    # Deductions
    expense_deduction: Decimal
    social_security: Decimal
    provident_fund: Decimal
    tax: Decimal
    total_deduction: Decimal

    # Calculated fields
    total_income: Decimal
    total_deduction: Decimal
    net_salary: Decimal

    # Audit fields
    created_at: datetime
    updated_at: datetime