from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    phone_no: str
    password: str
    invitation_code: str | None = None

class UserOut(BaseModel):
    user_id: int
    name: str
    phone_no: str

    class Config:
        orm_mode = True
