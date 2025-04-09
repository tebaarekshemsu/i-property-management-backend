from pydantic import BaseModel
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
