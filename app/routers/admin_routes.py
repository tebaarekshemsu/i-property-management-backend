from fastapi import APIRouter, Depends, HTTPException, status, Form, File, UploadFile, Query # type: ignore
from fastapi.security import OAuth2PasswordRequestForm # type: ignore
from sqlalchemy.orm import Session # type: ignore
from passlib.context import CryptContext # type: ignore
from app.database import get_db
from app.models import Admin, House, User, Invitation, FailureReport, SuccessReport, Area
from datetime import timedelta
from app.services.admin import get_dashboard_data
from app.schemas.schemas import AdminCreate, HouseUpdate, AreaCreate
from app.auth.auth_handler import get_password_hash
from app.auth.dependencies import get_current_user
from typing import List, Optional
import os
import shutil
import json

router = APIRouter(prefix='/admin', tags=['Admin'])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.get("/dashboard")
def dashboard(current_admin: Admin = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Get dashboard data for the current admin.
    """
    return get_dashboard_data(current_admin.admin_id, db)

@router.get("/houselist")
def get_admin_houses(
    page: int = Query(1, ge=1, description="Page number"),
    db: Session = Depends(get_db), 
    current_admin: Admin = Depends(get_current_user)
):
    """
    Get houses assigned to the current admin with pagination (10 houses per page).
    """
    if not hasattr(current_admin, "admin_id"):
        raise HTTPException(status_code=403, detail="Not authorized as admin")
    
    # Calculate offset
    per_page = 10
    offset = (page - 1) * per_page
    
    # Get total count
    total_houses = db.query(House).filter(House.assigned_for == current_admin.admin_id).count()
    
    # Get paginated houses
    houses = db.query(House).filter(
        House.assigned_for == current_admin.admin_id
    ).offset(offset).limit(per_page).all()
    
    # Calculate total pages
    total_pages = (total_houses + per_page - 1) // per_page
    
    return {
        "houses": houses,
        "pagination": {
            "current_page": page,
            "total_pages": total_pages,
            "total_houses": total_houses,
            "houses_per_page": per_page
        }
    }

@router.delete("/delete/{house_id}")
def delete_house(house_id: int, db: Session = Depends(get_db), current_admin: Admin = Depends(get_current_user)):
    """
    Delete a house by ID. Only the assigned admin can delete it.
    """
    house = db.query(House).filter(House.house_id == house_id).first()
    if not house:
        raise HTTPException(status_code=404, detail="House not found")
    if house.assigned_for != current_admin.admin_id:
        raise HTTPException(status_code=403, detail="You do not have permission to delete this house")

    db.delete(house)
    db.commit()
    return {"detail": "House deleted successfully"}

@router.put("/edit/{house_id}")
def update_house(house_id: int, updated_data: HouseUpdate, db: Session = Depends(get_db), current_admin: Admin = Depends(get_current_user)):
    """
    Update a house by ID. Only the assigned admin can update it.
    """
    house = db.query(House).filter(House.house_id == house_id).first()
    if not house:
        raise HTTPException(status_code=404, detail="House not found")
    if house.assigned_for != current_admin.admin_id:
        raise HTTPException(status_code=403, detail="You do not have permission to update this house")

    for field, value in updated_data.dict(exclude_unset=True).items():
        setattr(house, field, value)

    db.commit()
    db.refresh(house)
    return house

@router.post("/house-post")
async def admin_post_house(
    area: str = Form(...),
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
    db: Session = Depends(get_db),
    current_user: Admin = Depends(get_current_user)
):
    """
    Post a new house. Validates input and saves images.
    """
    if not hasattr(current_user, "admin_id"):
        raise HTTPException(status_code=403, detail="Not authorized as admin")

    errors = {}
    if not area.strip():
        errors["area"] = "Area is required."
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
    if not description.strip() or len(description) < 20:
        errors["description"] = "Description must be at least 20 characters."
    if price <= 0:
        errors["price"] = "Price must be greater than 0."
    if negotiability not in ["open to negotiation", "not"]:
        errors["negotiability"] = "Invalid negotiability value."
    if not listedBy.strip():
        errors["listedBy"] = "Listed by is required."
    elif listedBy not in ["agent", "owner"]:
        errors["listedBy"] = "Listed by must be either 'agent' or 'owner'."
    if not name.strip():
        errors["name"] = "Name is required."
    if not phoneNumber.strip():
        errors["phoneNumber"] = "Phone number is required."
    if not photos:
        errors["photos"] = "At least one photo is required."

    try:
        facilities_list = []
        if facilities.strip().startswith("["):
            facilities_list = json.loads(facilities)
        else:
            facilities_list = [item.strip() for item in facilities.split(",") if item.strip()]

        if not isinstance(facilities_list, list):
            errors["facilities"] = "Facilities must be a list."
    except Exception:
        errors["facilities"] = "Invalid facilities format."

    if errors:
        raise HTTPException(status_code=400, detail=errors)

    # Fetch area_code from Area table using area name
    area_obj = db.query(Area).filter(Area.name == area.strip()).first()
    if not area_obj:
        raise HTTPException(status_code=400, detail=f"Area '{area}' does not exist in the Area table.")

    image_paths = []
    os.makedirs("media/house_photos", exist_ok=True)
    for photo in photos:
        filename = f"{name.replace(' ', '_')}_{photo.filename}"
        file_path = os.path.join("media/house_photos", filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(photo.file, buffer)
        image_paths.append(file_path)

    owner_user = db.query(User).filter(User.phone_no == phoneNumber).first()
    if not owner_user:
        # Create new user with default password
        hashed_password = get_password_hash("00000000")
        new_user = User(
            name=name,
            phone_no=phoneNumber,
            password=hashed_password
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        owner_user = new_user

    house = House(
        category=category,
        area_code=area_obj.code,  # Use the fetched area code
        location=location.strip(),  # Keep location as a separate field
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
        assigned_for=current_user.admin_id,
        owner=owner_user.user_id,
        image_urls=image_paths,
        video=videoLink
    )
    db.add(house)
    db.commit()
    db.refresh(house)
    return {"success": True, "message": "House posted successfully", "house": house}

@router.get("/visit-request")
def get_visit_requests_for_admin(
    db: Session = Depends(get_db), current_admin: Admin = Depends(get_current_user)
):
    """
    Get all visit requests for the current admin.
    """
    if not hasattr(current_admin, "admin_id"):
        raise HTTPException(status_code=403, detail="Not authorized as admin")
    requests = db.query(Invitation).filter(Invitation.house_id.in_(
        db.query(House.house_id).filter(House.assigned_for == current_admin.admin_id)
    )).all()
    return requests

@router.put("/{request_id}/mark-seen")
def mark_visit_request_as_seen(
    request_id: int, db: Session = Depends(get_db), current_admin: Admin = Depends(get_current_user)
):
    """
    Mark a visit request as seen.
    """
    if not hasattr(current_admin, "admin_id"):
        raise HTTPException(status_code=403, detail="Not authorized as admin")
    request = db.query(Invitation).filter(Invitation.id == request_id).first()
    if not request:
        raise HTTPException(status_code=404, detail="Visit request not found")
    request.status = "seen"
    db.commit()
    return {"detail": "Visit request marked as seen"}

@router.post("/success-report/{request_id}")
def create_success_report(
    request_id: int,
    price: float = Form(...),
    type: str = Form(...),
    commission: float = Form(...),
    transaction_photo: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_user)
):
    """
    Create a success report for a visit request.
    """
    if not hasattr(current_admin, "admin_id"):
        raise HTTPException(status_code=403, detail="Not authorized as admin")
    request = db.query(Invitation).filter(Invitation.id == request_id).first()
    if not request:
        raise HTTPException(status_code=404, detail="Visit request not found")

    filename = f"success_report_{request_id}_{transaction_photo.filename}"
    file_path = os.path.join("media/transaction_photos", filename)
    os.makedirs("media/transaction_photos", exist_ok=True)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(transaction_photo.file, buffer)

    report = SuccessReport(
        admin_id=current_admin.admin_id,
        invitation_id=request_id,
        price=price,
        type=type,
        commission=commission,
        transaction_photo=file_path
    )
    db.add(report)
    db.commit()
    return {"detail": "Success report created"}

@router.post("/failure-report/{request_id}")
def create_failure_report(
    request_id: int,
    reason: str = Form(...),
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_user)
):
    """
    Create a failure report for a visit request.
    """
    if not hasattr(current_admin, "admin_id"):
        raise HTTPException(status_code=403, detail="Not authorized as admin")
    request = db.query(Invitation).filter(Invitation.id == request_id).first()
    if not request:
        raise HTTPException(status_code=404, detail="Visit request not found")

    report = FailureReport(
        admin_id=current_admin.admin_id,
        invitation_id=request_id,
        reason=reason
    )
    db.add(report)
    db.commit()
    return {"detail": "Failure report created"}

@router.get("/area")
def getarea(db: Session = Depends(get_db)):
    """
    Get all areas from the database.
    """
    areas = db.query(Area).all()
    return areas

@router.post("/area")
def create_area(area: AreaCreate, db: Session = Depends(get_db)):
    """
    Create a new area.
    """
    try:
        # Validate area name
        if not area.name or not area.name.strip():
            raise HTTPException(status_code=400, detail="Area name cannot be empty")
        
        # Check if area name already exists
        existing_area = db.query(Area).filter(Area.name == area.name.strip()).first()
        if existing_area:
            raise HTTPException(status_code=400, detail="Area with this name already exists")
        
        # Get the highest code and increment by 1
        highest_code = db.query(Area.code).order_by(Area.code.desc()).first()
        next_code = 1 if highest_code is None else highest_code[0] + 1
        
        new_area = Area(
            code=next_code,
            name=area.name.strip()
        )
        db.add(new_area)
        db.commit()
        db.refresh(new_area)
        return {"detail": "Area created successfully", "area": new_area}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
