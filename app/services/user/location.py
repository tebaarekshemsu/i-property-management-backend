from app.database import SessionLocal
from app.models import Area  # Import the Area model

def get_all_locations():
    db = SessionLocal()
    try:
        # Query the distinct area_name using SQLAlchemy ORM
        locations = db.query(Area.name).all()  # .all() returns a list of tuples
        # Extract the area_name from the result tuples
        location_list = [location[0] for location in locations]
        return {"locations": location_list}
    finally:
        db.close()
