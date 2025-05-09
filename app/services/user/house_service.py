from sqlalchemy.orm import Session
from app.database import SessionLocal
from sqlalchemy import or_, and_
from app.models import House
from fastapi import HTTPException
from typing import Optional

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

def get_house_list(
    page: int = 1,
    page_size: int = 10,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    house_type: Optional[str] = None,
    furnishing_status: Optional[str] = None,
    bedrooms: Optional[int] = None,
    bathrooms: Optional[int] = None,
    location: Optional[str] = None,
    category: str = "",
):
    """
    Get a list of houses with optional filtering.
    """
    db = SessionLocal()
    try:
        query = db.query(House)

        if min_price is not None:
            query = query.filter(House.price >= min_price)
        if max_price is not None:
            query = query.filter(House.price <= max_price)
        if house_type:
            query = query.filter(House.property_type == house_type)
        if furnishing_status:
            query = query.filter(House.furnish_status == furnishing_status)
        if bedrooms is not None:
            query = query.filter(House.bedroom == bedrooms)
        if bathrooms is not None:
            query = query.filter(House.bathroom == bathrooms)
        if location:
            query = query.filter(House.location == location)
        if category:
            query = query.filter(House.category == category)

        houses = query.offset((page - 1) * page_size).limit(page_size).all()
        return [house_as_dict(house) for house in houses]
    finally:
        db.close()

def get_house_detail(db: Session, house_id: int):
    house = db.query(House).filter(House.house_id == house_id).first()
    if not house:
        return {"message": "House not found"}
    return house_as_dict(house)