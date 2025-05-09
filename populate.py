from app.database import SessionLocal
from app.models import VIPStatus, Admin, House, Area
from passlib.context import CryptContext
import random

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def populate_area(db):
    """Create a sample area if it doesn't exist"""
    area = db.query(Area).filter(Area.code == 1).first()
    if not area:
        area = Area(
            code=1,
            name="Sample Location"
        )
        db.add(area)
        db.commit()
        print("✅ Sample area created with code 1.")
    else:
        print("✅ Sample area already exists.")

def populate_houses(db):
    """Create sample houses"""
    for i in range(42, 48):
        house = House(
            house_id=i,
            category='sell',  # Using valid enum value: 'sell' or 'rent'
            location="Sample Location",
            address=f"Address {i}",
            size=random.randint(80, 200),
            condition='newly built',  # Using valid enum value
            bedroom=random.randint(2, 4),
            toilets=random.randint(1, 3),
            bathroom=random.randint(1, 3),
            property_type='apartment',  # Using valid enum value
            furnish_status='furnished',  # Using valid enum value
            facility="[]",
            description=f"Sample house description {i}",
            price=random.uniform(100000, 500000),
            negotiability='open to negotiation',  # Using valid enum value
            parking_space=True,
            listed_by='owner',  # Using valid enum value
            status='available',  # Using valid enum value
            image_urls=[],
            video=None,
            area_code=1,  # Adding required area_code
            owner=1  # Assuming there's at least one user with ID 1
        )
        db.add(house)
    db.commit()
    print("✅ Sample houses created with IDs 42 to 47.")

def populate_vip_status(db):
    """Create VIP status entries for houses"""
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
        populate_area(db)  # Create area first
        populate_houses(db)  # Create houses next
        populate_vip_status(db)  # Then create VIP status entries
        populate_admin(db)
    finally:
        db.close()

if __name__ == "__main__":
    run()
