from pydantic import BaseModel, EmailStr
from typing import List
from datetime import datetime
from app.schemas.video import VideoResponse

class UserReq(BaseModel):
    full_name : str
    email: EmailStr
    password: str

class UserDetail(BaseModel):
    total_spent: float
    vid_count: int
    class Config: 
        orm_mode = True

class UserRes(BaseModel):
    id: str
    full_name: str
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode = True

class UserDetailRes(UserRes):
    detail: List[UserDetail]
    class Config: 
        orm_mode = True