from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.auth.auth_handler import SECRET_KEY, ALGORITHM
from app.database import get_db
from app.models import User, Admin

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_type = payload.get("role")
        user_id = int(payload.get("sub"))

        if user_type == "user":
            user = db.query(User).filter(User.id == user_id).first()
        elif user_type in ("admin", "super-admin"):
            user = db.query(Admin).filter(Admin.admin_id == user_id).first()
        else:
            raise credentials_exception

        if user is None:
            raise credentials_exception
        return user

    except JWTError:
        raise credentials_exception
    
