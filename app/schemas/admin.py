from pydantic import BaseModel
from typing import Optional

class AdminBase(BaseModel):
    """
    Base schema for admin.
    """
    name: str
    phone_no: str
    id_front: str
    id_back: str
    invitation_code: str
    admin_type: str

class AdminCreate(AdminBase):
    """
    Schema for creating a new admin.
    """
    password: str

class AdminUpdate(AdminBase):
    """
    Schema for updating an admin.
    """
    password: Optional[str] = None

class AdminInDB(AdminBase):
    """
    Schema for admin in database.
    """
    admin_id: int

    class Config:
        orm_mode = True
