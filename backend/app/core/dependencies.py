from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.logger import logger
from app.core.database import get_db
from app.models.user import User

# Get token from header
security = HTTPBearer()

def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db: Session = Depends(get_db)
):
    # Extract token from request header
    token = credentials.credentials

    # Decode JWT token and get user info
    try:
        # Decode JWT token
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        # Extract user_id from token payload
        user_id = payload.get("user_id")

        if user_id is None:
            logger.warning("Token decode failed: Missing user_id")
            raise HTTPException(status_code=401, detail="Invalid token")

    except JWTError:
        logger.warning("Token decode failed")
        raise HTTPException(status_code=401, detail="Invalid token")

    # Find user from database
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        logger.warning(f"User not found from token user_id={user_id}")
        raise HTTPException(status_code=404, detail="User not found")
    
    logger.info(f"Authenticated user_id={user_id}")

    return user