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

from typing import List, Optional
from fastapi import Depends, File, Form, UploadFile
from sqlalchemy.orm import Session
import os, json, shutil
from app.database import SessionLocal
from app.models import House, User

def create_house_posting(
    category: str = Form(...),
    location: str = Form(...),
    address: str = Form(...),
    size: float = Form(...),
    
    condition: str = Form(...),
    bedrooms: int = Form(...),
    toilets: int = Form(...),
    bathrooms: int = Form(...),
    propertyType: str = Form(...),
    furnishStatus: str = Form(...),
    
    facilities: str = Form(...),  # JSON string
    description: str = Form(...),
    price: float = Form(...),
    negotiability: str = Form(...),
    parkingSpace: bool = Form(...),
    
    listedBy: str = Form(...),
    name: str = Form(...),
    phoneNumber: str = Form(...),
    videoLink: Optional[str] = Form(None),
    
    photos: List[UploadFile] = File(...),
    db: Session = SessionLocal()
):
    # Custom validation for user inputs
    errors = {}

    if not category.strip():
        errors["category"] = "Category is required."
    if not location.strip():
        errors["location"] = "Location is required."
    if not address.strip():
        errors["address"] = "Address is required."
    if size <= 0:
        errors["size"] = "Size must be greater than 0."
    if bedrooms < 0:
        errors["bedrooms"] = "Bedrooms cannot be negative."
    if toilets < 0:
        errors["toilets"] = "Toilets cannot be negative."
    if bathrooms < 0:
        errors["bathrooms"] = "Bathrooms cannot be negative."
    if not propertyType.strip():
        errors["propertyType"] = "Property type is required."
    if not furnishStatus.strip():
        errors["furnishStatus"] = "Furnish status is required."
    if not description.strip():
        errors["description"] = "Description is required."
    elif len(description) < 20:
        errors["description"] = "Description must be at least 20 characters long."
    if price <= 0:
        errors["price"] = "Price must be greater than 0."
    if negotiability not in ["open to negotiation", "not negotiable"]:
        errors["negotiability"] = "Negotiability must be 'open to negotiation' or 'not negotiable'."
    if not listedBy.strip():
        errors["listedBy"] = "Listed by is required."
    if not name.strip():
        errors["name"] = "Name is required."
    if not phoneNumber.strip():
        errors["phoneNumber"] = "Phone number is required."
    if not photos:
        errors["photos"] = "At least one photo is required."

    # Validate facilities JSON
    try:
        facilities_list = json.loads(facilities)
        if not isinstance(facilities_list, list):
            errors["facilities"] = "Facilities must be a JSON array."
    except json.JSONDecodeError:
        errors["facilities"] = "Invalid facilities JSON."

    # If there are errors, return them
    if errors:
        return {"success": False, "errors": errors}

    # 1. Save uploaded photos and collect file paths
    image_paths = []
    for photo in photos:
        filename = f"{name.replace(' ', '_')}_{photo.filename}"
        file_path = os.path.join("media/house_photos", filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(photo.file, buffer)
        image_paths.append(file_path)

    # 2. Get owner and assigned admin (this should come from session or external logic)
    owner_user = db.query(User).filter(User.phone_no == phoneNumber).first()

    if not owner_user:
        return {"success": False, "message": "User not found."}

    # TODO: Update this when you have logic to assign admin
    assigned_admin_id = 1

    # 3. Save the house entry
    house = House(
        category=category,
        location=location,
        address=address,
        size=size,
        condition=condition,
        bedroom=bedrooms,
        toilets=toilets,
        bathroom=bathrooms,
        property_type=propertyType,
        furnish_status=furnishStatus,
        facility=json.dumps(facilities_list),
        description=description,
        price=price,
        negotiability=negotiability,
        parking_space=parkingSpace,
        listed_by=listedBy,
        video=videoLink,
        image_urls=image_paths,
        owner=owner_user.user_id,
        assigned_for=assigned_admin_id,  # Placeholder
        status="pending",
    )

    db.add(house)
    db.commit()
    db.refresh(house)

    return {
        "success": True,
        "message": "House posted successfully.",
        "house_id": house.house_id,
     }