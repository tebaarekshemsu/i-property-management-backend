from fastapi import APIRouter, Depends, HTTPException, Query
from app.services.user import featured_houses, house_detail, house_service ,admin_contact,visit_request
from sqlalchemy.orm import Session
from app.database import SessionLocal
from sqlalchemy.orm import Session
from app.schemas.schemas import UserCreate
from app.models import User
from app.auth.auth_handler import get_password_hash
from app.database import get_db

router = APIRouter(prefix="/user", tags=["User"])

@router.post("/signup")
def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.phone_no == user_data.phone_no).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Phone number already exists")

    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        name=user_data.name,
        phone_no=user_data.phone_no,
        password=hashed_password,
        invitation_code=user_data.invitation_code,
        invited_by=user_data.invited_by
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"status":"ok","msg": "User signed up successfully"}


@router.get('/')
def index():
    return 'hey'

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
    category: str="",

    ):
    return house_service.get_house_list( page, page_size, min_price, max_price, house_type, furnishing_status, bedrooms, bathrooms, location ,category)


@router.post('/visite-request')
def visit_requestt(visit_data: dict):
    return visit_request.save_visit_request(visit_data)

@router.post('/house-post')
def posttt(house_data: dict):
    try:
        with SessionLocal() as db:
            new_house = House(**house_data)
            db.add(new_house)
            db.commit()
            db.refresh(new_house)
            return house_as_dict(new_house)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get('/vip-houses')
def house_list():
    return featured_houses.get_featured_houses()

@router.get('/house/{house_id}')
def detaill(house_id: int):
    return house_detail.get_house_detail(house_id)

@router.get("/admins/search")
def search_admins_by_area_name(
    area_name: str = Query(..., description="Area name to search for"),
):
    return admin_contact.search_admins_by_area_name(area_name)