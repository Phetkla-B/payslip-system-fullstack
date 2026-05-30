from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.logger import logger
from app.core.config import settings
from app.core.database import SessionLocal, get_db
from app.models.user import User

# hash password
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
    result = pwd_context.verify(plain_password, hash_password)

    if result:
        logger.info("Password verification success")
    else:
        logger.warning("Password verification failed")

    return result 

# Create JWT token
def create_access_token(data: dict):
    logger.info(f"Creating access token for data : {data}")

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    logger.info("Access token created successfully")

    return encoded_jwt