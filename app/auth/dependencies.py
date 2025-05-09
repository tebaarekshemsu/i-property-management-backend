from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, Admin
from app.auth.auth_handler import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Get the current user from the JWT token.
    """
    payload = decode_token(token)
    user_id = payload.get("sub")
    role = payload.get("role")

    if role == "user":
        user = db.query(User).filter(User.user_id == user_id).first()
    else:
        user = db.query(Admin).filter(Admin.admin_id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
    
