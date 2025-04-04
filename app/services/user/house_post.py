from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.database import SessionLocal
from app.models import House

# Helper function to convert a House object to dictionary
def house_as_dict(house):
    return {
        "house_id": house.house_id,
        "category": house.category,
        "location": house.location,
        "address": house.address,
        "size": house.size,
        "condition": house.condition,
        "bedroom": house.bedroom,
        "toilets": house.toilets,
        "listed_by": house.listed_by,
        "property_type": house.property_type,
        "furnish_status": house.furnish_status,
        "bathroom": house.bathroom,
        "facility": house.facility,
        "description": house.description,
        "price": house.price,
        "negotiability": house.negotiability,
        "parking_space": house.parking_space,
        "assigned_for": house.assigned_for,
        "owner": house.owner,
        "status": house.status,
        "image_urls": house.image_urls,
        "video": house.video,
        "posted_by": house.posted_by
    }

def create_house(house_data: dict):
    print("Saving house data...")  
    with SessionLocal() as db:
        new_house = House(**house_data)
        db.add(new_house)
        db.commit()
        db.refresh(new_house)
    
    return house_as_dict(new_house)
