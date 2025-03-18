from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.database import SessionLocal
from app.models import House

def get_house_detail(house_id):
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
                "condition": house.condition,
                "bedroom": house.bedroom,
                "bathroom": house.bathroom,
                "price": float(house.price),
                "status": house.status,
                "image_urls": house.image_urls,
                "description": house.description
            }
            return (response), 200

        print("House not found")  # Debugging info
        return ({"message": "House not found"}), 404

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
