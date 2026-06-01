from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.core.logger import logger
from app.models.user import User
from app.models.payslip import Payslip
from app.schemas.payslip import PayslipResponse

router = APIRouter()

# Endpoint to get current user's payslip list
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


@router.get("/{payslip_id}", response_model=PayslipResponse)
def get_my_payslip_detail(
    payslip_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Log payslip detail request
    logger.info(f"Get payslip detail request: user_id{current_user.id}, payslip_id={payslip_id}")

    # Query payslip by id and current user id
    payslip = db.query(Payslip).filter(
        Payslip.id == payslip_id,
        Payslip.user_id == current_user.id
    ).first()

    # If not found, return 404
    # This also prevents users from seeing other users' payslips
    if payslip is None:
        logger.warning(f"Payslip not found or access denied: user_id={current_user.id}, payslip_i{payslip_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payslip not found"
        )
    
    logger.info(f"Get payslip detail success: user_id={current_user.id}, payslip_id={payslip_id}")

    return payslip