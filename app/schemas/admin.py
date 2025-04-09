from pydantic import BaseModel

class AdminCreate(BaseModel):
    name: str
    phone_no: str
    password: str
    admin_type: str  # only 'admin' allowed through API
    id_front: str
    id_back: str
    invitation_code: str | None = None
