from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class UserResponse(BaseModel):
    full_name: str
    email: EmailStr

class VideoCreate(BaseModel):
    vid_title: str

class VideoResponse(BaseModel):
    v_id:int
    vid_title : str
    vid_desc: Optional[str]
    vid_URI: str
    upload_cost: float
    class Config:
        orm_mode = True

class VideoDetailResponse(VideoResponse):
    vid_len: int
    vid_size: int
    vid_type: str
    uploaded_at: datetime
    user: UserResponse
    class Config:
        orm_mode = True