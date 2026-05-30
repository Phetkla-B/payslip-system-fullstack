from fastapi import APIRouter, Depends

from app.core.dependencies import get_current_user
from app.core.logger import logger
from app.models.user import User

router = APIRouter()

@router.get("/me")
# Get current user info
def get_me(current_user: User = Depends(get_current_user)):
    # Log successful profile request
    logger.info(f"Get current user profile: user_id={current_user.id}")

    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "citizen_id": current_user.citizen_id,
        "role": current_user.role
    }