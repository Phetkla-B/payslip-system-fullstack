from datetime import datetime
from pydantic import BaseModel, ConfigDict

from app.schemas.payslip import PayslipResponse


class UploadHistoryResponse(BaseModel):
    # Allow Pydantic to read data from SQLAlchemy model
    model_config = ConfigDict(from_attributes=True)

    id: int
    file_name: str
    salary_month: int
    salary_year: int
    total_records: int
    success_records: int
    failed_records: int
    status: str
    error_details: str | None
    created_at: datetime

class UploadHistoryDetailResponse(BaseModel):
    # Read data from SQLAlchemy model
    model_config = ConfigDict(from_attributes=True)

    id: int
    file_name: str
    salary_month: int
    salary_year: int
    total_records: int
    success_records: int
    failed_records: int
    status: str
    error_detail: str | None
    created_at: datetime

    # Payslips import from this upload
    payslips: list[PayslipResponse]