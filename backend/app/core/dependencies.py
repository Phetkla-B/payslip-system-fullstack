from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.logger import logger
from app.core.database import get_db
from app.models.user import User

# Read token from request header
# Authorization : Bearer <token>
security = HTTPBearer()

# Get current user from token
def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db: Session = Depends(get_db)
) -> User:
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

        # If token does not contain user_id token is not valid
        if user_id is None:
            logger.warning("Token decode failed: Missing user_id")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Invalid token"
            )

    except JWTError:
        # This includes invalid token, expired token, etc.
        logger.warning("Token decode failed: Cannot decode token")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    # Query user from database by user_id from token
    user = db.query(User).filter(User.id == user_id).first()

    # Token is valid, but user no longer exists in database
    if user is None:
        logger.warning(f"Authenticated user not found: user_id={user_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    logger.info(f"Authenticated user success: user_id={user.id}")

    return user