from app.models import House, VIPStatus
from sqlalchemy.orm import joinedload
from sqlalchemy import desc
from app.database import SessionLocal
from fastapi import HTTPException

def get_featured_houses():
    db = SessionLocal()
    try:
        vip_houses = (
            db.query(House)
            .join(VIPStatus, House.house_id == VIPStatus.house_id)  # Join on the house_id field
            .options(joinedload(House.vip_status))  # Load VIP status data
            .order_by(desc(VIPStatus.created_date))  # Order by newest VIP status
            .limit(5)  # Get only the top 5
            .all()
        )

        if not vip_houses:
            raise HTTPException(status_code=404, detail="No featured houses found.")

        # Serialize the results
        featured_houses = [
            {
                "id": house.house_id,
                "price": house.price,
                "description": house.description,
                "imageUrl": house.image_urls[0] if house.image_urls else None  # Get the first image from the array
            }
            for house in vip_houses
        ]

        return {"featured_houses": featured_houses}

    finally:
        db.close()
