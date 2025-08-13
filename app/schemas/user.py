from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    name: Optional[str] = None
    email: EmailStr
    phone_number : Optional[str] = None
    dob : Optional[datetime] = None
    gender : Optional[int] = None
    identity_number : Optional[str] = None
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number : Optional[str] = None
    dob : Optional[datetime] = None
    gender : Optional[int] = None
    identity_number : Optional[str] = None
    password: Optional[str] = None

class UserView(BaseModel):
    name: Optional[str] = None
    email: EmailStr
    phone_number : Optional[str] = None
    dob : Optional[datetime] = None
    gender : Optional[int] = None
    identity_number : Optional[str] = None

class UserOut(UserView):
    id: int

    class Config:
        orm_mode = True



class UserLogin(BaseModel):
    email: str
    password: str