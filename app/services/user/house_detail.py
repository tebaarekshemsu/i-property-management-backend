from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.database import SessionLocal
from app.models import House
from fastapi import HTTPException

def get_house_detail(house_id: int):
    """
    Get detailed information about a specific house.
    """
    print("get touch")
    print(house_id)
    db: Session = SessionLocal()
    try:
        print(f"Fetching house detail for ID: {house_id}")  # Debugging info
        house = db.query(House).filter(House.house_id == house_id).first()
        
        if house:
            print(f"House found: {house}")  # Debugging info
            response = {
                "house_id": house.house_id,
                "category": house.category,
                "location": house.location,
                "address": house.address,
                "size": house.size,
                "toilets": house.toilets,
                "condition": house.condition,
                "bedroom": house.bedroom,
                "facility": house.facility,
                "property_type": house.property_type,
                "furnish_status": house.furnish_status,
                "negotiability": house.negotiability,
                "bathroom": house.bathroom,
                "price": float(house.price),
                "status": house.status,
                "image_urls": house.image_urls,
                "description": house.description,
                "parking_space": house.parking_space,
                "listed_by": house.listed_by,
                "video": house.video
            }
            return (response), 200

        print("House not found")  # Debugging info
        raise HTTPException(status_code=404, detail="House not found")

    except SQLAlchemyError as e:
        db.rollback()
        print(f"Database error: {str(e)}")  # Debugging info
        return ({"error": "Database error"}), 500

    except Exception as e:
        print(f"Unexpected error: {str(e)}")  # Debugging info
        return ({"error": "Unexpected error"}), 500

    finally:
        db.close()
        print("Database session closed")  # Debugging info
