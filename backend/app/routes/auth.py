from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.security import verify_password, create_access_token, hash_password
from app.core.logger import logger
from app.core.database import get_db
from app.models.user import User

router = APIRouter()

class RegisterRequest(BaseModel):
    username: str
    email: str
    citizen_id: str
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

# Register endpoint
@router.post("/register")
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    logger.info(f"Register attempt: {request.username}")

    # hash password
    hash_pw = hash_password(request.password)

    # Create user
    new_user = User(
        username=request.username,
        email=request.email,
        citizen_id=request.citizen_id,
        hashed_password=hash_pw,
        role="user"
    )

    # Save to database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User registered successfully",
        "user_id": new_user.id
    }

# API
@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    logger.info(f"Login attempt: {request.username}")

    # Get user from database
    user = db.query(User).filter(User.username == request.username).first()

    # No user
    if not user:
        logger.error("User not found")
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # No password
    if not verify_password(request.password, user.hashed_password):
        logger.warning("Login failed:Wrong password")
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Create token
    token = create_access_token({
        "user_id": user.id,
        "username": user.username,
        "role": user.role
    })

    logger.info("Login success")

    return {
        "access_token": token,
        "token_type": "bearer"
    }