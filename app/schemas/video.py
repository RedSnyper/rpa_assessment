from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

from app.schemas.user import UserResponse

class VideoCreate(BaseModel):
    vid_title: str

class VideoResponse(BaseModel):
    v_id:int
    vid_title : str
    vid_desc: Optional[str]
    vid_URI: str
    class Config:
        orm_mode = True

class VideoDetailResponse(VideoResponse):
    vid_len: int
    vid_size: int
    vid_type: str
    upload_cost: float
    uploaded_at: datetime
    user: UserResponse.email
    class Config:
        orm_mode = True