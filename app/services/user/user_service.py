from sqlalchemy.orm import Session
from app.models import User
from app.auth.dependencies import get_current_user
from fastapi import HTTPException

def get_user_profile(current_user: User):
    """
    Get the current user's profile.
    """
    return {
        "user_id": current_user.user_id,
        "name": current_user.name,
        "phone_no": current_user.phone_no,
        "invitation_code": current_user.invitation_code,
        "invited_by": current_user.invited_by
    }

def update_user_profile(user_data: dict, current_user: User):
    """
    Update the current user's profile.
    """
    for key, value in user_data.items():
        if hasattr(current_user, key):
            setattr(current_user, key, value)
    return get_user_profile(current_user)