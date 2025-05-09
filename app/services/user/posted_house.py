from sqlalchemy.orm import Session
from app.models import House, User
from fastapi import HTTPException

def fetch_posted_houses(current_user: User):
    """
    Get all houses posted by the current user.
    """
    houses = current_user.houses
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
            "property_type": house.property_type,
            "furnish_status": house.furnish_status,
            "facility": house.facility,
            "description": house.description,
            "price": house.price,
            "negotiability": house.negotiability,
            "parking_space": house.parking_space,
            "listed_by": house.listed_by,
            "status": house.status,
            "image_urls": house.image_urls,
            "video": house.video
        }
        for house in houses
    ]