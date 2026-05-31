from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext

from app.core.logger import logger
from app.core.config import settings

# Password hashing configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT settings Key
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

# Hash password
def hash_password(password: str) -> str:
    logger.info("Hashing Password")
    return pwd_context.hash(password)

# Verify password
def verify_password(plain_password: str, hash_password: str) -> bool:
    # Compare plain password from user with hashed password from database
    result = pwd_context.verify(plain_password, hash_password)

    if result:
        logger.info("Password verification success")
    else:
        logger.warning("Password verification failed")

    return result 

# Create JWT token
def create_access_token(data: dict) -> str:
    # Copy data to avoid modifying the original payload
    to_encode = data.copy()

    # Set token expiration time
    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})

    # Create JWT token
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

    logger.info("Access token created successfully")

    return encoded_jwt