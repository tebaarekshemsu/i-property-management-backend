from sqlalchemy.orm import Session
from app.database import SessionLocal
from sqlalchemy import or_, and_
from app.models import House

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

def get_house_list(page: int, page_size: int, min_price: float = None, max_price: float = None, house_type: str = None, furnishing_status: str = None, bedrooms: int = None, bathrooms: int = None, location: str = None, category: str = None):
    print('Fetching house list...')
    with SessionLocal() as db:
        query = db.query(House)

        if category:
            query = query.filter(House.category == category)
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
            query = query.filter(House.location.ilike(f"%{location}%"))

        total_count = query.count()
        houses = query.offset((page - 1) * page_size).limit(page_size).all()

    return {
        "total_count": total_count,
        "page": page,
        "page_size": page_size,
        "houses": [house_as_dict(house) for house in houses]
    }

def get_house_detail(db: Session, house_id: int):
    house = db.query(House).filter(House.house_id == house_id).first()
    if not house:
        return {"message": "House not found"}
    print(house)
    return house_as_dict(house)