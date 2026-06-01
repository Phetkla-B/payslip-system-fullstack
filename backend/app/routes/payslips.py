from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.core.logger import logger
from app.models.user import User
from app.models.payslip import Payslip
from app.schemas.payslip import PayslipResponse

router = APIRouter()

@router.get("/", response_model=list[PayslipResponse])
def get_my_payslips(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Log current user payslip list request
    logger.info(f"Get payslip list request: user_id={current_user.id}")

    # Query only payslips that belong to current logged-in user
    payslips = db.query(Payslip).filter(
        Payslip.user_id == current_user.id
    ).order_by(
        Payslip.salary_year.desc(),
        Payslip.salary_month.desc()
    ).all()

    logger.info(
        f"Get payslip list success: user_id={current_user.id}, "
        f"total_records={len(payslips)}"
    )

    return payslips