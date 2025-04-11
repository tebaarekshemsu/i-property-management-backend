from typing import List, Optional
from fastapi import UploadFile, Form
from sqlalchemy.orm import Session
import os, json, shutil
from app.models import House, User

async def create_house_posting(
    category: str,
    location: str,
    address: str,
    size: float,
    condition: str,
    bedrooms: int,
    toilets: int,
    bathrooms: int,
    propertyType: str,
    furnishStatus: str,
    facilities: str,  # JSON string
    description: str,
    price: float,
    negotiability: str,
    parkingSpace: bool,
    listedBy: str,
    name: str,
    phoneNumber: str,
    photos: List[UploadFile],
    admin_id: int,
    db: Session,
    videoLink: Optional[str] = None,
):
    errors = {}
    if not category.strip():
        errors["category"] = "Required"
    if not location.strip():
        errors["location"] = "Required"
    if not address.strip():
        errors["address"] = "Required"
    if size <= 0:
        errors["size"] = "Must be > 0"
    if bedrooms < 0:
        errors["bedrooms"] = "Cannot be negative"
    if toilets < 0:
        errors["toilets"] = "Cannot be negative"
    if bathrooms < 0:
        errors["bathrooms"] = "Cannot be negative"
    if not propertyType.strip():
        errors["propertyType"] = "Required"
    if not furnishStatus.strip():
        errors["furnishStatus"] = "Required"
    if not description.strip() or len(description) < 20:
        errors["description"] = "Must be at least 20 characters"
    if price <= 0:
        errors["price"] = "Must be > 0"
    if negotiability not in ["open to negotiation", "not negotiable"]:
        errors["negotiability"] = "Invalid value"
    if not listedBy.strip():
        errors["listedBy"] = "Required"
    if not name.strip():
        errors["name"] = "Required"
    if not phoneNumber.strip():
        errors["phoneNumber"] = "Required"
    if not photos:
        errors["photos"] = "At least one photo required"

    try:
        facilities_list = json.loads(facilities)
        if not isinstance(facilities_list, list):
            errors["facilities"] = "Must be a JSON list"
    except:
        errors["facilities"] = "Invalid JSON"

    if errors:
        return {"success": False, "errors": errors}

    os.makedirs("media/house_photos", exist_ok=True)
    image_paths = []
    for photo in photos:
        filename = f"{name.replace(' ', '_')}_{photo.filename}"
        path = os.path.join("media/house_photos", filename)
        with open(path, "wb") as f:
            shutil.copyfileobj(photo.file, f)
        image_paths.append(path)

    owner = db.query(User).filter(User.phone_no == phoneNumber).first()
    if not owner:
        return {"success": False, "message": "User not found"}

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
        owner=owner.user_id,
        assigned_for=admin_id,
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