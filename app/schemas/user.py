from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    """
    Base schema for user.
    """
    name: str
    phone_no: str
    invitation_code: Optional[str] = None
    invited_by: Optional[str] = None

class UserCreate(UserBase):
    """
    Schema for creating a new user.
    """
    password: str

class UserUpdate(UserBase):
    """
    Schema for updating a user.
    """
    password: Optional[str] = None

class UserInDB(UserBase):
    """
    Schema for user in database.
    """
    user_id: int

    class Config:
        orm_mode = True
