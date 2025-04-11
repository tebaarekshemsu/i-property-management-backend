from fastapi import Depends, HTTPException
from app.models import User
from app.database import SessionLocal
from app.auth.dependencies import get_current_user as auth_get_current_user  # Import from auth/dependencies.py

def get_user_service(user_id: int):
    db = SessionLocal()
    user = db.query(User).filter(User.user_id == user_id).first()
    print("herrrrrrrrr")
    print(user.phone_no)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def update_user_service(user_id: int, user_data: dict):
    print('youuuuuuuuu')
    db = SessionLocal()
    
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    for key, value in user_data.items():
        if hasattr(user, key):
            setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user

# Use the centralized token extraction logic from auth/dependencies.py
def get_current_user(user: User = Depends(auth_get_current_user)):
    return user