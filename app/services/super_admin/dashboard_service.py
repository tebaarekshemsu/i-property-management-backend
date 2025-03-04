from app.models import Area
from app.database import SessionLocal


def get_dashboard_data():
    return {"message": "Super Admin Dashboard"}


def get_all_location():
    db = SessionLocal()
    try:
        return db.query(Area).all()
    finally:
        db.close()
