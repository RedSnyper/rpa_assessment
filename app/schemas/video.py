from pydantic import BaseModel, EmailStr
from enum import Enum
from typing import Optional, List
from datetime import datetime

class VideoType(Enum):
    mkv = 'mkv'
    mp4 = 'mp4'


class VideoResponse(BaseModel):
    id:int
    title : str
    desc: Optional[str]
    URI: str
    uploaded_at: datetime
    class Config:
        orm_mode = True

class VideoDetail(BaseModel):
    len: int
    size: int
    type: Enum
    upload_cost: float
    class Config: 
        orm_mode = True

class VideoDetailResponse(VideoResponse):
    detail: List[VideoDetail]
    class Config:
        orm_mode = True
