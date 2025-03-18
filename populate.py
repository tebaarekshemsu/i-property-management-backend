from app.database import SessionLocal
from app.models import VIPStatus
import random
def populate_vip_status():
    db = SessionLocal()

    # Step 1: Insert 5 VIP Status entries for house IDs 42 to 47
    for house_id in range(42, 48):  # This will create house IDs 42, 43, 44, 45, 46, 47
        db.add(VIPStatus(
            house_id=house_id,
            duration=random.randint(15, 30),  # Random duration between 15 and 30 days
            price=round(random.uniform(1000, 5000), 2)  # Random price between 1000 and 5000
        ))

    db.commit()
    print("5 VIP Status entries inserted successfully for house IDs 42 to 47.")

if __name__ == "__main__":
    populate_vip_status()