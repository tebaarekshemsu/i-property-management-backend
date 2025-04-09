from typing import List, Optional
from fastapi import APIRouter, Depends, File, HTTPException, Query,Form, UploadFile 
from app.services.user import featured_houses, house_detail, house_service ,admin_contact,visit_request,house_post ,location
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
    category: str="",

    ):
    return house_service.get_house_list( page, page_size, min_price, max_price, house_type, furnishing_status, bedrooms, bathrooms, location ,category)


@router.post('/visite-request')
def visit_requestt(visit_data: dict):
    return visit_request.save_visit_request(visit_data)

@router.post("/house-post")
async def post_house(
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
    name: str = Form(...),
    phoneNumber: str = Form(...),
    videoLink: Optional[str] = Form(None),
    photos: List[UploadFile] = File(...)
):
    return house_post.create_house_posting(
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
        name=name,
        phoneNumber=phoneNumber,
        videoLink=videoLink,
        photos=photos
    )

@router.get("/locations")
def get_locations():
    return location.get_all_locations()


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