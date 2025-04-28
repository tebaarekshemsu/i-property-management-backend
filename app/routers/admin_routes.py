from fastapi import APIRouter, Depends, HTTPException, status, Form, File, UploadFile # type: ignore
from fastapi.security import OAuth2PasswordRequestForm # type: ignore
from sqlalchemy.orm import Session # type: ignore
from passlib.context import CryptContext # type: ignore
from app.database import get_db
from app.models import Admin, House, User, Invitation, FailureReport, SuccessReport
from datetime import timedelta
from app.services.admin import get_dashboard_data
from app.schemas.schemas import AdminCreate, HouseUpdate
from app.auth.auth_handler import get_password_hash
from app.auth.dependencies import get_current_user
from typing import List, Optional
import os
import shutil
import json

router = APIRouter(prefix='/admin', tags=['Admin'])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/signup")
def signup(admin_data: AdminCreate, db: Session = Depends(get_db), current=Depends(get_current_user)):
    if getattr(current, "admin_type", None) != "super-admin":
        raise HTTPException(status_code=403, detail="Only super-admins can create admins")

    existing = db.query(Admin).filter(Admin.phone_no == admin_data.phone_no).first()
    if existing:
        raise HTTPException(status_code=400, detail="Phone already exists")

    hashed_password = get_password_hash(admin_data.password)
    new_admin = Admin(
        name=admin_data.name,
        phone_no=admin_data.phone_no,
        password=hashed_password,
        id_front=admin_data.id_front,
        id_back=admin_data.id_back,
        invitation_code=admin_data.invitation_code,
        admin_type=admin_data.admin_type
    )
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    return {"msg": "Admin created successfully"}

@router.get("/dashboard")
def dashboard(current_admin: Admin = Depends(get_current_user), db: Session = Depends(get_db)):
    return get_dashboard_data(current_admin.admin_id, db)

@router.get("/houselist")
def get_admin_houses(db: Session = Depends(get_db), current_admin: Admin = Depends(get_current_user)):
    if not hasattr(current_admin, "admin_id"):
        raise HTTPException(status_code=403, detail="Not authorized as admin")
    houses = db.query(House).filter(House.assigned_for == current_admin.admin_id).all()
    return houses

@router.delete("/delete/{house_id}")
def delete_house(house_id: int, db: Session = Depends(get_db), current_admin: Admin = Depends(get_current_user)):
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

@router.delete("/delete/{house_id}")
def delete_house(house_id: int, db: Session = Depends(get_db), current_admin: Admin = Depends(get_current_user)):
    house = db.query(House).filter(House.house_id == house_id).first()

    if not house:
        raise HTTPException(status_code=404, detail="House not found")
    if house.assigned_for != current_admin.admin_id:
        raise HTTPException(status_code=403, detail="You do not have permission to delete this house")

    db.delete(house)
    db.commit()
    return {"detail": "House deleted successfully"}

@router.post("/house-post")
async def admin_post_house(
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
    if not hasattr(current_user, "admin_id"):
        raise HTTPException(status_code=403, detail="Not authorized as admin")
    print(facilities)
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
    if not description.strip() or len(description) < 20:
        errors["description"] = "Description must be at least 20 characters."
    if price <= 0:
        errors["price"] = "Price must be greater than 0."
    if negotiability not in ["open to negotiation", "not negotiable"]:
        errors["negotiability"] = "Invalid negotiability value."
    if not listedBy.strip():
        errors["listedBy"] = "Listed by is required."
    if not name.strip():
        errors["name"] = "Name is required."
    if not phoneNumber.strip():
        errors["phoneNumber"] = "Phone number is required."
    if not photos:
        errors["photos"] = "At least one photo is required."

    try:
        facilities_list = []  # Initialize the list to avoid the UnboundLocalError

        # Check if facilities look like a JSON array (starts with "[")
        if facilities.strip().startswith("["):
            # If it looks like JSON, parse it as such
            facilities_list = json.loads(facilities)
        else:
            # Fallback: treat as a comma-separated string
            facilities_list = [item.strip() for item in facilities.split(",") if item.strip()]

        if not isinstance(facilities_list, list):
            errors["facilities"] = "Facilities must be a list."
    except Exception:
        errors["facilities"] = "Invalid facilities format."

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
        return {"success": False, "message": "User not found."}

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
        assigned_for=current_user.admin_id,
        status="pending",
    )

    db.add(house)
    db.commit()
    db.refresh(house)

    return {
        "success": True,
        "message": "House posted successfully.",
        "data": {
            "house_id": house.house_id,
            "category": house.category,
            "location": house.location,
            "price": house.price,
            "status": house.status,
        },
    }

