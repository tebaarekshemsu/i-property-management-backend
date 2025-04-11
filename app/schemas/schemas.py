from pydantic import BaseModel
from typing import Optional, List 
from enum import Enum
from typing import Optional

class UserCreate(BaseModel):
    name: str
    phone_no: str
    password: str
    invitation_code: Optional[str] = None
    invited_by: Optional[int] = None

class AdminCreate(BaseModel):
    name: str
    phone_no: str
    password: str
    id_front: str
    id_back: str
    invitation_code: Optional[str]
    admin_type: str

class LoginSchema(BaseModel):
    phone_no: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    
class HouseUpdate(BaseModel):
    category: Optional[str]
    location: Optional[str]
    address: Optional[str]
    size: Optional[int]
    condition: Optional[str]
    bedroom: Optional[int]
    toilets: Optional[int]
    listed_by: Optional[str]
    property_type: Optional[str]
    furnish_status: Optional[str]
    bathroom: Optional[int]
    facility: Optional[str]
    description: Optional[str]
    price: Optional[float]
    negotiability: Optional[str]
    parking_space: Optional[bool]
    status: Optional[str]
    image_urls: Optional[List[str]]
    video: Optional[str]

class Config:
    orm_mode = True