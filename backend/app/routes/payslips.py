from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

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

# Gen PDF File
@router.get("/{payslip_id}/download")
def download_my_payslip_pdf(
    payslip_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Log PDF download request
    logger.info(f"Payslip PDF download request: user_id={current_user.id}, payslip_id={payslip_id}")

    # Query payslip by id and current user id
    payslip = db.query(Payslip).filter(
        Payslip.id == payslip_id,
        Payslip.user_id == current_user.id
    ).first()

    if payslip is None:
        logger.warning(
            f"Payslip PDF download failed: not found or access denied user_id={current_user.id}, "
            f"payslip_id={payslip_id}"
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payslip not found"
        )
    
    # Create PDF in memory
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)

    # PDF content
    pdf.setTitle(f"Payslip_{payslip.salary_month}_{payslip.salary_year}")

    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(50, 800, "Payslip")

    pdf.setFont("Helvetica", 11)
    pdf.drawString(50, 770, f"Employee Code: {payslip.employee_code}")
    pdf.drawString(50, 750, f"Citizen ID: {payslip.citizen_id}")
    pdf.drawString(50, 730, f"Department: {payslip.department or '-'}")
    pdf.drawString(50, 710, f"Position: {payslip.position or '-'}")
    pdf.drawString(50, 690, f"Period: {payslip.salary_month}/{payslip.salary_year}")

    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(50, 650, "Income")

    pdf.setFont("Helvetica", 11)
    pdf.drawString(70, 625, f"Base Salary: {payslip.base_salary}")
    pdf.drawString(70, 605, f"Paid Salary: {payslip.paid_salary}")
    pdf.drawString(70, 585, f"Allowance: {payslip.allowance}")
    pdf.drawString(70, 565, f"Overtime Pay: {payslip.overtime_pay}")
    pdf.drawString(70, 545, f"Bonus: {payslip.bonus}")
    pdf.drawString(70, 525, f"Other Income: {payslip.other_income}")
    pdf.drawString(70, 505, f"Adjust Amount: {payslip.adjust_amount}")
    pdf.drawString(70, 485, f"Special Amount: {payslip.special_amount}")

    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(300, 650, "Deduction")
    
    pdf.setFont("Helvetica", 11)
    pdf.drawString(320, 625, f"Expense Deduction: {payslip.expense_deduction}")
    pdf.drawString(320, 605, f"Social Security: {payslip.social_security}")
    pdf.drawString(320, 585, f"Provident Fund: {payslip.provident_fund}")
    pdf.drawString(320, 565, f"Tax: {payslip.tax}")
    pdf.drawString(320, 545, f"Other Deduction: {payslip.other_deduction}")

    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(300, 650, "Summary")

    pdf.setFont("Helvetica", 11)
    pdf.drawString(70, 405, f"Total Income: {payslip.total_income}")
    pdf.drawString(70, 385, f"Total Deduction: {payslip.total_deduction}")
    pdf.drawString(70, 365, f"Net Salary: {payslip.net_salary}")

    pdf.showPage()
    pdf.save()

    buffer.seek(0)

    file_name = f"payslip_{payslip.salary_month}_{payslip.salary_year}.pdf"

    logger.info(f"Payslip PDF download success: user_id={current_user.id}, payslip_id={payslip.id}")

    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename={file_name}"
        }
    )