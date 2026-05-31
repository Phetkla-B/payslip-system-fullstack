from fastapi import APIRouter, Depends

from app.core.dependencies import get_current_user
from app.core.logger import logger
from app.models.user import User
from app.schemas.user import UserResponse

router = APIRouter()

@router.get("/me", response_model=UserResponse)
# Get current user info
def get_me(current_user: User = Depends(get_current_user)):
    # Log successful profile request
    logger.info(f"Get current user profile: user_id={current_user.id}")

    return {
        "id": current_user.id,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
        "email": current_user.email,
        "citizen_id": current_user.citizen_id,
        "role": current_user.role
    }