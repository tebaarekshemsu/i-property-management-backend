from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.database import get_db
from app.models import Admin
from datetime import timedelta
from app.services.admin import get_dashboard_data
from app.schemas.schemas import AdminCreate
from app.auth.auth_handler import get_password_hash
from app.auth.dependencies import get_current_user
from app.database import get_db

router = APIRouter(prefix='/admin', tags=['Admin'])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/signup")
def signup(admin_data: AdminCreate, db: Session = Depends(get_db), current=Depends(get_current_user)):
    if getattr(current, "admin_type", None) != "super-admin":
        raise HTTPException(status_code=403, detail="Only super-admins can create admins")

    existing = db.query(Admin).filter(Admin.phone_no == admin_data.phone_no).first()
    if existing:
        raise HTTPException(status_code=400, detail="Phone already exists")

    hashed_password = get_password_hash(admin_data.password)
    new_admin = Admin(
        name=admin_data.name,
        phone_no=admin_data.phone_no,
        password=hashed_password,
        id_front=admin_data.id_front,
        id_back=admin_data.id_back,
        invitation_code=admin_data.invitation_code,
        admin_type=admin_data.admin_type
    )
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    return {"msg": "Admin created successfully"}

@router.get("/dashboard")
def dashboard(current_admin: Admin = Depends(get_current_user), db: Session = Depends(get_db)):
    return get_dashboard_data(current_admin.admin_id, db)
