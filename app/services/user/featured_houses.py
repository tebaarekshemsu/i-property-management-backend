from sqlalchemy.orm import Session
from app.models import House, VIPStatus
from fastapi import HTTPException
from app.database import SessionLocal
from sqlalchemy.exc import SQLAlchemyError

def get_featured_houses():
    """
    Get a list of VIP houses.
    """
    db = SessionLocal()
    try:
        # Query houses that have VIP status
        houses = db.query(House).join(VIPStatus).all()
        
        if not houses:
            return []  # Return empty list if no VIP houses found
            
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
                "price": float(house.price),  # Convert Decimal to float
                "negotiability": house.negotiability,
                "parking_space": house.parking_space,
                "listed_by": house.listed_by,
                "status": house.status,
                "image_urls": house.image_urls,
                "video": house.video,
                "vip_status": {
                    "duration": house.vip_status.duration,
                    "price": float(house.vip_status.price)  # Convert Decimal to float
                }
            }
            for house in houses
        ]
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Database error occurred while fetching featured houses: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred while fetching featured houses: {str(e)}"
        )
    finally:
        db.close()
