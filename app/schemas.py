from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class ImageBase(BaseModel):
    title: str
    description: Optional[str] = None
    value: float


class ImageCreate(ImageBase):
    pass


class ImageResponse(ImageBase):
    id: int
    filename: Optional[str] = None
    cloudinary_url: Optional[str] = None
    cloudinary_public_id: Optional[str] = None
    owner_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class ImageWithOwner(ImageResponse):
    owner: UserResponse


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
