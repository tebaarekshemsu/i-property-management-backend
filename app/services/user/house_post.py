from typing import List, Optional
from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session
import os
import json
import shutil
from app.models import House, Area, User

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}


def create_house(
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
    facilities: Optional[str],
    description: str,
    price: float,
    negotiability: str,
    parkingSpace: bool,
    listedBy: str,
    name: str,
    phoneNumber: str,
    videoLink: Optional[str],
    photos: List[UploadFile],
    user_id: int,
    db: Session,
):
    try:
        # Validate inputs
        if not category.strip():
            raise HTTPException(status_code=400, detail={"category": "Category is required."})
        if size <= 0:
            raise HTTPException(status_code=400, detail={"size": "Size must be greater than 0."})
        if bedrooms < 0:
            raise HTTPException(status_code=400, detail={"bedrooms": "Bedrooms cannot be negative."})
        if not description.strip() or len(description) < 20:
            raise HTTPException(status_code=400, detail={"description": "Description must be at least 20 characters long."})
        if price <= 0:
            raise HTTPException(status_code=400, detail={"price": "Price must be greater than 0."})

        # Fetch area_code from Area table using location
        area = db.query(Area).filter(Area.name == location).first()
        if not area:
            raise HTTPException(status_code=400, detail=f"Location '{location}' does not exist in the Area table.")
        area_code = area.code  # Extract the area_code

        # Validate facilities JSON
        try:
            facilities_list = json.loads(facilities) if facilities else []
            if not isinstance(facilities_list, list):
                raise ValueError
        except (json.JSONDecodeError, ValueError):
            raise HTTPException(status_code=400, detail={"facilities": "Facilities must be a valid JSON array."})

        # Validate and save photos
        image_paths = []
        try:
            os.makedirs("media/house_photos", exist_ok=True)
        except OSError as e:
            raise HTTPException(status_code=500, detail=f"Failed to create directory for photos: {str(e)}")

        for photo in photos:
            if not photo.filename.split(".")[-1].lower() in ALLOWED_EXTENSIONS:
                raise HTTPException(status_code=400, detail="Only JPG, JPEG, and PNG files are allowed.")
            filename = f"{name.replace(' ', '_')}_{photo.filename}"
            file_path = os.path.join("media/house_photos", filename)
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(photo.file, buffer)
            image_paths.append(file_path)

        # Save house entry
        house = House(
            category=category,
            area_code=area_code,  # Include the fetched area_code
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
            owner=user_id,
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
    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")