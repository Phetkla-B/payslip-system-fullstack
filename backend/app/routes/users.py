from fastapi import APIRouter, Depends

from app.core.dependencies import get_current_user

router = APIRouter()

@router.get("/me")
# Get current user info
def get_me(current_user: dict = Depends(get_current_user)):
    return {
        "message": "You are authenticated",
        "user_id": current_user
    }