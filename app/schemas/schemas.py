from pydantic import BaseModel, EmailStr
from typing import Optional, List 
from enum import Enum

class UserCreate(BaseModel):
    """
    Schema for creating a new user.
    """
    name: str
    phone_no: str
    password: str
    invitation_code: Optional[str] = None
    invited_by: Optional[str] = None

class AdminCreate(BaseModel):
    """
    Schema for creating a new admin.
    """
    name: str
    phone_no: str
    password: str
    id_front: str
    id_back: str
    invitation_code: str
    admin_type: str

class LoginSchema(BaseModel):
    phone_no: str
    password: str

class Token(BaseModel):
    """
    Schema for JWT token.
    """
    access_token: str
    token_type: str
    
class HouseUpdate(BaseModel):
    """
    Schema for updating a house.
    """
    category: Optional[str] = None
    location: Optional[str] = None
    address: Optional[str] = None
    size: Optional[float] = None
    condition: Optional[str] = None
    bedroom: Optional[int] = None
    toilets: Optional[int] = None
    bathroom: Optional[int] = None
    property_type: Optional[str] = None
    furnish_status: Optional[str] = None
    facility: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    negotiability: Optional[str] = None
    parking_space: Optional[bool] = None
    listed_by: Optional[str] = None
    video: Optional[str] = None

class Config:
    orm_mode = True