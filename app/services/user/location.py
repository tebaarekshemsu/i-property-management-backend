from sqlalchemy.orm import Session
from app.models import Area
from fastapi import HTTPException
from app.database import SessionLocal
from sqlalchemy.exc import SQLAlchemyError

def get_all_locations():
    """
    Get all available locations.
    """
    db = SessionLocal()
    try:
        areas = db.query(Area).all()
        return [{"code": area.code, "name": area.name} for area in areas]
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Database error occurred while fetching locations: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred while fetching locations: {str(e)}"
        )
    finally:
        db.close()
