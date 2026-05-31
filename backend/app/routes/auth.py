from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.core.security import verify_password, create_access_token, hash_password
from app.core.logger import logger
from app.core.database import get_db
from app.models.user import User
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse

router = APIRouter()

# Register endpoint
@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    logger.info(f"Register attempt: username={request.username}")

    # Check duplicate username
    existing_username = db.query(User).filter(User.username == request.username).first()
    if existing_username:
        logger.warning(f"Register failed: username already exists username={request.username}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )
    
    # Check duplicate email
    existing_email = db.query(User).filter(User.email == request.email).first()
    if existing_email:
        logger.warning(f"Register failed: email already exists email={request.email}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )
    
    # Check duplicate citizen_id
    existing_citizen_id = db.query(User).filter(User.citizen_id == request.citizen_id).first()
    if existing_citizen_id:
        logger.warning(f"Register failed: citizen_id already exists")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Citizen ID already exists"
        )

    # hash password before saving to database
    hash_pw = hash_password(request.password)

    # Create user
    new_user = User(
        username=request.username,
        email=request.email,
        citizen_id=request.citizen_id,
        hashed_password=hash_pw,
        role="user"
    )

    try:
        # Save to database
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        logger.info(f"Register success: user_id={new_user.id}")

    except IntegrityError:
        # Rollback transaction if database insert failed
        db.rollback()
        logger.error("Register failed: database integrity error")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User data already exists"
        )

    return {
        "message": "User registered successfully",
        "user_id": new_user.id
    }

# Login endpoint
@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    logger.info(f"Login attempt by citizen_id")

    # Find user by citizen_id
    user = db.query(User).filter(User.citizen_id == request.citizen_id).first()

    # Do not reveal whether citizen_id or password is wrong
    if not user:
        logger.warning(f"Login failed: citizen_id not found")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    # Verify password from request against hashed password in database
    if not verify_password(request.password, user.hashed_password):
        logger.warning(f"Login failed: wrong password username={request.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    # Create JWT token payload
    token = create_access_token({
        "user_id": user.id,
        "citizen_id": user.citizen_id,
        "role": user.role
    })

    logger.info(f"Login success: user_id={user.id}")

    return {
        "access_token": token,
        "token_type": "bearer"
    }