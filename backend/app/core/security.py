from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.logger import logger

# hash password
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# key for sign token
SECRET_KEY = "you-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def hash_password(password: str) -> str:
    logger.info("Hashing Password")
    return pwd_context.hash(password)

def verify_password(plain_password: str, hash_password: str) -> bool:
    result = pwd_context.verify(plain_password, hash_password)

    if result:
        logger.info("Password verification success")
    else:
        logger.warning("Password verification failed")

    return result 

def create_access_token(data: dict):
    logger.info(f"Creating access token for data : {data}")

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    logger.info("Access token created successfully")

    return encoded_jwt