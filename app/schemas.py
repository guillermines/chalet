from calendar import c
from typing import Optional
from pydantic import BaseModel, EmailStr, conint
from datetime import date, datetime
from typing import Optional

# class Post(BaseModel):
#     title: str
#     content: str
#     published: bool = True
#     # rating: Optional[int] = None
class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class userLogin(BaseModel):
    email: EmailStr
    password: str


class BookingBase(BaseModel):
    start_date: datetime
    end_date: datetime
    number_of_people: int = 1
    validated: bool = False


class BookingCreate(BookingBase):
    pass


class Booking(BookingBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        orm_mode = True


class BookingOut(BaseModel):
    Booking: Booking
    # votes: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None


class Validation(BaseModel):
    booking_id: int
    dir: conint(le=1)
