from fastapi import APIRouter, Depends, HTTPException
from app.services.user import featured_houses, house_detail, visit_request, house_service
from sqlalchemy.orm import Session
from app.database import SessionLocal

router = APIRouter(prefix='/user', tags=['User'])

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

    
):
    return house_service.get_house_list( page, page_size, min_price, max_price, house_type, furnishing_status, bedrooms, bathrooms, location)


@router.post('/visite-request')
def visit_request(visit_data: dict):
    return visit_request.save_visit_request(visit_data)

@router.post('/house-post')
def posttt():
    return 'posting'

@router.get('/vip-houses')
def house_list():
    return featured_houses.get_featured_houses()

@router.get('/detail/{house_id}')
def detail(house_id: int, db: Session = Depends(SessionLocal)):
    try:
        return house_service.get_house_detail(db, house_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/houses/{house_id}")
def get_house_by_id(house_id: int, db: Session = Depends(SessionLocal)):
    try:
        return house_service.get_house_detail(db, house_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
