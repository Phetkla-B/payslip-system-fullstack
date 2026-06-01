from fastapi import APIRouter, Depends, File, UploadFile, Form, HTTPException, status
from sqlalchemy.orm import Session
from decimal import Decimal
from io import BytesIO
import pandas as pd

from app.core.database import get_db
from app.core.dependencies import require_admin
from app.core.logger import logger
from app.models.user import User
from app.models.upload_history import UploadHistory
from app.models.payslip import Payslip
from app.schemas.upload_history import UploadHistoryResponse

router = APIRouter()

# Helper function to convert Excel value to Decimal
def to_decimal(value) -> Decimal:
    # Convert empty value to Decimal 0
    if pd.isna(value) or str(value).strip() == "":
        return Decimal("0")
    
    # Remove comma from number string
    clean_value = str(value).replace(",", "").strip()
    
    # Convert value to Decimal using string to avoid float precision issue
    return Decimal(clean_value)

# Helper function to read value from multiple possible column names
def get_row_value(row, possible_columns, default=None):
    # Read value from the first matching column name
    for column in possible_columns:
        if column in row:
            return row.get(column)
        
    return default

def clean_text(value):
    # Convert empty, None, or NaN to empty string
    if pd.isna(value):
        return ""
    
    # Convert value to string
    text = str(value).strip()

    # Remove trailing 0. from Excel numeric value
    if text.endswith(".0"):
        text = text[:-2]

    return text

# Admin-only endpoint to upload payslip
@router.post("/upload-payslip")
def upload_payslip(
    salary_month: int = Form(...),
    salary_year: int = Form(...),
    file: UploadFile = File(...),
    current_admin: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    # Log upload attempt
    logger.info(
        f"Payslip upload attempt: admin_id={current_admin.id}, "
        f"file_name={file.filename}, month={salary_month}, year={salary_year}"
    )

    # Validate file extension
    if not file.filename.endswith((".xlsx", ".xls")):
        logger.warning(f"Upload failed: invalid file type file_name={file.filename}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only Excel files are allowed"
        )
    
    try:
        # Read uploaded file as bytes
        file_content = file.file.read()

        # Convert bytes to file-like object for pandas
        excel_file = BytesIO(file_content)

        # Read Excel file from uploaded
        df = pd.read_excel(excel_file)

        # Count total records from Excel
        total_records = int(df["ID Card"].notna().sum())

        logger.info(
            f"Excel file read success: file_name={file.filename}, "
            f"total_records={total_records}"
        )

    except Exception as e:
        logger.error(f"Excel file read failed: cannot read Excel file error={str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot read Excel file"
        )

    # Create upload history record
    upload_history = UploadHistory(
        file_name=file.filename,
        uploaded_by_user_id=current_admin.id,
        salary_month=salary_month,
        salary_year=salary_year,
        total_records=total_records,
        success_records=0,
        failed_records=0,
        status="success",
        error_details=None
    )

    # Save upload history to database
    db.add(upload_history)
    db.commit()
    db.refresh(upload_history)

    logger.info(f"Upload history created: upload_history_id={upload_history.id}")

    success_records = 0
    failed_records = 0

    # Loop through Excel rows
    for index, row in df.iterrows():
        try:
            # Read required data from Excel row
            employee_code = clean_text(row["เลขรหัส / ID"]).strip()
            full_name = clean_text(row["ชื่อ-สกุล / Name"]).strip()
            citizen_id = clean_text(row["ID Card"]).strip()

            # Skip row if citizen_id is missing
            if citizen_id == "":
                logger.info(f"Payslip import skipped: empty citizen_id row={index + 1}")
                continue

            # Find user by citizen_id
            user = db.query(User).filter(User.citizen_id == citizen_id).first()

            # If user does not exist, skip this row
            if user is None:
                failed_records += 1
                logger.warning(f"Payslip import failed: user not found citizen_id={citizen_id}, row={index + 1}")
                continue

            # Check duplicate payslip for this user/month/year
            existing_payslip = db.query(Payslip).filter(
                Payslip.user_id == user.id,
                Payslip.salary_month == salary_month,
                Payslip.salary_year == salary_year
            ).first()

            if existing_payslip:
                failed_records += 1
                logger.warning(
                    f"Payslip import failed: duplicate payslip user_id={user.id}, "
                    f"month={salary_month}, year={salary_year}"
                )
                continue

            # Create payslip record
            payslip = Payslip(
                user_id=user.id,
                upload_history_id=upload_history.id,
                employee_code=employee_code,
                citizen_id=citizen_id,
                department=str(row.get("แผนก / Department", "")).strip(),
                position=str(row.get("ตำแหน่ง / Position", "")).strip(),
                salary_month=salary_month,
                salary_year=salary_year,

                base_salary=to_decimal(row.get("เงินเดือน / Salary")),
                paid_salary=to_decimal(row.get("Paid Salary")),
                allowance=to_decimal(row.get("Allowance")),
                overtime_pay=to_decimal(row.get("จำนวนชั่วโมงทำงานล่วงเวลา / Total Overtime")),
                bonus=Decimal("0"),
                other_income=Decimal("0"),
                adjust_amount=to_decimal(row.get("รายการปรับ / Adjust")),
                special_amount=to_decimal(row.get("Special")),

                expense_deduction=to_decimal(row.get("รายการหัก / Deduct")),
                social_security=Decimal("0"),
                provident_fund=Decimal("0"),
                tax=to_decimal(get_row_value(row, ["TAX", "Tax", "tax"])),
                other_deduction=Decimal("0"),

                total_income=to_decimal(row.get("รายรับทั้งหมด / Total Income")),
                total_deduction=to_decimal(row.get("รวมรายการหัก")),
                net_salary=to_decimal(row.get("รวมทั้งหมด / Total Payment"))
            )

            db.add(payslip)
            success_records += 1

        except Exception as e:
            failed_records += 1
            logger.error(f"Payslip import failed: row={index + 1}, error={str(e)}")

    # Update upload history result
    upload_history.success_records = success_records
    upload_history.failed_records = failed_records

    if failed_records == 0:
        upload_history.status = "success"
    elif success_records > 0:
        upload_history.status = "partial_failed"
    else:
        upload_history.status = "failed"

    db.commit()
    db.refresh(upload_history)

    logger.info(
        f"Payslip upload finished: upload_history_id={upload_history.id}, "
        f"success_records={success_records}, failed_records={failed_records}, "
        f"status={upload_history.status}"
    )

    return {
        "message": "Payslip upload completed",
        "upload_history_id": upload_history.id,
        "file_name": file.filename,
        "salary_month": salary_month,
        "salary_year": salary_year,
        "total_records": int(total_records),
        "success_records": success_records,
        "failed_records": failed_records,
        "status": upload_history.status,
        "uploaded_by": current_admin.id
    }

@router.get("/upload-history", response_model=list[UploadHistoryResponse])
def get_upload_history(
    current_admin: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    # Log admin request for upload history
    logger.info(f"Get upload history: admin_id={current_admin.id}")

    # Query upload histories ordered by latest first
    histories = db.query(UploadHistory).order_by(
        UploadHistory.created_at.desc()
    ).all()

    logger.info(
        f"Get upload history success: admin_id={current_admin.id}, "
        f"total_records={len(histories)}"
    )

    return histories