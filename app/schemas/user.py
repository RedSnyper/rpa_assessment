from pydantic import BaseModel, EmailStr
from typing import List

from app.schemas.video import VideoResponse



class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    u_id: int
    email: EmailStr
    full_name : str
    vid_count: int
    total_spent: int
    class Config:
        orm_mode = True

class UserDetailResponse(UserResponse):
    videos: List[VideoResponse] = []
    class Config: 
        orm_mode = True