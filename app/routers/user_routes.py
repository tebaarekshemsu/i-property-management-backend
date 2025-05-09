from typing import List, Optional
from fastapi import APIRouter, Body, Depends, File, HTTPException, Query, Form, UploadFile, logger
from app.services.user import (
    featured_houses,
    house_detail,
    house_service,
    admin_contact,
    visit_request,
    house_post,
    location,
    user_service,
    posted_house,
    fetch_visit_r,
)
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.schemas import UserCreate
from app.models import User
from app.auth.auth_handler import get_password_hash
from app.auth.dependencies import get_current_user


def to_dict(obj):
    """Convert a SQLAlchemy model instance into a dictionary."""
    if obj is None:
        return None
    return {column.key: getattr(obj, column.key) for column in obj.__table__.columns}


router = APIRouter(prefix="/user", tags=["User"])


@router.post("/signup")
def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user.
    """
    print(f"Attempting signup for phone number: {user_data.phone_no}")
    try:
        existing_user = db.query(User).filter(User.phone_no == user_data.phone_no).first()
        if existing_user:
            print(f"Signup failed: Phone number already exists for {user_data.phone_no}")
            raise HTTPException(status_code=400, detail="Phone number already exists")

        hashed_password = get_password_hash(user_data.password)
        new_user = User(
            name=user_data.name,
            phone_no=user_data.phone_no,
            password=hashed_password,
            invitation_code=user_data.invitation_code,
            invited_by=user_data.invited_by if user_data.invited_by else None,
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        return {"status": "ok", "msg": "User signed up successfully"}
    except HTTPException as http_exception:
        print(f"HTTPException during signup for {user_data.phone_no}: {http_exception.detail}")
        raise http_exception
    except Exception as e:
        print(f"An unexpected error occurred during signup for {user_data.phone_no}: {str(e)}")
        db.rollback()  # Rollback the database session in case of an error
        raise HTTPException(status_code=500, detail=f"An error occurred during signup: {str(e)}")


@router.get("/")
def index():
    """
    Simple index endpoint.
    """
    return "hey"


@router.get("/house-list")
def get_houses(
    page: int = 1,
    page_size: int = 10,
    min_price: float = None,
    max_price: float = None,
    house_type: str = None,
    furnishing_status: str = None,
    bedrooms: int = None,
    bathrooms: int = None,
    location: str = None,
    category: str = "",
):
    """
    Get a list of houses with optional filtering.
    """
    return house_service.get_house_list(
        page, page_size, min_price, max_price, house_type, furnishing_status, bedrooms, bathrooms, location, category
    )


@router.post("/visite-request")
def visit_requestt(
    visit_data: dict,
    current_user: User = Depends(user_service.get_current_user),
    db: Session = Depends(get_db),
):
    """
    Create a visit request for a house.
    """
    print(f"Debugging: Received visit request data: {visit_data}")
    print(f"Debugging: Current user ID: {current_user.user_id}")
    print(f"Debugging: Database session: {db}")
    try:
        house_id = visit_data.get("house_id")
        if isinstance(house_id, dict):
            house_id = house_id.get("id")

        if not house_id or not str(house_id).isdigit():
            raise HTTPException(status_code=400, detail="Invalid house_id provided.")

        visit_data["house_id"] = int(house_id)
        result = visit_request.save_visit_request(visit_data, current_user.user_id, db)
        print(f"Debugging: Visit request saved successfully. Result: {result}")
        return result
    except HTTPException as http_exception:
        print(f"Debugging: HTTPException occurred: {http_exception.detail}")
        raise http_exception
    except Exception as e:
        print(f"Debugging: An unexpected error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An error occurred while processing visit request: {str(e)}")


@router.post("/house-post")
def post_house(
    current_user: User = Depends(user_service.get_current_user),
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
    facilities: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    negotiability: str = Form(...),
    parkingSpace: bool = Form(...),
    listedBy: str = Form(...),
    videoLink: Optional[str] = Form(None),
    photos: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
):
    """
    Post a new house.
    """
    try:
        return house_post.create_house(
            category=category,
            location=location,
            address=address,
            size=size,
            condition=condition,
            bedrooms=bedrooms,
            toilets=toilets,
            bathrooms=bathrooms,
            propertyType=propertyType,
            furnishStatus=furnishStatus,
            facilities=facilities,
            description=description,
            price=price,
            negotiability=negotiability,
            parkingSpace=parkingSpace,
            listedBy=listedBy,
            name=current_user.name,
            phoneNumber=current_user.phone_no,
            videoLink=videoLink,
            photos=photos,
            user_id=current_user.user_id,
            db=db,
        )
    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while posting house: {str(e)}")


@router.get("/locations")
def get_locations():
    """
    Get all available locations.
    """
    try:
        return location.get_all_locations()
    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while fetching locations: {str(e)}")


@router.get("/vip-houses")
def house_list():
    """
    Get a list of VIP houses.
    """
    try:
        return featured_houses.get_featured_houses()
    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while fetching featured houses: {str(e)}")


@router.get("/house/{house_id}")
def detaill(house_id: int):
    """
    Get detailed information about a specific house.
    """
    try:
        return house_detail.get_house_detail(house_id)
    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while fetching house details: {str(e)}")


@router.get("/admins/search")
def search_admins_by_area_name(area_name: str = Query(..., description="Area name to search for")):
    """
    Search for admins by area name.
    """
    return admin_contact.search_admins_by_area_name(area_name)


@router.get("/profile")
def get_user_profile(current_user: User = Depends(get_current_user)):
    """
    Get the current user's profile.
    """
    return user_service.get_user_profile(current_user)


@router.put("/profile")
def update_user_profile(user_data: dict = Body(...), current_user: User = Depends(get_current_user)):
    """
    Update the current user's profile.
    """
    return user_service.update_user_profile(user_data, current_user)


@router.get("/posted")
def fetch_posted_houses(current_user: User = Depends(get_current_user)):
    """
    Get all houses posted by the current user.
    """
    return posted_house.fetch_posted_houses(current_user)


@router.get("/fetch_visit_request")
def fetch_visit_requests(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Get all visit requests for the current user.
    """
    return fetch_visit_r.fetch_visit_requests(current_user, db)