@router.get("/visit-request")
def get_visit_requests_for_admin(
    db: Session = Depends(get_db), current_admin: Admin = Depends(get_current_user)
):
    print(current_admin)
    if not hasattr(current_admin, "admin_id"):
        raise HTTPException(status_code=403, detail="Access forbidden: Admins only")

    house_ids = db.query(House.house_id).filter(House.assigned_for == current_admin.admin_id).subquery()
    requests = (
        db.query(Invitation)
        .filter(Invitation.house_id.in_(house_ids), Invitation.status == "not seen")
        .order_by(Invitation.request_date.desc())
        .all()
    )

    return {
        "success": True,
        "visit_requests": [
            {
                "id": r.id,
                "user_id": r.user_id,
                "status": r.status,
                "created_at": r.request_date,
                "visited_date": r.visited_date,
            }
            for r in requests
        ]
    }

@router.put("/{request_id}/mark-seen")
def mark_visit_request_as_seen(
    request_id: int, db: Session = Depends(get_db), current_admin: Admin = Depends(get_current_user)
):
    if not hasattr(current_admin, "admin_id"):
        raise HTTPException(status_code=403, detail="Access forbidden: Admins only")

    visit_request = (
        db.query(Invitation)
        .filter(
            Invitation.id == request_id,
            Invitation.admin_id == current_admin.admin_id
        )
        .first()
    )

    if not visit_request:
        raise HTTPException(status_code=404, detail="Visit request not found.")

    if visit_request.status == "seen":
        return {"success": False, "message": "Already marked as seen."}

    visit_request.status = "seen"
    db.commit()

    return {"success": True, "message": "Visit request marked as seen."}

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
    if not hasattr(current_admin, "admin_id"):
        raise HTTPException(status_code=403, detail="Access forbidden: Admins only")

    visit_request = db.query(Invitation).filter(Invitation.id == request_id).first()
    if not visit_request:
        raise HTTPException(status_code=404, detail="Visit request not found.")

    if visit_request.status != "seen":
        raise HTTPException(status_code=400, detail="Visit request must be marked as seen first.")

    # Save the transaction photo
    filename = f"{current_admin.name.replace(' ', '_')}_{transaction_photo.filename}"
    file_path = os.path.join("media/transaction_photos", filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(transaction_photo.file, buffer)

    success_report = SuccessReport(
        admin_id=current_admin.admin_id,
        invitation_id=request_id,
        price=price,
        type=type,
        commission=commission,
        transaction_photo=file_path
    )

    db.add(success_report)
    db.commit()

    return {"success": True, "message": "Success report created successfully."}

@router.post("/failure-report/{request_id}")
def create_failure_report(
    request_id: int,
    reason: str = Form(...),
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_user)
):
    if not hasattr(current_admin, "admin_id"):
        raise HTTPException(status_code=403, detail="Access forbidden: Admins only")

    visit_request = db.query(Invitation).filter(Invitation.id == request_id).first()
    if not visit_request:
        raise HTTPException(status_code=404, detail="Visit request not found.")

    if visit_request.status != "seen":
        raise HTTPException(status_code=400, detail="Visit request must be marked as seen first.")

    failure_report = FailureReport(
        admin_id=current_admin.admin_id,
        invitation_id=request_id,
        reason=reason
    )

    db.add(failure_report)
    db.commit()

    return {"success": True, "message": "Failure report created successfully."}