from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.models import User, Admin
from app.auth.auth_handler import verify_password, create_access_token
from app.database import get_db
from app.schemas.schemas import Token

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # OAuth2PasswordRequestForm only accepts 'username', so treat 'username' as 'phone_no'
    phone_no = form_data.username  # ✅ This is the actual field sent in the form
    password = form_data.password

    user = db.query(User).filter(User.phone_no == phone_no).first()
    role = "user"

    if user:
        user_id = user.user_id
    else:
        user = db.query(Admin).filter(Admin.phone_no == phone_no).first()
        print(user)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        role = user.admin_type
        user_id = user.admin_id

    if not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid password")

    access_token = create_access_token(data={"sub": str(user_id), "role": role})
    return {"access_token": access_token, "token_type": "bearer"}