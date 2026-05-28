from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.core.security import verify_password, create_access_token
from app.core.logger import logger

router = APIRouter()

# Mick User for test
fake_user_db = {
    "1234567890123": {
        "user_id": 1,
        "citizen_id": "1234567890123",
        "hashed_password": "$2b$12$ACINKqlXS.EwmCWn8VFZd.ylr7DheH8lBIfCRd7UPQGk9PuCYzMzO",
        "role": "user"
    }
}

# Request Schema
class LoginRequest(BaseModel):
    citizen_id: str
    password: str

# API
@router.post("/login")
def login(request: LoginRequest):
    logger.info(f"Login attempt: {request.citizen_id}")

    user = fake_user_db.get(request.citizen_id)

    # No user
    if not user:
        logger.error("User not found")
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # No password
    if not verify_password(request.password, user["hashed_password"]):
        logger.warning("Wrong password")
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Create token
    token = create_access_token({
        "user_id": user["user_id"],
        "role": user["role"]
    })

    logger.info("Login success")

    return {
        "access_token": token,
        "token_type": "bearer"
    }