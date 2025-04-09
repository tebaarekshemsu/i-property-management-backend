from sqlalchemy.orm import Session
from app.models import User, Admin
from app.utils.jwt import create_access_token
from fastapi import HTTPException, status
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def register_user(user_data, db: Session):
    if db.query(User).filter(User.phone_no == user_data.phone_no).first():
        raise HTTPException(status_code=400, detail="Phone number already registered.")
    user = User(
        name=user_data.name,
        phone_no=user_data.phone_no,
        password=hash_password(user_data.password),
        invitation_code=user_data.invitation_code
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def register_admin(admin_data, db: Session, super_admin_id: int):
    super_admin = db.query(Admin).filter_by(admin_id=super_admin_id, admin_type='super-admin').first()
    if not super_admin:
        raise HTTPException(status_code=403, detail="Only super admins can register new admins.")
    if db.query(Admin).filter(Admin.phone_no == admin_data.phone_no).first():
        raise HTTPException(status_code=400, detail="Phone number already registered.")
    admin = Admin(
        name=admin_data.name,
        phone_no=admin_data.phone_no,
        password=hash_password(admin_data.password),
        admin_type='admin',
        id_front=admin_data.id_front,
        id_back=admin_data.id_back,
        invitation_code=admin_data.invitation_code
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return admin
