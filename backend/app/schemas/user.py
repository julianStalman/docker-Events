from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from enums.UserRole import UserRole


class UserBase(BaseModel):
    email: EmailStr = Field(..., min_length=7, max_length=50)
    name: str = Field(..., min_length=1, max_length=100)
    role: UserRole = UserRole.USER


class UserCreate(UserBase):
    password: str = Field(..., min_length=1, max_length=50)


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = Field(None, min_length=7, max_length=50)
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    role: Optional[UserRole] = None
    password: Optional[str] = Field(None, min_length=1, max_length=50)


class UserInDBBase(UserBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class User(UserInDBBase):
    pass


class UserInDB(UserInDBBase):
    hashed_password: str
