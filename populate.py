from app.database import SessionLocal
from app.models import VIPStatus, Admin
from passlib.context import CryptContext
import random

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def populate_vip_status(db):
    for house_id in range(42, 48):  # House IDs 42 to 47
        vip = VIPStatus(
            house_id=house_id,
            duration=random.randint(15, 30),
            price=round(random.uniform(1000, 5000), 2)
        )
        db.add(vip)
    db.commit()
    print("✅ VIP Status entries inserted for house IDs 42 to 47.")

def populate_admin(db):
            hashed_password = pwd_context.hash("admin123")
            print(hashed_password)
    # existing_admin = db.query(Admin).filter_by(phone_no="0911223344").first()
    # if not existing_admin:
    #     hashed_password = pwd_context.hash("admin123")
    #     admin = Admin(
    #         name="Test Admin",
    #         phone_no="0911223344",
    #         id_front="Adm234",
    #         id_back="Adm234",
    #         admin_type="admin",
    #         password=hashed_password
    #     )
    #     print(hashed_password)
    #     db.add(admin)
    #     db.commit()
    #     print("✅ Test admin created with phone_no: 0911223344 and password: admin123")
    # else:
    #     print("⚠️ Test admin already exists.")

def run():
    db = SessionLocal()
    try:
        # populate_vip_status(db)
        populate_admin(db)
    finally:
        db.close()

if __name__ == "__main__":
    run()
