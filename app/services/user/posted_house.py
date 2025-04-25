from app.models import House
from fastapi import HTTPException
from app.database import SessionLocal


def get_posted_houses(user_id: int):
    db = SessionLocal()
    try:
        print(f"Fetching houses for user_id: {user_id}")  # Debugging
        houses = db.query(House).filter(House.owner == user_id).all()
        print(f"Fetched houses: {houses}") 
        if not houses:
            return []
        return [
            {
               
                "house_id": house.house_id,
                "category": house.category,
                "location": house.location,
                "address": house.address,
                "size": house.size,
                "condition": house.condition,
                "bedroom": house.bedroom,
                "toilets": house.toilets,
                "bathroom": house.bathroom,
                "price": float(house.price),
                "status": house.status,
                "image_urls": house.image_urls,
                "video": house.video,
            }
            for house in houses
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to fetch posted houses")